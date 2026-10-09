"use strict";
const benchmark_n = 60;
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
let u = [], v = [], temp = [];
for (let i = 0; i < benchmark_n; i++) {
  u = u.concat([1.0]); v = v.concat([0.0]); temp = temp.concat([0.0]);
}
for (let iteration = 0; iteration < 10; iteration++) {
  multiply(u, temp, false); multiply(temp, v, true);
  multiply(v, temp, false); multiply(temp, u, true);
}
let uv = 0.0, vv = 0.0;
for (let i = 0; i < benchmark_n; i++) { uv += u[i] * v[i]; vv += v[i] * v[i]; }
console.log("RESULT", uv / vv);
