const bufferSize = 64 * 1024 * 1024;
const wasmPageSize = 64 * 1024;
const amountOfPages = bufferSize / wasmPageSize;
const VERBOSE = true;

function log(...s) {
  var output = document.getElementById("result-container");
  output.innerText = s;
}

function updateProgress(value) {
  var bar = document.getElementById("mainBar");
  bar.style.width = `${Number(value * 100)}%`;
  if (Number(value) === 1) {
    bar.classList += " bg-success";
  }
  if (Number(value) === 0) {
    bar.classList = "progress-bar";
  }
}

function jsonify(data) {
  return JSON.stringify(data, (key, value) =>
    typeof value === "bigint" ? value.toString() : value
  );
}

async function startClockWorker() {
  const resp = await fetch("/static/wasm/clock.wasm");
  const bin = await resp.arrayBuffer();
  const module = new WebAssembly.Module(bin);
  const clock = new Worker("/static/utils/clockWorker.js");
  clock.postMessage({ module: module, memory: memory });
  return clock;
}

function createChart(headers, url, id, points) {
  let params = {
    points: points,
  };

  fetch(url, {
    method: "POST",
    headers: headers,
    body: jsonify(params),
    credentials: "same-origin",
  })
    .then((res) => res.blob())
    .then((blob) => {
      document.getElementById("image" + id).src = URL.createObjectURL(blob);
    });
}

// main page specific

function createAccordionItem(accordion, id, name, time) {
  let header = document.createElement("h2");
  header.classList = "accordion-header";
  header.id = "heading" + id;

  let toggle = document.createElement("button");
  toggle.innerText = name;
  toggle.classList = "accordion-button collapsed";
  toggle.setAttribute("type", "button");
  toggle.setAttribute("data-bs-toggle", "collapse");
  toggle.setAttribute("data-bs-target", "#collapse" + id);
  toggle.setAttribute("aria-expanded", "false");
  toggle.setAttribute("aria-controls", "collapse" + id);

  header.appendChild(toggle);

  let body = document.createElement("div");
  body.classList = "accordion-collapse collapse";
  body.id = "collapse" + id;
  body.setAttribute("aria-labelledby", "heading" + id);
  body.setAttribute("data-bs-parent", "#" + accordion);

  let bodyContainer = document.createElement("div");
  bodyContainer.classList = "accordion-body";

  let timeContainer = document.createElement("p");
  timeContainer.style = "text-align: center";
  timeContainer.innerText = time;

  let image = document.createElement("img");
  image.style =
    "display: block; margin-left: auto; margin-right: auto; width: 80%;";
  image.id = "image" + id;

  bodyContainer.appendChild(timeContainer);
  bodyContainer.appendChild(image);

  body.appendChild(bodyContainer);

  let container = document.createElement("div");
  container.classList = "accordion-item";
  container.appendChild(header);
  container.appendChild(body);

  document.getElementById(accordion).appendChild(container);
}

async function createChartsAndUpload() {
  document.getElementById("waitingcontainer").hidden = false;
  document.getElementById("waitingcontainer2").hidden = false;

  await new Promise((r) => setTimeout(r, 100));

  const unit = " s";
  const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  let headers = {
    "Content-Type": "application/json;charset=UTF-8",
    "X-CSRFToken": csrftoken,
  };

  // adjust execution times to seconds
  profiler_times = profiler_times.map(
    (x) => Math.round((x / 1000 + Number.EPSILON) * 100) / 100
  );

  if (VERBOSE) {
    for (let i = 0; i < profiler_results.length; i++) {
      createAccordionItem(
        "resultAccordion",
        i,
        profiler_names[i],
        profiler_times[i] + unit
      );
      createChart(headers, profiler_chart_types[i], i, profiler_results[i]);
    }
  }

  let data = {
    benchmark_results: profiler_results,
    user_agent: navigator.userAgent.substring(0, 255),
    times: profiler_times,
  };

  let success = await fetch("/upload/", {
    method: "POST",
    headers: headers,
    body: jsonify(data),
  });

  if (success.status != 200) {
    throw new Error("Unexpected response");
  } else {
    let predictions = await success.json();

    // actual predictions
    document.getElementById("l1").innerText =
      predictions["L1CacheSizes"] + " KB";
    document.getElementById("l2").innerText =
      predictions["L2CacheSizes"] + " KB";
    document.getElementById("l3").innerText =
      predictions["L3CacheSizes"] + " MB";
    document.getElementById("l1asso").innerText =
      predictions["L1Associativities"];
    document.getElementById("cores").innerText = predictions["NumberofThreads"];
    document.getElementById("vendor").innerText = predictions["AMDvsIntel"];
    document.getElementById("uarch").innerText =
      predictions["Microarchitectures"];
    document.getElementById("model").innerText =
      predictions["Modelswithexecutiontimes"];

    // confidence
    document.getElementById("l1proba").innerText =
      predictions["L1CacheSizesproba"].toFixed(2);
    document.getElementById("l2proba").innerText =
      predictions["L2CacheSizesproba"].toFixed(2);
    document.getElementById("l3proba").innerText =
      predictions["L3CacheSizesproba"].toFixed(2);
    document.getElementById("l1assoproba").innerText =
      predictions["L1Associativitiesproba"].toFixed(2);
    document.getElementById("coresproba").innerText =
      predictions["NumberofThreadsproba"].toFixed(2);
    document.getElementById("vendorproba").innerText =
      predictions["AMDvsIntelproba"].toFixed(2);
    document.getElementById("uarchproba").innerText =
      predictions["Microarchitecturesproba"].toFixed(2);
    document.getElementById("modelproba").innerText =
      predictions["Modelswithexecutiontimesproba"].toFixed(2);
  }

  document.getElementById("waitingcontainer").hidden = true;
  document.getElementById("waitingcontainer2").hidden = true;
  document.getElementById("resultcontainer").hidden = false;
}

function updateProfiler(value) {
  var bar = document.getElementById("mainBar");
  bar.innerHTML = value;
}

function updateTotalProgress(value) {
  var bar = document.getElementById("totalBar");
  bar.style.width = `${Number(value * 100)}%`;
  if (Number(value) === 1) {
    bar.classList += " bg-success";
  }
}

function nextProfiler(profiler) {
  profiler_times.push(performance.now() - tmp);
  updateTotalProgress(profiler_results.length / PROFILERS);
  updateProgress(0);
  updateProfiler(profiler);
  profiler_names.push(profiler);
  tmp = performance.now();
}
