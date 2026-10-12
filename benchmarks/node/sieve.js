"use strict";
const benchmark_n = 10000;
const benchmark_start = process.hrtime.bigint();
let flags = [];
// Copy-and-append matches Aquarius push's allocation semantics.
for (let i = 0; i <= benchmark_n; i++) flags = flags.concat([true]);
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
const benchmark_result = count;
const benchmark_elapsed_ms = Number(process.hrtime.bigint() - benchmark_start) / 1e6;
console.log("RESULT", benchmark_result);
console.log("ELAPSED_MS", benchmark_elapsed_ms);
