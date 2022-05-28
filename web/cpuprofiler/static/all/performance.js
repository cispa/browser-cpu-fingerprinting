async function calculateSinglePerformance() {
  let points = [];

  let ITERATIONS = 500;
  let counter;
  let start;

  for (let i = 0; i < ITERATIONS; i++) {
    counter = 0;
    start = performance.now() + 1;
    while (start > performance.now()) {
      counter += 1;
    }

    points.push({ x: Number(i), y: Number(counter) });
  }

  updateProgress(1 / 3);

  await new Promise((r) => setTimeout(r, 100));

  for (let i = 0; i < ITERATIONS; i++) {
    counter = 0;
    start = performance.now() + 1;
    while (start > performance.now()) {
      counter += 1;
    }

    points.push({ x: Number(i + ITERATIONS), y: Number(counter) });
  }

  updateProgress(2 / 3);

  await new Promise((r) => setTimeout(r, 100));

  for (let i = 0; i < ITERATIONS; i++) {
    counter = 0;
    start = performance.now() + 1;
    while (start > performance.now()) {
      counter += 1;
    }

    points.push({ x: Number(i + ITERATIONS * 2), y: Number(counter) });
  }

  updateProgress(1);

  profiler_results.push(points);
  profiler_chart_types.push("/plot/line/");

  nextProfiler("Multi core performance");
  if (stop) return;
  calculateMultiPerformance();
}

async function calculateMultiPerformance() {
  let WORKERS = 10;
  const ITERATIONS = 10000;
  let results = new Array(WORKERS).fill({});
  let workers = [];
  let finishedWorkers = 0;

  for (let i = 0; i < WORKERS; i++) {
    let worker = new Worker("/static/performance/performanceWorker.js");
    worker.onmessage = function (event) {
      let data = event.data;
      workers[data.workerId].terminate();
      results[data.workerId] = data.points;
      finishedWorkers += 1;
      updateProgress(finishedWorkers / WORKERS);

      if (finishedWorkers == WORKERS) {
        profiler_results.push(results);
        profiler_chart_types.push("/plot/multiline/");

        nextProfiler("Number of cores");
        if (stop) return;
        run(1, 2, 97777);
      }
    };
    workers.push(worker);
  }

  for (let i = 0; i < WORKERS; i++) {
    workers[i].postMessage({ workerId: i, iterations: ITERATIONS });
  }
}
