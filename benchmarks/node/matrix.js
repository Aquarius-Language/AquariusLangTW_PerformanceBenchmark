"use strict";
const benchmark_n = 45;
const benchmark_warmups = 0;
const benchmark_timed_runs = 1;
function benchmark_run() {
  const a = [], b = [];
  for (let i = 0; i < benchmark_n * benchmark_n; i++) { a.push(0); b.push(0); }
  for (let i = 0; i < benchmark_n; i++) {
    for (let j = 0; j < benchmark_n; j++) {
      const x = i + j, y = i * 2 + j;
      a[i * benchmark_n + j] = x - Math.trunc(x / 7) * 7;
      b[i * benchmark_n + j] = y - Math.trunc(y / 5) * 5;
    }
  }
  let checksum = 0;
  for (let i = 0; i < benchmark_n; i++) {
    for (let j = 0; j < benchmark_n; j++) {
      let total = 0;
      for (let k = 0; k < benchmark_n; k++) total += a[i * benchmark_n + k] * b[k * benchmark_n + j];
      checksum += total;
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
