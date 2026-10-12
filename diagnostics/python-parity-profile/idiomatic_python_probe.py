"""Measure separately labeled Python construction variants; preserve algorithms.

Fresh processes, one discarded warmup and five randomized samples per case.
Do not overwrite the published benchmark or its sources.
"""
import hashlib
import json
from pathlib import Path
import random
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from run_benchmarks import execute, summarize
from reference import expected


def main(output):
    manifest = json.loads((ROOT / "benchmarks.json").read_text(encoding="utf-8"))
    replacements = {
        "sieve": [("flags = []\n# Copy-and-append matches Aquarius push's allocation semantics.\nfor i in range(benchmark_n + 1):\n    flags = flags + [True]", "flags = [True] * (benchmark_n + 1)")],
        "quicksort": [("values = values + [seed]", "values.append(seed)")],
        "matrix": [("a = a + [x - (x // 7) * 7]", "a.append(x - (x // 7) * 7)"), ("b = b + [y - (y // 5) * 5]", "b.append(y - (y // 5) * 5)")],
    }
    cases = {}
    with tempfile.TemporaryDirectory(prefix="idiomatic-", dir=ROOT / ".benchmark-work") as stage:
        for name, substitutions in replacements.items():
            original = (ROOT / "benchmarks" / "python" / (name + ".py")).read_text(encoding="utf-8")
            idiomatic = original
            for old, new in substitutions:
                if idiomatic.count(old) != 1:
                    raise ValueError(f"Source changed: {name}")
                idiomatic = idiomatic.replace(old, new)
            for variant, source in [("copy_append", original), ("idiomatic", idiomatic)]:
                path = Path(stage) / (name + "_" + variant + ".py")
                path.write_text(source, encoding="utf-8")
                cases[name + "/" + variant] = {"benchmark": name, "variant": variant, "source": source,
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "command": [sys.executable, str(path)],
                    "warmups": [], "samples": []}
        rng = random.Random(20261013)
        for phase, count in [("warmups", 1), ("samples", 5)]:
            for round_number in range(1, count + 1):
                keys = list(cases)
                rng.shuffle(keys)
                for key in keys:
                    case = cases[key]
                    spec = manifest[case["benchmark"]]
                    sample = execute(case["command"], expected(case["benchmark"], spec["standard"]), spec, 120, stage)
                    sample["round"] = round_number
                    case[phase].append(sample)
        for key, case in cases.items():
            case["summary"] = summarize(case, 5)
            if case["summary"]["status"] != "ok":
                raise RuntimeError(f"Validation failed: {key}")
            print(f"{key}: {case['summary']['median_ms']:.4f} ms")
    Path(output).write_text(json.dumps({"method": __doc__, "python": sys.version,
        "seed": 20261013, "cases": cases}, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1])
