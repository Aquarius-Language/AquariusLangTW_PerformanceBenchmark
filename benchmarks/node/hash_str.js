"use strict";
const benchmark_n = 1000;
const benchmark_warmups = 0;
const benchmark_timed_runs = 1;
// Counts string keys in a hash: one read and one write per update, 1000 distinct keys.
function benchmark_run() {
  const keys = new Array(1000);
  for (let j = 0; j < 1000; j++) keys[j] = "key" + j;
  const counts = new Map();
  for (let i = 0; i < benchmark_n; i++) {
    const key = keys[i % 1000];
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return (counts.get("key7") ?? 0) * 1000 + counts.size;
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
