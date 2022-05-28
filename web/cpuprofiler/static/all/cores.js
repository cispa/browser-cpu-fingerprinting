const CORES_MAX_WORKERS = 33;

let cores_workers = [];
let cores_tmp_results = [];
let cores_finishedWorkers = 0;

let cores_start = 0;
let cores_end = 0;
let cores_amountOfWorkers = 1;
let cores_points = [];

function run(workersAmount, base, mod) {
  cores_tmp_results = new Array(workersAmount).fill(0);
  cores_start = performance.now();
  for (let i = 0; i < workersAmount; i++) {
    let worker = new Worker("/static/misc/cores/worker.js");
    worker.onmessage = callback;
    cores_workers.push(worker);
  }

  for (let i = 0; i < workersAmount; i++) {
    let data = {};
    data.workerId = i;
    data.base = base;
    data.power = 128000000 / 4;
    data.mod = mod;
    cores_workers[i].postMessage(data);
  }
}

function callback(event) {
  let data = event.data;
  cores_workers[data.workerId].terminate();
  cores_tmp_results[data.workerId] = data.result;

  if (++cores_finishedWorkers == cores_amountOfWorkers) {
    cores_end = performance.now() - cores_start;

    cores_points.push({ x: cores_amountOfWorkers, y: cores_end });

    if (cores_amountOfWorkers == 1) cores_amountOfWorkers += 1;
    else if (cores_amountOfWorkers < 32) cores_amountOfWorkers += 2;
    else cores_amountOfWorkers += 16;

    if (cores_amountOfWorkers < CORES_MAX_WORKERS) {
      cores_tmp_results = [];
      cores_workers = [];
      cores_finishedWorkers = 0;
      updateProgress(cores_amountOfWorkers / CORES_MAX_WORKERS);
      run(cores_amountOfWorkers, 2, 97777);
    }

    if (cores_amountOfWorkers >= CORES_MAX_WORKERS) {
      cores_amountOfWorkers = 0;
      profiler_results.push(cores_points);
      profiler_chart_types.push("/plot/line/");
      profiler_times.push(performance.now() - tmp);

      updateProfiler("");
      updateProgress(1);
      updateTotalProgress(1);
      if (stop) return;
      createChartsAndUpload();
    }
  }
}
