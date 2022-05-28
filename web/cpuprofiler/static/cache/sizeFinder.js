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
  const { module, memory, large } = evt.data;
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

  let sizes = [1 * KB];

  for (let i = 4; i < 513; i += 4) sizes.push(i * KB);

  sizes.push(Number(1 * MB));

  if (large) {
    for (let i = 2; i < 33; i += 2) sizes.push(Number(i * MB));
  }

  let points = [];

  for (let i = 0; i < sizes.length; i++) {
    prepareList(sizes[i] / 4, view);
    instance.exports.iterate(START, ITERATIONS);
    let result = instance.exports.iterate(START, ITERATIONS);
    postMessage({ type: "progress", value: i / sizes.length });
    points.push({ x: Number(sizes[i]), y: Number(result) });
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
