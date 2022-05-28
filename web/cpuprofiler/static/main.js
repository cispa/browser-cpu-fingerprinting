let profiler_times = [];
let profiler_results = [];
let profiler_names = [];
let profiler_chart_types = [];
const PROFILERS = 13;
let tmp;
let LARGE = true;

async function startProfilers() {
  if (document.getElementById("model").value == "") {
    document.getElementById("model").classList.add("is-invalid");
    return;
  }

  if (document.getElementById("workerid").value == "") {
    document.getElementById("workerid").classList.add("is-invalid");
    return;
  }

  window.scrollBy(0, 10000);

  interval_id = setInterval(dec_timer, 1000);

  document.getElementById("model").classList.remove("is-invalid");
  document.getElementById("model").setAttribute("readonly", true);

  document.getElementById("workerid").classList.remove("is-invalid");
  document.getElementById("workerid").setAttribute("readonly", true);

  document.getElementById("lowMemory").disabled = true;
  document.getElementById("startButton").disabled = true;

  // Shared memory
  memory = new WebAssembly.Memory({
    initial: amountOfPages,
    maximum: amountOfPages,
    shared: true,
  });

  const clock = await startClockWorker();

  tmp = performance.now();
  profiler_names.push("Pagesize");
  updateProfiler("Pagesize");
  pagesize(memory, clock);
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
