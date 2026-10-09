"use strict";
const benchmark_n = 2000;
let values = [], seed = 42;
for (let i = 0; i < benchmark_n; i++) {
  const raw = seed * 251 + 17;
  seed = raw - Math.trunc(raw / 65536) * 65536;
  values = values.concat([seed]);
}
function sort(a, lo, hi) {
  let i = lo, j = hi;
  const pivot = a[Math.trunc((lo + hi) / 2)];
  while (i <= j) {
    while (a[i] < pivot) i++;
    while (a[j] > pivot) j--;
    if (i <= j) {
      const tmp = a[i]; a[i] = a[j]; a[j] = tmp; i++; j--;
    }
  }
  if (lo < j) sort(a, lo, j);
  if (i < hi) sort(a, i, hi);
}
sort(values, 0, benchmark_n - 1);
let checksum = 0;
for (let i = 0; i < benchmark_n; i++) {
  if (i > 0 && values[i] < values[i - 1]) throw Error("Unsorted output");
  checksum += values[i] * (i + 1);
  checksum -= Math.trunc(checksum / 1000003) * 1000003;
}
console.log("RESULT", checksum);
