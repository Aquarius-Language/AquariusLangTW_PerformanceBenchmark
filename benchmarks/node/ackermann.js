"use strict";
const benchmark_n = 6;
function ack(m, n) {
  if (m === 0) return n + 1;
  if (n === 0) return ack(m - 1, 1);
  return ack(m - 1, ack(m, n - 1));
}
console.log("RESULT", ack(3, benchmark_n));
