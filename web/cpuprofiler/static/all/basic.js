async function pagesize(memory, clock) {
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
      case "terminate":
        finder.terminate();
        break;
      case "results":
        profiler_results.push(msg.points);
        profiler_chart_types.push("/plot/line/");

        nextProfiler("Prefetcher");
        if (stop) return;
        prefetcher(memory, clock);
        break;
      default:
    }
  };
  finder.postMessage({ module: module2, memory: memory });
}

async function prefetcher(memory, clock) {
  const resp2 = await fetch("/static/wasm/prefetch.wasm");
  const bin2 = await resp2.arrayBuffer();
  const module2 = new WebAssembly.Module(bin2);
  const finder = new Worker("/static/misc/prefetcher/prefetchWorker.js");
  finder.onmessage = function handle(evt) {
    let msg = evt.data;
    switch (msg.type) {
      case "progress":
        updateProgress(msg.value);
        break;
      case "terminate":
        finder.terminate();
        break;
      case "results":
        profiler_results.push(msg.points);
        profiler_chart_types.push("/plot/bar/");

        nextProfiler("Cache associativity");
        if (stop) return;
        cacheassociativity(memory, clock);
        break;
      default:
    }
  };
  finder.postMessage({ module: module2, memory: memory });
}

async function cacheassociativity(memory, clock) {
  const resp2 = await fetch("/static/wasm/size.wasm");
  const bin2 = await resp2.arrayBuffer();
  const module2 = new WebAssembly.Module(bin2);
  const finder = new Worker("/static/cache/assoFinder.js");
  finder.onmessage = function handle(evt) {
    let msg = evt.data;
    switch (msg.type) {
      case "progress":
        updateProgress(msg.value);
        break;
      case "terminate":
        finder.terminate();
        break;
      case "results":
        profiler_results.push(msg.points);
        profiler_chart_types.push("/plot/line/");

        nextProfiler("Cache size up to 512KB");
        if (stop) return;
        cachesize(memory, clock);
        break;
      default:
    }
  };
  finder.postMessage({ module: module2, memory: memory });
}

async function cachesize(memory, clock) {
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
      case "terminate":
        finder.terminate();
        break;
      case "results":
        profiler_results.push(msg.points.slice(0, 128));
        profiler_chart_types.push("/plot/line/");

        profiler_names.push("Cache size from 0.5 MB upwards");
        profiler_results.push(msg.points.slice(129));
        profiler_chart_types.push("/plot/line/");

        nextProfiler("TLB size");
        profiler_times.push(profiler_times[profiler_times.length - 1]);
        if (stop) return;
        tlbsize(memory, clock);
        break;
      default:
    }
  };
  finder.postMessage({
    module: module2,
    memory: memory,
    large: true,
  });
}

async function tlbsize(memory, clock) {
  const resp2 = await fetch("/static/wasm/size.wasm");
  const bin2 = await resp2.arrayBuffer();
  const module2 = new WebAssembly.Module(bin2);
  const finder = new Worker("/static/tlb/tlbsizeFinder.js");
  finder.onmessage = function handle(evt) {
    let msg = evt.data;
    switch (msg.type) {
      case "progress":
        updateProgress(msg.value);
        break;
      case "results":
        finder.terminate();
        profiler_results.push(msg.points);
        profiler_chart_types.push("/plot/line/");

        nextProfiler("Number of Cores");
        if (stop) return;
        run(1, 2, 97777);
        break;
      default:
    }
  };
  finder.postMessage({ module: module2, memory: memory });
}

async function calculatePrecision(memory, clock) {
  const view = new DataView(memory.buffer);
  const ITERATIONS = 3;
  const INNER_ITERATIONS = 1000;
  let pointsDiff = [];
  let pointsAbs = [];

  await new Promise((r) => setTimeout(r, 10));

  tmp = performance.now();

  for (let j = 0; j < INNER_ITERATIONS; j++) {
    let tmp = view.getBigUint64(0, true);
    view.setBigUint64(0, tmp + 1n, true);
  }

  let totalStart = view.getBigUint64(256, true);
  for (let i = 0; i < ITERATIONS; i++) {
    let start = view.getBigUint64(256, true);

    await new Promise((r) => setTimeout(r, 1000));
    // for (let j = 0; j < INNER_ITERATIONS; j++) {
    //   let tmp = view.getBigUint64(0, true);
    //   view.setBigUint64(0, tmp + 1n, true);
    // }

    let end = view.getBigUint64(256, true);
    pointsDiff.push({ x: i, y: Number(end - start) });
    pointsAbs.push({ x: i, y: Number(end - totalStart) });
    updateProgress(i / ITERATIONS);
  }

  profiler_results.push(pointsAbs);
  profiler_chart_types.push("/plot/line/");

  profiler_names.push("Timer increments per clock edge");
  profiler_results.push(pointsDiff);
  profiler_chart_types.push("/plot/line/");

  nextProfiler("Memory latencies");
  profiler_times.push(profiler_times[profiler_times.length - 1]);
  if (stop) return;
  calculateMemoryLatencies(memory, clock);
}

async function calculateMemoryLatencies(memory, clock) {
  let finished = 0;
  let result = [];
  const resp2 = await fetch("/static/wasm/pagesize.wasm");
  const bin2 = await resp2.arrayBuffer();
  const module2 = new WebAssembly.Module(bin2);
  const finder1 = new Worker("/static/performance/memoryWorker.js");
  finder1.onmessage = function handle(evt) {
    let msg = evt.data;
    switch (msg.type) {
      case "progress":
        updateProgress(msg.value);
        break;
      case "terminate":
        finder1.terminate();
        break;
      case "results":
        result = result.concat(msg.points);
        // if (++finished == 2) {
        profiler_results.push(result);
        profiler_chart_types.push("/plot/hist/");

        nextProfiler("Load buffer size");
        if (stop) return;
        calculateLoadBufferSize(memory, clock);
        // }
        break;
      default:
    }
  };
  // const finder2 = new Worker("/static/performance/memoryWorker.js");
  // finder2.onmessage = function handle(evt) {
  //   let msg = evt.data;
  //   switch (msg.type) {
  //     case "progress":
  //       updateProgress(msg.value);
  //       break;
  //     case "terminate":
  //       finder2.terminate();
  //       break;
  //     case "results":
  //       result = result.concat(msg.points);
  //       if (++finished == 2) {
  //         profiler_results.push(result);
  //         profiler_chart_types.push("/plot/hist/");

  //         nextProfiler("Load buffer size");
  //         calculateLoadBufferSize(memory, clock);
  //       }
  //       break;
  //     default:
  //   }
  // };
  finder1.postMessage({ module: module2, memory: memory });
  // finder2.postMessage({ module: module2, memory: memory });
}
