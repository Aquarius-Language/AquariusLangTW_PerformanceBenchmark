"use strict";
const benchmark_n = 28;
function fib(n) {
  if (n < 2) return n;
  return fib(n - 1) + fib(n - 2);
}
console.log("RESULT", fib(benchmark_n));
