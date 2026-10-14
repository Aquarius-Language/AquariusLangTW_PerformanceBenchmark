"use strict";
const benchmark_n = 10000;
const benchmark_start = process.hrtime.bigint();
let checksum = 0;
for (let start = 1; start <= benchmark_n; start++) {
  let value = start;
  while (value !== 1) {
    const half = Math.trunc(value / 2);
    if (half * 2 === value) value = half;
    else value = value * 3 + 1;
    checksum++;
  }
}
const benchmark_result = checksum;
const benchmark_elapsed_ms = Number(process.hrtime.bigint() - benchmark_start) / 1e6;
console.log("RESULT", benchmark_result);
console.log("ELAPSED_MS", benchmark_elapsed_ms);
