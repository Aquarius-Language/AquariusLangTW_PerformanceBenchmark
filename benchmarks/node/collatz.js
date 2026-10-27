"use strict";
const benchmark_n = 10000;
const benchmark_warmups = 0;
const benchmark_timed_runs = 1;
function benchmark_run() {
  let checksum = 0;
  for (let start = 1; start <= benchmark_n; start++) {
    let value = start;
    while (value !== 1) {
      const half = Math.trunc(value / 2);
      if (half * 2 === value) value = half;
      else value = value * 3 + 1;
      checksum++;
    }
  }
  return checksum;
}
// Untimed in-process warm-up runs, then timed runs; the harness substitutes both counts.
for (let benchmark_warmup = 0; benchmark_warmup < benchmark_warmups; benchmark_warmup++) benchmark_run();
for (let benchmark_round = 0; benchmark_round < benchmark_timed_runs; benchmark_round++) {
  const benchmark_start = process.hrtime.bigint();
  const benchmark_result = benchmark_run();
  const benchmark_elapsed_ms = Number(process.hrtime.bigint() - benchmark_start) / 1e6;
  console.log("RESULT", benchmark_result);
  console.log("ELAPSED_MS", benchmark_elapsed_ms);
}
