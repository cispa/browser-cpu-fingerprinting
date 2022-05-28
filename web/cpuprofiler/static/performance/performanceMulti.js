let WORKERS = 1;
const ITERATIONS = 10000;
let results = new Array(WORKERS).fill({});
let workers = [];
let finishedWorkers = 0;

async function calculatePerformance(CanvasJS) {
  document.getElementById("startButton").disabled = true;

  WORKERS = Number(document.forms["startForm"]["cores"].value);

  if (isNaN(WORKERS) || WORKERS == 0) {
    WORKERS = 1;
  }

  for (let i = 0; i < WORKERS; i++) {
    let worker = new Worker("/static/performance/performanceWorker.js");
    worker.onmessage = callback;
    workers.push(worker);
  }

  for (let i = 0; i < WORKERS; i++) {
    workers[i].postMessage({ workerId: i, iterations: ITERATIONS });
  }
}

function callback(event) {
  let data = event.data;
  workers[data.workerId].terminate();
  results[data.workerId] = {
    type: "line",
    indexLabelFontSize: 16,
    dataPoints: data.points,
  };
  finishedWorkers += 1;
  updateProgress(finishedWorkers / WORKERS);

  if (finishedWorkers == WORKERS) {
    var chart = new CanvasJS.Chart("chartContainer", {
      animationEnabled: true,
      theme: "light2",
      data: results,
    });
    chart.render();
  }
}
