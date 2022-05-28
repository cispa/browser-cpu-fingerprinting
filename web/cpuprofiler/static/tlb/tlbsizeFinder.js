// Constants
const KB = 1024;
const MB = 1024 * 1024;
const MAXSIZE = 128;
const RANDOM = false;
const ITERATIONS = 32 * MB;
const PAGESIZE = 4096;
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

  const view = new DataView(memory.buffer);

  await new Promise((r) => setTimeout(r, 10)); // allow counter to start

  let points = [];

  for (let size = 2; size < MAXSIZE; size += 4) {
    prepareList(size, view);

    let time = instance.exports.iterate(START, BigInt(ITERATIONS));

    postMessage({ type: "progress", value: size / MAXSIZE });
    points.push({ x: Number(size), y: Number(time) });
  }

  postMessage({ type: "progress", value: 1 });

  postMessage({ type: "results", points: points });

  postMessage({ type: "terminate" });
};

function prepareList(size, view) {
  let indices = [];
  for (let i = 0; i < size; i++) {
    indices.push(i * PAGESIZE);
  }

  // randomize indices
  if (RANDOM) {
    for (let i = 0; i < size; i++) {
      let j = i + getRandomInt(0, size - i - 1);
      // swap
      if (j != i) [indices[j], indices[i]] = [indices[i], indices[j]];
    }
  }

  indices = indices.map((x) => START + x);

  // write linked list to memory
  for (let i = 1; i < size; i++) {
    view.setUint32(indices[i - 1], indices[i], true);
  }
  view.setUint32(indices[size - 1], indices[0], true);
}

function getRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}
