async function calculatePageSize(CanvasJS) {
  document.getElementById("startButton").disabled = true;

  // Shared memory
  memory = new WebAssembly.Memory({
    initial: amountOfPages,
    maximum: amountOfPages,
    shared: true,
  });

  const clock = await startClockWorker();

  const resp2 = await fetch("/static/wasm/pagesize.wasm");
  const bin2 = await resp2.arrayBuffer();
  const module2 = new WebAssembly.Module(bin2);
  const finder = new Worker("/static/misc/pagesize/pagesizeFinder.js");
  finder.onmessage = function handle(evt) {
    let msg = evt.data;
    switch (msg.type) {
      case "progress":
        updateProgress(msg.value);
        break;
      case "log":
        log(...msg.str);
        break;
      case "terminate":
        clock.terminate();
        finder.terminate();
        break;

      case "results":
        var chart = new CanvasJS.Chart("chartContainer", {
          animationEnabled: true,
          theme: "light2",
          data: [
            {
              type: "line",
              indexLabelFontSize: 16,
              dataPoints: msg.points,
            },
          ],
        });
        chart.render();
        break;
      default:
    }
  };
  finder.postMessage({ module: module2, memory: memory });
}
