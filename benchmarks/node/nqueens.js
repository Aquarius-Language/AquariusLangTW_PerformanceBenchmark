"use strict";
const benchmark_n = 8;
const benchmark_warmups = 0;
const benchmark_timed_runs = 1;
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
const board = [];
for (let i = 0; i < benchmark_n; i++) board.push(0);
function benchmark_run() {
  return solve(0);
}
// Untimed in-process warm-up runs, then timed runs; the harness substitutes both counts.
for (let benchmark_warmup = 0; benchmark_warmup < benchmark_warmups; benchmark_warmup++) benchmark_run();
for (let benchmark_round = 0; benchmark_round < benchmark_timed_runs; benchmark_round++) {
  const benchmark_start = process.hrtime.bigint();
  const benchmark_result = benchmark_run();
  const benchmark_elapsed_ms = Number(process.hrtime.bigint() - benchmark_start) / 1e6;
  console.log("RESULT", benchmark_result);
  console.log("ELAPSED_MS", benchmark_elapsed_ms);
}
