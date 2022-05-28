async function calculatePerformance(CanvasJS) {
  document.getElementById("startButton").disabled = true;

  let points = [];

  let ITERATIONS = 500;
  let counter;
  let start;

  for (let i = 0; i < ITERATIONS; i++) {
    counter = 0;
    start = performance.now() + 1;
    while (start > performance.now()) {
      counter += 1;
    }

    points.push({ x: Number(i), y: Number(counter) });
  }

  updateProgress(1 / 3);

  await new Promise((r) => setTimeout(r, 100));

  for (let i = 0; i < ITERATIONS; i++) {
    counter = 0;
    start = performance.now() + 1;
    while (start > performance.now()) {
      counter += 1;
    }

    points.push({ x: Number(i + ITERATIONS), y: Number(counter) });
  }

  updateProgress(2 / 3);

  await new Promise((r) => setTimeout(r, 100));

  for (let i = 0; i < ITERATIONS; i++) {
    counter = 0;
    start = performance.now() + 1;
    while (start > performance.now()) {
      counter += 1;
    }

    points.push({ x: Number(i + ITERATIONS * 2), y: Number(counter) });
  }

  updateProgress(1);
  var chart = new CanvasJS.Chart("chartContainer", {
    animationEnabled: true,
    theme: "light2",
    data: [
      {
        type: "line",
        indexLabelFontSize: 16,
        dataPoints: points,
      },
    ],
  });
  chart.render();
}
