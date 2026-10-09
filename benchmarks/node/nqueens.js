"use strict";
const benchmark_n = 8;
let board = [];
for (let i = 0; i < benchmark_n; i++) board = board.concat([0]);
function solve(row) {
  if (row === benchmark_n) return 1;
  let count = 0;
  for (let col = 0; col < benchmark_n; col++) {
    let safe = true;
    for (let prev = 0; prev < row; prev++) {
      const delta = row - prev;
      if (board[prev] === col || board[prev] === col - delta || board[prev] === col + delta) { safe = false; break; }
    }
    if (safe) { board[row] = col; count += solve(row + 1); }
  }
  return count;
}
console.log("RESULT", solve(0));
