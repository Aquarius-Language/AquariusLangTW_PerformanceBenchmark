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
let checksum = 0;
for (let i = 0; i < 8; i++) {
  const tree = build(benchmark_n);
  checksum += check(tree, benchmark_n);
}
console.log("RESULT", checksum);
