// Constants
const KB = 1024;
const MB = 1024 * 1024;
const MAXSIZE = MB + 100;

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

  await new Promise((r) => setTimeout(r, 10)); // allow counter to start

  let points = [];

  for (let size = 0; START + size * 4 < MAXSIZE; size++) {
    let result = instance.exports.maccess(START + size * 4);
    postMessage({ type: "progress", value: size / (MAXSIZE - START) });
    points.push({ x: Number(START + size * 4), y: Number(result) });
  }

  postMessage({ type: "progress", value: 1 });

  postMessage({ type: "results", points: points });

  postMessage({ type: "terminate" });
};
