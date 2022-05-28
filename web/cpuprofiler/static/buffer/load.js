let wabt;
let mod_module;
let parts;
let pump_counter = 0;
let pump_part = "";
let points = [];

async function calculateLoadBufferSize(CanvasJS) {
  document.getElementById("startButton").disabled = true;

  // Shared memory
  memory = new WebAssembly.Memory({
    initial: amountOfPages,
    maximum: amountOfPages,
    shared: true,
  });

  // Clock thread
  const clock = await startClockWorker();

  const resp2 = await fetch("/static/wasm/loadbuffer.wat");
  let text = await resp2.text();
  let wabt = await new WabtModule();
  parts = text.split("here");

  let pumped = parts[0] + pump_part + parts[1] + pump_part + parts[2];

  let wabt_module = wabt.parseWat("pumped", pumped, { threads: true });
  mod_module = await wabt_module.toBinary({
    log: false,
    canonicalize_lebs: false,
    relocatable: false,
    write_debug_names: false,
  });
  mod_module = await mod_module.buffer.buffer;
  wabt_module.destroy();
  mod_module = new WebAssembly.Module(mod_module);

  let finished = 0;
  const OUTER_ITERATIONS = 116;

  const finder = new Worker("/static/buffer/loadWorker.js");
  finder.onmessage = function handle(evt) {
    let msg = evt.data;
    switch (msg.type) {
      case "result":
        points.push({ x: finished + 16, y: Number(msg.result) });
        finished += 1;
        updateProgress(finished / OUTER_ITERATIONS);
        // update module
        next_iteration();
        //
        finder.postMessage({ module: mod_module, memory: memory });

        if (finished == OUTER_ITERATIONS) {
          clock.terminate();
          finder.terminate();
          var chart = new CanvasJS.Chart("chartContainer", {
            animationEnabled: true,
            theme: "light2",
            data: [
              {
                type: "line",
                indexLabelFontSize: 16,
                dataPoints: points,
              },
            ],
          });
          chart.render();
        }
        break;
      default:
    }
  };
  finder.postMessage({ module: mod_module, memory: memory });
}

async function next_iteration() {
  wabt = await new WabtModule();
  pump_counter += 128;
  pump_part += `\n(i32.add (i32.load (i32.const ${512 + pump_counter})))\n`;
  pumped = parts[0] + pump_part + parts[1] + pump_part + parts[2];

  let wabt_module = wabt.parseWat("pumped", pumped, { threads: true });
  mod_module = await wabt_module.toBinary({
    log: false,
    canonicalize_lebs: false,
    relocatable: false,
    write_debug_names: false,
  });
  mod_module = await mod_module.buffer.buffer;
  wabt_module.destroy();
  mod_module = new WebAssembly.Module(mod_module);
}

function concatenate(resultConstructor, ...arrays) {
  let totalLength = 0;
  for (const arr of arrays) {
    totalLength += arr.length;
  }
  const result = new resultConstructor(totalLength);
  let offset = 0;
  for (const arr of arrays) {
    result.set(arr, offset);
    offset += arr.length;
  }
  return result;
}
