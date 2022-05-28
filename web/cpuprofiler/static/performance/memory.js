let finished = 0;
let result = [];
let clock;
let finder1;
let finder2;

async function calculateMemoryLatencies(CanvasJS) {
  document.getElementById("startButton").disabled = true;

  // Shared memory
  memory = new WebAssembly.Memory({
    initial: amountOfPages,
    maximum: amountOfPages,
    shared: true,
  });

  clock = await startClockWorker();

  const resp2 = await fetch("/static/wasm/pagesize.wasm");
  const bin2 = await resp2.arrayBuffer();
  const module2 = new WebAssembly.Module(bin2);
  finder1 = new Worker("/static/performance/memoryWorker.js");
  finder2 = new Worker("/static/performance/memoryWorker.js");

  finder1.onmessage = handle;
  finder2.onmessage = handle;

  finder1.postMessage({ module: module2, memory: memory });
  finder2.postMessage({ module: module2, memory: memory });
}

function handle(evt) {
  let msg = evt.data;
  switch (msg.type) {
    case "progress":
      updateProgress(msg.value);
      break;
    case "log":
      log(...msg.str);
      break;
    case "results":
      const csrftoken = document.querySelector(
        "[name=csrfmiddlewaretoken]"
      ).value;
      let headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "X-CSRFToken": csrftoken,
      };

      result = result.concat(msg.points);

      if (++finished == 2) {
        clock.terminate();
        finder1.terminate();
        finder2.terminate();
        let params = {
          points: result,
        };
        fetch("/plot/hist/", {
          method: "POST",
          headers: headers,
          body: jsonify(params),
          credentials: "same-origin",
        })
          .then((res) => res.blob())
          .then((blob) => {
            document.getElementById("memoryLatencyGraph").src =
              URL.createObjectURL(blob);
          });
      }
    default:
  }
}
