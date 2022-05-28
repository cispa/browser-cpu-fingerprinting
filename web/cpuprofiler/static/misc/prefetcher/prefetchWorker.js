// Constants
const KB = 1024;
const MB = 1024 * 1024;
const MAXSIZE = 128 * MB;
const RANDOM = true;
const ENTRIES = KB;
const PAGESIZE = 4096;
const START = 512;
const FENCE = 200;

self.onmessage = async function start(evt) {
  // Prepare wasm instance
  const { module, memory } = evt.data;
  const instance = new WebAssembly.Instance(module, {
    env: { mem: memory },
    console: {
      log: function (arg) {
        console.log(arg);
      },
    },
  });

  const view = new DataView(memory.buffer);

  await new Promise((r) => setTimeout(r, 10)); // allow counter to start

  let points = [];
  let time = 0n;

  let indices = prepareList(ENTRIES, START, view);

  for (let i = 0; i < ENTRIES; i++) {
    time += instance.exports.maccess(indices[i], 16, FENCE);
    postMessage({ type: "progress", value: i / (ENTRIES * 3) });
  }

  points.push({ y: Number(time), label: "One cache line" });

  time = 0n;
  indices = prepareList(ENTRIES, START + ENTRIES * 256, view);

  for (let i = 0; i < ENTRIES; i++) {
    time += instance.exports.maccess(indices[i], 64, FENCE);
    postMessage({ type: "progress", value: (i + ENTRIES) / (ENTRIES * 3) });
  }

  points.push({ y: Number(time), label: "Two cache lines" });

  time = 0n;
  indices = prepareList(ENTRIES, START + ENTRIES * 256, view);

  for (let i = 0; i < ENTRIES; i++) {
    time += instance.exports.maccess(indices[i], 128, FENCE);
    postMessage({ type: "progress", value: (i + ENTRIES * 2) / (ENTRIES * 3) });
  }

  points.push({ y: Number(time), label: "Far cache lines" });

  postMessage({ type: "progress", value: 1 });

  postMessage({ type: "results", points: points });

  postMessage({ type: "terminate" });
};

function prepareList(size, start, view) {
  let indices = [];
  for (let i = 0; i < size; i++) {
    indices.push(i * 256);
  }

  // randomize indices
  if (RANDOM) {
    for (let i = 0; i < size; i++) {
      let j = i + getRandomInt(0, size - i - 1);
      // swap
      if (j != i) [indices[j], indices[i]] = [indices[i], indices[j]];
    }
  }

  indices = indices.map((x) => start + x);

  return indices;
}

function getRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}
