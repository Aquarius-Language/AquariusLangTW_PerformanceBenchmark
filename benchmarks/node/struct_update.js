"use strict";
const benchmark_n = 1000;
const benchmark_warmups = 0;
const benchmark_timed_runs = 1;
// Updates 1000 struct particles through a step function, n calls in all.
class Particle { constructor(x, v) { this.x = x; this.v = v; } }
function step(p) {
  p.x = (p.x + p.v) % 10007;
  return p.x;
}
function benchmark_run() {
  const particles = new Array(1000);
  for (let j = 0; j < 1000; j++) particles[j] = new Particle(j, j % 17 + 1);
  let total = 0;
  for (let i = 0; i < benchmark_n; i++) total = (total + step(particles[i % 1000])) % 1000003;
  return total;
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
