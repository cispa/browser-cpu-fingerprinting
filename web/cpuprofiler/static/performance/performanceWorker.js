let workerId = 0;

onmessage = function (event) {
  let data = event.data;
  workerId = data.workerId;

  benchmark(data.iterations);
};

function benchmark(iterations) {
  let points = [];
  for (let i = 0; i < iterations; i++) {
    counter = 0;
    start = performance.now() + 1;
    while (start > performance.now()) {
      counter += 1;
    }

    points.push({ x: Number(i), y: Number(counter) });
  }

  postMessage({ workerId: workerId, points: points });
}
