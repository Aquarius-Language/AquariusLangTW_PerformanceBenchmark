"use strict";
const benchmark_n = 45;
let a = [], b = [];
for (let i = 0; i < benchmark_n; i++) {
  for (let j = 0; j < benchmark_n; j++) {
    const x = i + j, y = i * 2 + j;
    a = a.concat([x - Math.trunc(x / 7) * 7]);
    b = b.concat([y - Math.trunc(y / 5) * 5]);
  }
}
let checksum = 0;
for (let i = 0; i < benchmark_n; i++) {
  for (let j = 0; j < benchmark_n; j++) {
    let total = 0;
    for (let k = 0; k < benchmark_n; k++) total += a[i * benchmark_n + k] * b[k * benchmark_n + j];
    checksum += total;
  }
}
console.log("RESULT", checksum);
