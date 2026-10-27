"use strict";
const benchmark_n = 80;
function benchmark_run() {
  let checksum = 0;
  for (let y = 0; y < benchmark_n; y++) {
    const ci = 2.0 * y / benchmark_n - 1.0;
    for (let x = 0; x < benchmark_n; x++) {
      const cr = 3.0 * x / benchmark_n - 2.0;
      let zr = 0.0, zi = 0.0, count = 0;
      while (count < 60 && zr * zr + zi * zi <= 4.0) {
        const next_r = zr * zr - zi * zi + cr;
        zi = 2.0 * zr * zi + ci; zr = next_r; count++;
      }
      checksum += count;
    }
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
