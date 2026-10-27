"use strict";
const benchmark_n = 6;
function ack(m, n) {
  if (m === 0) return n + 1;
  if (n === 0) return ack(m - 1, 1);
  return ack(m - 1, ack(m, n - 1));
}
function benchmark_run() {
  return ack(3, benchmark_n);
}
// Untimed warm-up runs, identical in every language.
for (let benchmark_warmup = 0; benchmark_warmup < 3; benchmark_warmup++) benchmark_run();
const benchmark_start = process.hrtime.bigint();
const benchmark_result = benchmark_run();
const benchmark_elapsed_ms = Number(process.hrtime.bigint() - benchmark_start) / 1e6;
console.log("RESULT", benchmark_result);
console.log("ELAPSED_MS", benchmark_elapsed_ms);
