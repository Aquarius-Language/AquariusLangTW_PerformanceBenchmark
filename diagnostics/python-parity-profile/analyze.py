"""Derive diagnostic medians and ratios from the preserved raw measurements."""
import json
import math
from pathlib import Path
import statistics
import sys


def analyze(directory):
    root = Path(directory)
    def read(name):
        return json.loads((root / name).read_text(encoding="utf-8"))
    baseline, warm, variants = read("latest.json"), read("warm-profile.json"), read("idiomatic-python.json")
    for assembly in ["AquariusCore.dll", "AquariusDesktop.dll", "Wasmtime.Dotnet.dll"]:
        assert warm["fingerprints"][assembly] == baseline["runtimes"]["aquarius"]["assemblies_sha256"][assembly]
    metrics = {"baseline": {}, "warm": {}, "tuning": {}, "typed": {}, "idiomatic_python": {}}
    ratios = []
    for name in baseline["benchmarks"]:
        aquarius = baseline["cases"][name + "/aquarius"]["summary"]
        python = baseline["cases"][name + "/python"]["summary"]
        assert aquarius["status"] == python["status"] == "ok"
        a, p = aquarius["median_ms"], python["median_ms"]
        ratios.append(a / p)
        metrics["baseline"][name] = {"aquarius_ms": a, "python_ms": p,
            "aquarius_over_python": a / p, "reduction_to_parity_percent": max(0, 1 - p / a) * 100}
    for name, case in warm["results"].items():
        assert case["valid"]
        # The API compiler names its module main.aqua; CLI packaging uses the
        # source filename. Whole-module hashes therefore differ in metadata.
        assert case["source_sha256"] == baseline["cases"][name + "/aquarius"]["source_sha256"]
        metrics["warm"][name] = {
            "workload_median_ms": statistics.median(s["workload_ms"] for s in case["samples"]),
            "managed_allocated_bytes_median": statistics.median(s["managed_allocated_bytes"] for s in case["samples"]),
            **{field: case[field] for field in ["guest_heap_high_water_bytes", "native_calls", "scheduler_entries", "explicit_host_collection_calls"]}}
    for name in ["collatz", "fibonacci", "binary_trees", "spectral_norm", "matrix", "mandelbrot"]:
        unchanged = warm["tuning_probes"][name + "/unchanged"]
        tuned = warm["tuning_probes"][name + "/budget_65536"]
        assert unchanged["valid"] and tuned["valid"]
        a, b = statistics.median(unchanged["workload_ms"]), statistics.median(tuned["workload_ms"])
        metrics["tuning"][name] = {"baseline_4096_ms": a, "budget_65536_ms": b, "speedup": a / b}
    for name, case in warm["typed_probes"].items():
        assert case["valid"]
        median = statistics.median(case["elapsed_ms"])
        metrics["typed"][name] = {"median_ms": median,
            "generic_over_typed": metrics["warm"][name]["workload_median_ms"] / median,
            "python_over_typed": metrics["baseline"][name]["python_ms"] / median}
    for name in ["sieve", "quicksort", "matrix"]:
        original = variants["cases"][name + "/copy_append"]["summary"]
        idiomatic = variants["cases"][name + "/idiomatic"]["summary"]
        assert original["status"] == idiomatic["status"] == "ok"
        a, b = original["median_ms"], idiomatic["median_ms"]
        metrics["idiomatic_python"][name] = {"copy_append_ms": a, "idiomatic_ms": b,
            "speedup": a / b, "aquarius_baseline_over_idiomatic": metrics["baseline"][name]["aquarius_ms"] / b}
    metrics["baseline_geometric_mean_slowdown"] = math.exp(statistics.mean(map(math.log, ratios)))
    metrics["baseline_geometric_mean_reduction_percent"] = (1 - 1 / metrics["baseline_geometric_mean_slowdown"]) * 100
    metrics["geometric_mean_if_worst_three_reached_parity"] = math.exp(sum(math.log(x) for x in sorted(ratios)[:-3]) / 10)
    (root / "analysis.json").write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    for group in ["warm", "tuning", "typed", "idiomatic_python"]:
        print(group, json.dumps(metrics[group], indent=2))


if __name__ == "__main__":
    analyze(sys.argv[1])
