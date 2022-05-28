async function calculateCacheSize(CanvasJS) {
  document.getElementById("startButton").disabled = true;

  // Shared memory
  memory = new WebAssembly.Memory({
    initial: amountOfPages,
    maximum: amountOfPages,
    shared: true,
  });

  const clock = await startClockWorker();

  const resp2 = await fetch("/static/wasm/size.wasm");
  const bin2 = await resp2.arrayBuffer();
  const module2 = new WebAssembly.Module(bin2);
  const finder = new Worker("/static/cache/sizeFinder.js");
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
        console.log(msg.points.slice(0, 128));
        console.log(msg.points.slice(129));
        var chartSmall = new CanvasJS.Chart("chartContainerSmall", {
          animationEnabled: true,
          theme: "light2",
          data: [
            {
              type: "line",
              indexLabelFontSize: 16,
              dataPoints: msg.points.slice(0, 128),
            },
          ],
        });
        chartSmall.render();
        var chartLarge = new CanvasJS.Chart("chartContainerLarge", {
          animationEnabled: true,
          theme: "light2",
          data: [
            {
              type: "line",
              indexLabelFontSize: 16,
              dataPoints: msg.points.slice(129),
            },
          ],
        });
        chartLarge.render();
        break;
      default:
    }
  };
  finder.postMessage({ module: module2, memory: memory, large: true });
}
