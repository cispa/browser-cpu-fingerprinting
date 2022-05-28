// Constants
const P = 4096;
const KB = 1024;
const MB = 1024 * 1024;
//const ITERATIONS = BigInt(MB * 64);
const ITERATIONS = BigInt(MB * 16);
const RANDOM = true;

const START = 512;

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
  // Memory view
  const view = new DataView(memory.buffer);

  await new Promise((r) => setTimeout(r, 10)); // allow counter to start

  let points = [];
  prepareList(4 * MB, view);

  let ptr;
  for (let outer = 0; outer < 2; outer++) {
    ptr = START;
    for (let i = 0; i < MB; i++) {
      let result = instance.exports.maccess(ptr);
      ptr = view.getUint32(ptr, true);
      postMessage({
        type: "progress",
        value: (outer * MB + i) / (MB * 2),
      });
      if (i % 128 == 0) points.push(Number(result));
    }
  }

  postMessage({ type: "progress", value: 1 });

  postMessage({ type: "results", points: points });

  postMessage({ type: "terminate" });
};

function prepareList(size, view) {
  // init [0, ... , size - 1]
  let indices = [];
  for (let i = 0; i < size; i++) {
    indices.push(i);
  }

  // randomize indices
  if (RANDOM) {
    for (let i = 0; i < size; i++) {
      let j = i + getRandomInt(0, size - i - 1);
      // swap
      if (j != i) [indices[j], indices[i]] = [indices[i], indices[j]];
    }
  }

  // index to address conversion
  indices = indices.map((x) => START + x * 4);

  // write linked list to memory
  for (let i = 1; i < size; i++) {
    view.setUint32(indices[i - 1], indices[i], true);
  }
  view.setUint32(indices[size - 1], indices[0], true);
}

function getRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}
