async function calculatePrecision(CanvasJS) {
  document.getElementById("startButton").disabled = true;

  // Shared memory
  memory = new WebAssembly.Memory({
    initial: amountOfPages,
    maximum: amountOfPages,
    shared: true,
  });

  const clock = await startClockWorker();

  const view = new DataView(memory.buffer);
  const ITERATIONS = 3;
  const INNER_ITERATIONS = 1000;
  let pointsDiff = [];
  let pointsAbs = [];

  await new Promise((r) => setTimeout(r, 1000));

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
    // pointsDiff.push({ x: i, y: Number(end - start) });
    // pointsAbs.push({ x: i, y: Number(end - totalStart) });
    pointsDiff.push({ y: Number(end - start), label: "Iteration " + i });
    updateProgress(i / ITERATIONS);
  }

  updateProgress(1);
  clock.terminate();

  var chartSmall = new CanvasJS.Chart("chartContainer", {
    animationEnabled: true,
    theme: "light2",
    data: [
      {
        type: "column",
        indexLabelFontSize: 16,
        dataPoints: pointsDiff,
      },
    ],
  });
  chartSmall.render();

  // var chartLarge = new CanvasJS.Chart("chartContainerLarge", {
  //   animationEnabled: true,
  //   theme: "light2",
  //   data: [
  //     {
  //       type: "line",
  //       indexLabelFontSize: 16,
  //       dataPoints: pointsAbs,
  //     },
  //   ],
  // });
  // chartLarge.render();
}
