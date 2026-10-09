"use strict";
const benchmark_n = 10000;
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
console.log("RESULT", checksum);
