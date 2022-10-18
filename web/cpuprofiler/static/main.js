let profiler_times = [];
let profiler_results = [];
let profiler_names = [];
let profiler_chart_types = [];
const PROFILERS = 5;
let tmp;
let LARGE = true;
let stop = false;

async function startProfilers() {
  window.scrollBy(0, 10000);

  document.getElementById("startButton").disabled = true;

  // Shared memory
  memory = new WebAssembly.Memory({
    initial: amountOfPages,
    maximum: amountOfPages,
    shared: true,
  });

  const clock = await startClockWorker();

  tmp = performance.now();
  profiler_names.push("Cacheassociativity");
  updateProfiler("Cacheassociativity");
  cacheassociativity(memory, clock);
}

async function checkChargingStatus() {
  let status = document.getElementById("chargingstatus");
  if (navigator.getBattery) {
    navigator.getBattery().then(function (battery) {
      let button = document.getElementById("chargingbutton");
      button.classList.remove("btn-secondary");
      button.classList.remove("btn-success");
      button.classList.remove("btn-danger");
      if (battery.charging) {
        status.innerText = "Charging!";
        button.classList.add("btn-success");
      } else {
        status.innerText = "Not charging?";
        button.classList.add("btn-danger");
      }
    });
  } else {
    status.innerText = "Still unknown";
  }
}
