# CPU-Profiler

Mounting microarchitectural attacks, such as Spectre or Rowhammer, is possible from browsers. However, to be realistically exploitable, they require precise knowledge about microarchitectural properties. While a native attacker can easily query many of these properties, the sandboxed environment in browsers prevents this. In this paper, we present eight side-channel-related benchmarks that reveal CPU properties, such as cache sizes or cache associativities. Our benchmarks are implemented in JavaScript and run in unmodified browsers on multiple platforms. Based on a study with 834 participants using 297 different CPU models, we show that we can infer microarchitectural properties with an accuracy of up to 100%. Combining multiple properties also allows identifying the CPU vendor with an accuracy of 99%, and the microarchitecture and CPU model each with an accuracy of above 60%. The benchmarks are unaffected by current side-channel and browser fingerprinting mitigations, and can thus be used for more targeted attacks and to increase the entropy in browser fingerprinting.

## Server

The Django application is built using Bootstrap and CanvasJS. It serves the different profilers and was used to conduct our study.

### Quickstart

Create a `.env` file containing:

```
SECRET_KEY=<something>
REDEEM_SECRET=<something>
```

Then run:
`cd web && python3 manage.py runserver --nostatic`

### Structure

```
web/cpuprofiler/static/ - contains all profilers

web/navigation/         - contains all general pages that are served (e.g., home)
web/plot/               - contains endpoints to generate plots using matplotlib
web/profilers/          - contains all pages to showcase individual profilers
web/upload/             - contains an endpoint to upload the final results
```

## Profilers

`web/cpuprofiler/static/` contains all profilers.

### Structure

```
web/cpuprofiler/static/admin/       - can be ignored, as it only contains Django related files
web/cpuprofiler/static/vendor/      - can be ignored, as it only contains Bootstrap, jQuery and CanvasJS

web/cpuprofiler/static/all/         - contains scripts to run all profilers in a chain
web/cpuprofiler/static/utils/       - contains utility functions used by most profilers
web/cpuprofiler/static/wasm/        - contains WebAssembly code used by benchmarks (wat and wasm)

web/cpuprofiler/static/buffer/      - contains the loadbuffer benchmark and a first draft of a storebuffer benchmark
web/cpuprofiler/static/cache/       - contains the cache size and cache associativity benchmark
web/cpuprofiler/static/performance/ - contains the single- and multi-core performance benchmarks
web/cpuprofiler/static/tlb/         - contains the TLB size benchmark
web/cpuprofiler/static/misc/bits/       - contains a first draft of a 32-bit vs 64-bit benchmark
web/cpuprofiler/static/misc/cores/      - contains the cores benchmark
web/cpuprofiler/static/misc/pagesize/   - contains the pagesize benchmark
web/cpuprofiler/static/misc/prefetcher/ - contains the prefetcher benchmark
web/cpuprofiler/static/misc/timer/      - contains a timer evaluation benchmark of the SharedArrayBuffer-based timer
```

## Classification

```
classification/main.py                        - runs the classification on the normal data set
classification/noisy.py                       - runs the classification on the noisy data set
classification/pagesize.py                    - runs the classification for the pagesize

classification/benchmark_examples.ipynb       - showcases plots of individual benchmarks
classification/dataset_visualization.ipynb    - showcases the data sets used for classification

classification/utils/                         - contains utilities to load the data set from the database dumps
```

## Native

`native/` contains a variety of benchmark templates implemented in C and with some x86_64 inline assembly.
