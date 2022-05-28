async function calculateBits(CanvasJS) {
  document.getElementById("startButton").disabled = true;

  let points = [];

  // Shared memory
  memory = new WebAssembly.Memory({
    initial: amountOfPages,
    maximum: amountOfPages,
    shared: true,
  });

  // Clock thread
  const resp = await fetch("/static/wasm/bits.wasm");
  const bin = await resp.arrayBuffer();
  const module = new WebAssembly.Module(bin);
  const instance = new WebAssembly.Instance(module, {
    env: { mem: memory },
    console: {
      log: function (arg) {
        console.log(arg);
      },
    },
  });

  let start = performance.now();

  for (let i = 0; i < 10000000; i++) {
    instance.exports.test8();
  }

  let time = performance.now() - start;
  points.push({ y: Number(time), label: "8" });

  updateProgress(0.5);

  start = performance.now();

  for (let i = 0; i < 10000000; i++) {
    instance.exports.test9();
  }

  time = performance.now() - start;
  points.push({ y: Number(time), label: "9" });

  updateProgress(1);

  var chart = new CanvasJS.Chart("chartContainer", {
    animationEnabled: true,
    theme: "light2",
    data: [
      {
        type: "column",
        indexLabelFontSize: 16,
        dataPoints: points,
      },
    ],
  });
  chart.render();
}
