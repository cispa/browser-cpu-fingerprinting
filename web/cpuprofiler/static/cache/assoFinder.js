// Constants
const P = 4096;
const KB = 1024;
const MB = 1024 * 1024;
const ITERATIONS = BigInt(MB * 64);
const RANDOM = true;
const MAXSIZE = 32;

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

  const sizes = [
    1 * KB,
    4 * KB,
    8 * KB,
    16 * KB,
    32 * KB,
    64 * KB,
    128 * KB,
    256 * KB,
    512 * KB,
    1 * MB,
    2 * MB,
  ];

  let points = [];

  for (let size = 1; size < MAXSIZE; size++) {
    prepareList(size, view);
    //console.log(instance.exports.check(START));
    instance.exports.iterate(START, ITERATIONS);
    let result = instance.exports.iterate(START, ITERATIONS);
    // log("Iteration " + size + " of " + MAXSIZE);
    postMessage({ type: "progress", value: size / MAXSIZE });
    points.push({ x: Number(size), y: Number(result) });
  }

  postMessage({ type: "progress", value: 1 });

  postMessage({ type: "results", points: points });

  postMessage({ type: "terminate" });
};

function prepareList(size, view) {
  // init [0, ... , 32 * KB * (size - 1)]
  let indices = [];
  for (let i = 0; i < size; i++) {
    indices.push(i * 32 * KB);
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
