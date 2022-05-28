const ITERATIONS = 8192 * 4;
const P1 = 512 + 128 * 120;
const P2 = P1 + ITERATIONS * 16;
const RANDOM = true;
const INNER_ITERATIONS = 128;
const WARMUP = 12000;

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

  prepareList(ITERATIONS * 2, view, P1);
  prepareList(ITERATIONS * 2, view, P2);

  for (let i = 0; i < WARMUP; i++) instance.exports.routine(P1, P2, 20);

  prepareList(ITERATIONS * 2, view, P1);
  prepareList(ITERATIONS * 2, view, P2);
  let result = 0n;
  for (let i = 0; i < INNER_ITERATIONS; i++)
    result += instance.exports.routine(P1, P2, ITERATIONS);

  postMessage({ type: "result", result: result / BigInt(INNER_ITERATIONS) });
};

function prepareList(size, view, start) {
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
  indices = indices.map((x) => start + x * 4);

  // write linked list to memory
  for (let i = 1; i < size; i++) {
    view.setUint32(indices[i - 1], indices[i], true);
  }
  view.setUint32(indices[size - 1], indices[0], true);
}

function getRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}
