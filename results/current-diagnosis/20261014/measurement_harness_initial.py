"""Compare current Aquarius scripts with idiomatic Python and a helper-inlining probe.

Preserves the published suite, README and latest.json. All variants retain the
algorithms and reference checksums. Each sample is a fresh process; compilation,
startup and printing are outside the workload timer. Inlining changes both call
handling and binding locality, so its speedup is not a pure call-cost measurement.
"""
import argparse
from datetime import datetime, timedelta, timezone
import json
import math
from pathlib import Path
import random
import statistics
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from reference import expected
from run_benchmarks import environment_info, execute, runtime_info, sha256, summarize


def replace_once(source, old, new):
    if source.count(old) != 1:
        raise ValueError(f"Source changed: expected one occurrence of {old!r}")
    return source.replace(old, new)


def idiomatic_python(name, source):
    replacements = {
        "sieve": [("flags = []\n# Copy-and-append matches Aquarius push's allocation semantics.\n"
                   "for i in range(benchmark_n + 1):\n    flags = flags + [True]",
                   "flags = [True] * (benchmark_n + 1)")],
        "quicksort": [("values = values + [seed]", "values.append(seed)")],
        "matrix": [("a = a + [x - (x // 7) * 7]", "a.append(x - (x // 7) * 7)"),
                   ("b = b + [y - (y // 5) * 5]", "b.append(y - (y // 5) * 5)")],
    }
    for old, new in replacements.get(name, []):
        source = replace_once(source, old, new)
    return source


def inline_spectral(source):
    return replace_once(source,
        "如果 (transpose) { coefficient = element(j, i); } 否則 { coefficient = element(i, j); }",
        "變數 s = i + j;\n"
        "            如果 (transpose) { coefficient = 1.0d / (s * (s + 1) / 2 + j + 1); } "
        "否則 { coefficient = 1.0d / (s * (s + 1) / 2 + i + 1); }")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--aquarius", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repetitions", type=int, default=7)
    args = parser.parse_args()
    if args.repetitions < 1:
        parser.error("repetitions must be positive")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.output.exists():
        parser.error("output already exists; select a new filename")
    executable = str(args.aquarius.resolve())
    specs = json.loads((ROOT / "benchmarks.json").read_text(encoding="utf-8"))
    clock = timezone(timedelta(hours=8), "Asia/Taipei")
    report = {
        "method": __doc__, "started_at": datetime.now(clock).isoformat(),
        "config": {"repetitions": args.repetitions, "warmups": 1, "seed": 20261014},
        "environment": environment_info(), "runtimes": {
            "aquarius": runtime_info("aquarius", executable),
            "python": runtime_info("python", sys.executable)},
        "harness_sha256": sha256(__file__), "cases": {}, "execution_order": []}
    with tempfile.TemporaryDirectory(prefix="current-diagnosis-", dir=ROOT / ".benchmark-work") as directory:
        stage = Path(directory)
        for name, spec in specs.items():
            aqua = (ROOT / "benchmarks" / "aquarius" / (name + ".aqua")).read_text(encoding="utf-8")
            py = (ROOT / "benchmarks" / "python" / (name + ".py")).read_text(encoding="utf-8")
            variants = [("aquarius", "aquarius", aqua),
                        ("python_idiomatic", "python", idiomatic_python(name, py))]
            if name in ("sieve", "quicksort", "matrix"):
                variants.append(("python_original", "python", py))
            if name == "spectral_norm":
                variants.append(("aquarius_inlined", "aquarius", inline_spectral(aqua)))
            for variant, language, source in variants:
                folder = stage / variant
                folder.mkdir(exist_ok=True)
                path = folder / (name + (".aqua" if language == "aquarius" else ".py"))
                path.write_text(source, encoding="utf-8")
                case = {"benchmark": name, "variant": variant, "language": language,
                        "source": source, "source_sha256": sha256(path),
                        "warmups": [], "samples": []}
                if language == "aquarius":
                    wasm = path.with_suffix(".wasm")
                    command = [executable, "build", str(path), "--root", str(folder), "-o", str(wasm)]
                    built = subprocess.run(command, cwd=stage, capture_output=True, text=True,
                                           encoding="utf-8", timeout=120, stdin=subprocess.DEVNULL)
                    if built.returncode != 0 or not wasm.is_file():
                        raise RuntimeError(f"Build failed {name}/{variant}: {built.stdout} {built.stderr}")
                    case.update(build_command=command, wasm_sha256=sha256(wasm))
                    command = [executable, "run", str(wasm)]
                else:
                    command = [sys.executable, str(path)]
                case["command"] = command
                report["cases"][name + "/" + variant] = case
        rng = random.Random(20261014)
        for phase, count in [("warmups", 1), ("samples", args.repetitions)]:
            for round_number in range(1, count + 1):
                keys = list(report["cases"])
                rng.shuffle(keys)
                for key in keys:
                    case = report["cases"][key]
                    spec = specs[case["benchmark"]]
                    sample = execute(case["command"], expected(case["benchmark"], spec["standard"]),
                                     spec, 120, stage)
                    sample["round"] = round_number
                    case[phase].append(sample)
                    report["execution_order"].append({"case": key, "phase": phase, "round": round_number})
                print(f"{phase} round {round_number}/{count} complete", flush=True)
        for case in report["cases"].values():
            case["summary"] = summarize(case, args.repetitions)
        report["finished_at"] = datetime.now(clock).isoformat()
        args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        if any(case["summary"]["status"] != "ok" for case in report["cases"].values()):
            raise RuntimeError("Validation failed; inspect the saved report")
        ratios = []
        for name in specs:
            a = report["cases"][name + "/aquarius"]["summary"]["median_ms"]
            p = report["cases"][name + "/python_idiomatic"]["summary"]["median_ms"]
            ratios.append(a / p)
            print(f"{name}: Aquarius {a:.4f} ms, idiomatic Python {p:.4f} ms, ratio {a/p:.3f}")
        print(f"Geometric mean Aquarius/idiomatic Python: {math.exp(statistics.mean(map(math.log, ratios))):.4f}")


if __name__ == "__main__":
    main()
