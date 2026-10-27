"use strict";
const benchmark_n = 28;
function fib(n) {
  if (n < 2) return n;
  return fib(n - 1) + fib(n - 2);
}
function benchmark_run() {
  return fib(benchmark_n);
}
// Untimed warm-up runs, identical in every language.
for (let benchmark_warmup = 0; benchmark_warmup < 3; benchmark_warmup++) benchmark_run();
const benchmark_start = process.hrtime.bigint();
const benchmark_result = benchmark_run();
const benchmark_elapsed_ms = Number(process.hrtime.bigint() - benchmark_start) / 1e6;
console.log("RESULT", benchmark_result);
console.log("ELAPSED_MS", benchmark_elapsed_ms);
