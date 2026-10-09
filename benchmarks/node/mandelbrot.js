"use strict";
const benchmark_n = 80;
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
console.log("RESULT", checksum);
