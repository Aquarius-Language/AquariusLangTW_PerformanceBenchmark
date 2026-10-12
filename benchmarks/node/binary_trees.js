"use strict";
const benchmark_n = 12;
function build(depth) {
  if (depth === 0) return [0, 0];
  return [build(depth - 1), build(depth - 1)];
}
function check(tree, depth) {
  if (depth === 0) return 1;
  return 1 + check(tree[0], depth - 1) + check(tree[1], depth - 1);
}
const benchmark_start = process.hrtime.bigint();
let checksum = 0;
for (let i = 0; i < 8; i++) {
  const tree = build(benchmark_n);
  checksum += check(tree, benchmark_n);
}
const benchmark_result = checksum;
const benchmark_elapsed_ms = Number(process.hrtime.bigint() - benchmark_start) / 1e6;
console.log("RESULT", benchmark_result);
console.log("ELAPSED_MS", benchmark_elapsed_ms);
