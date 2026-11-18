"use strict";
const benchmark_n = 1000;
const benchmark_warmups = 0;
const benchmark_timed_runs = 1;
// Appends to a string that a closure can also see.
function benchmark_run() {
  let text = "";
  const size = () => text.length;
  for (let i = 0; i < benchmark_n; i++) text = text + "ab,";
  return size();
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
