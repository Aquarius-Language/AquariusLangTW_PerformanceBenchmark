"use strict";
const benchmark_n = 60;
const benchmark_warmups = 0;
const benchmark_timed_runs = 1;
function element(i, j) {
  const s = i + j;
  return 1.0 / (Math.trunc(s * (s + 1) / 2) + i + 1);
}
function multiply(src, dst, transpose) {
  for (let i = 0; i < benchmark_n; i++) {
    let total = 0.0;
    for (let j = 0; j < benchmark_n; j++) {
      const coefficient = transpose ? element(j, i) : element(i, j);
      total += coefficient * src[j];
    }
    dst[i] = total;
  }
}
function benchmark_run() {
  const u = [], v = [], temp = [];
  for (let i = 0; i < benchmark_n; i++) { u.push(1.0); v.push(0.0); temp.push(0.0); }
  for (let iteration = 0; iteration < 10; iteration++) {
    multiply(u, temp, false); multiply(temp, v, true);
    multiply(v, temp, false); multiply(temp, u, true);
  }
  let uv = 0.0, vv = 0.0;
  for (let i = 0; i < benchmark_n; i++) { uv += u[i] * v[i]; vv += v[i] * v[i]; }
  return uv / vv;
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
