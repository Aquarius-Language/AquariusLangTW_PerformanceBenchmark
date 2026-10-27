"use strict";
const benchmark_n = 2000;
function sort(a, lo, hi) {
  let i = lo, j = hi;
  const pivot = a[Math.trunc((lo + hi) / 2)];
  while (i <= j) {
    while (a[i] < pivot) i++;
    while (a[j] > pivot) j--;
    if (i <= j) {
      const tmp = a[i]; a[i] = a[j]; a[j] = tmp; i++; j--;
    }
  }
  if (lo < j) sort(a, lo, j);
  if (i < hi) sort(a, i, hi);
}
function benchmark_run() {
  const values = [];
  let seed = 42;
  for (let i = 0; i < benchmark_n; i++) {
    const raw = seed * 251 + 17;
    seed = raw - Math.trunc(raw / 65536) * 65536;
    values.push(seed);
  }

  sort(values, 0, benchmark_n - 1);
  let checksum = 0;
  for (let i = 0; i < benchmark_n; i++) {
    if (i > 0 && values[i] < values[i - 1]) throw Error("Unsorted output");
    checksum += values[i] * (i + 1);
    checksum -= Math.trunc(checksum / 1000003) * 1000003;
  }
  return checksum;
}
// Untimed warm-up runs, identical in every language.
for (let benchmark_warmup = 0; benchmark_warmup < 3; benchmark_warmup++) benchmark_run();
const benchmark_start = process.hrtime.bigint();
const benchmark_result = benchmark_run();
const benchmark_elapsed_ms = Number(process.hrtime.bigint() - benchmark_start) / 1e6;
console.log("RESULT", benchmark_result);
console.log("ELAPSED_MS", benchmark_elapsed_ms);
