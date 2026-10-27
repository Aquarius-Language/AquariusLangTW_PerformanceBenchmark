"use strict";
const benchmark_n = 10000;
const benchmark_warmups = 0;
const benchmark_timed_runs = 1;
function benchmark_run() {
  const flags = [];
  for (let i = 0; i <= benchmark_n; i++) flags.push(true);
  flags[0] = false;
  flags[1] = false;
  let p = 2;
  while (p * p <= benchmark_n) {
    if (flags[p]) {
      let j = p * p;
      while (j <= benchmark_n) { flags[j] = false; j += p; }
    }
    p++;
  }
  let count = 0;
  for (let i = 2; i <= benchmark_n; i++) if (flags[i]) count++;
  return count;
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
