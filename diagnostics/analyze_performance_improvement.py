"""Validate the final evidence and derive before/after diagnostic statistics."""
import json
import math
from pathlib import Path
import random
import statistics
import sys
import xml.etree.ElementTree as ET


def analyze(directory):
    root = Path(directory)
    def read(file):
        return json.loads((root / file).read_text(encoding="utf-8-sig"))
    paired = read("paired.json")
    before, after = read("before/latest.json"), read("after/latest.json")
    warm_before, warm_after = read("warm-before.json"), read("warm-after.json")
    assert paired["valid"] and len(paired["cases"]) == 40
    for report in [before, after, paired]:
        assert all(c["summary"]["status"] == "ok" for c in report["cases"].values())
        assert all(len(c["samples"]) == 7 and len(c["warmups"]) == 1 for c in report["cases"].values())
    for name in paired["benchmarks"]:
        assert paired["cases"][name + "/before"]["source_sha256"] == paired["cases"][name + "/after"]["source_sha256"]
        for variant, standard, warm in [("before", before, warm_before), ("after", after, warm_after)]:
            for assembly in ["AquariusCore.dll", "AquariusDesktop.dll", "Wasmtime.Dotnet.dll", "wasmtime.dll"]:
                assert warm["fingerprints"][assembly] == paired["runtimes"][variant]["assemblies_sha256"][assembly]
            assert standard["cases"][name + "/aquarius"]["source_sha256"] == warm["results"][name]["source_sha256"]
            assert warm["results"][name]["valid"] and len(warm["results"][name]["samples"]) == 7
    tests = {}
    ns = {"t": "http://microsoft.com/schemas/VisualStudio/TeamTest/2010"}
    for file in ["before.trx", "after-full.trx", "performance-tests.trx"]:
        counters = ET.parse(root / "tests" / file).find(".//t:Counters", ns).attrib
        assert counters["failed"] == "0"
        tests[file] = {k: int(counters[k]) for k in ["total", "executed", "passed", "failed"]}
    for file in ["desktop-examples.json", "browser-smoke.json"]:
        rows = read(file)
        assert all(row["passed"] for row in rows)
        tests[file] = {"passed": len(rows), "failed": 0}
    gm = lambda numbers: math.exp(statistics.mean(math.log(x) for x in numbers))
    rng = random.Random(20261013)
    estimates = []
    # Descriptive resampling interval; it does not model thermal or scheduling drift.
    for _ in range(2000):
        ratios = []
        for name in paired["benchmarks"]:
            a = [s["elapsed_ms"] for s in paired["cases"][name + "/before"]["samples"]]
            b = [s["elapsed_ms"] for s in paired["cases"][name + "/after"]["samples"]]
            ratios.append(statistics.median(rng.choices(a, k=len(a))) / statistics.median(rng.choices(b, k=len(b))))
        estimates.append(gm(ratios))
    estimates.sort()
    result = {"paired_speedup": paired["geometric_mean_speedup"],
        "paired_speedup_bootstrap_95_percent": [estimates[49], estimates[1949]],
        "paired_before_over_python": paired["before_over_python"], "paired_after_over_python": paired["after_over_python"],
        "after_time_reduction_percent": (1 - 1 / paired["geometric_mean_speedup"]) * 100,
        "further_time_reduction_for_python_parity_percent": (1 - 1 / paired["after_over_python"]) * 100,
        "cases": paired["comparison"], "tests": tests,
        "warm_execute_geometric_speedup": gm([statistics.median(s["execute_ms"] for s in warm_before["results"][name]["samples"]) / statistics.median(s["execute_ms"] for s in warm_after["results"][name]["samples"]) for name in paired["benchmarks"]]),
        "historical_diagnostic": "The earlier 3.395x Python slowdown used an older build and a separate run; it is not the baseline credited to this patch."}
    (root / "analysis.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k not in {"cases", "tests"}}, indent=2))


if __name__ == "__main__":
    analyze(sys.argv[1])
