// Idea: http://pmav.eu/stuff/javascript-webworkers/
const MAX = 65;
let points = [];

let workers = [];
let results = [];
let finishedWorkers = 0;
let start = 0;
let end = 0;
let amountOfWorkers = 1;
let endResult = 1;
let canvasLib;

function countCores(CanvasJS) {
  document.getElementById("startButton").disabled = true;

  canvasLib = CanvasJS;
  run(amountOfWorkers, 2, 2048000000, 97777);
}

function run(workersAmount, base, power, mod) {
  results = new Array(workersAmount).fill(0);

  for (let i = 0; i < workersAmount; i++) {
    let worker = new Worker("/static/misc/cores/worker.js");
    worker.onmessage = callback;
    workers.push(worker);
  }

  start = performance.now();

  for (let i = 0; i < workersAmount; i++) {
    let data = {};
    data.workerId = i;
    data.base = base;
    data.power = 128000000 / 4;
    data.mod = mod;
    workers[i].postMessage(data);
  }
}

function callback(event) {
  let data = event.data;
  workers[data.workerId].terminate();
  results[data.workerId] = data.result;

  if (++finishedWorkers == amountOfWorkers) {
    end = performance.now() - start;

    for (let i = 0; i < results.length; i++) {
      endResult = (endResult * results[i]) % data.mod;
    }

    points.push({ x: amountOfWorkers, y: end });

    if (amountOfWorkers == 1) amountOfWorkers += 1;
    else if (amountOfWorkers < 32) amountOfWorkers += 2;
    else amountOfWorkers += 16;

    if (amountOfWorkers < MAX) {
      results = [];
      workers = [];
      endResult = 1;
      finishedWorkers = 0;
      updateProgress(amountOfWorkers / MAX);
      run(amountOfWorkers, 2, 2048000000, 97777);
    }

    if (amountOfWorkers >= MAX) {
      updateProgress(1);
      var chart = new canvasLib.Chart("chartContainer", {
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
  }
}
