"""Interleave preserved/new Aquarius, CPython and Node samples without changing algorithms."""
import argparse
import csv
from datetime import datetime, timedelta, timezone
import json
import math
from pathlib import Path
import random
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from run_benchmarks import environment_info, execute, resolve_executable, runtime_info, sha256, summarize
from reference import expected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--before", required=True)
    parser.add_argument("--after", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repetitions", type=int, default=7)
    args = parser.parse_args()
    if args.repetitions < 1:
        parser.error("repetitions must be positive")
    executables = {"before": resolve_executable(args.before, []), "after": resolve_executable(args.after, []),
        "python": sys.executable, "node": resolve_executable(None, ["node"])}
    if not all(executables.values()):
        raise RuntimeError("A required executable is unavailable")
    manifest = json.loads((ROOT / "benchmarks.json").read_text(encoding="utf-8"))
    clock = timezone(timedelta(hours=8), "Asia/Taipei")
    report = {"started_at": datetime.now(clock).isoformat(), "method": __doc__,
        "config": {"repetitions": args.repetitions, "warmups": 1, "seed": 20261013,
            "timing": "in-process", "aquarius_mode": "precompiled", "profile": "standard"},
        "environment": environment_info(), "runtimes": {name: runtime_info("aquarius" if name in {"before", "after"} else name, exe) for name, exe in executables.items()},
        "benchmarks": {}, "cases": {}, "execution_order": [], "harness_sha256": sha256(__file__)}
    rng = random.Random(20261013)
    with tempfile.TemporaryDirectory(prefix="paired-performance-", dir=ROOT / ".benchmark-work") as directory:
        stage = Path(directory)
        for name, spec in manifest.items():
            answer = expected(name, spec["standard"])
            report["benchmarks"][name] = {**spec, "n": spec["standard"], "expected": answer}
            for variant, language, extension in [("before", "aquarius", ".aqua"), ("after", "aquarius", ".aqua"), ("python", "python", ".py"), ("node", "node", ".js")]:
                source = ROOT / "benchmarks" / language / (name + extension)
                target = stage / variant / source.name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
                command = [executables[variant], str(target)]
                case = {"benchmark": name, "variant": variant, "source_sha256": sha256(source), "staged_sha256": sha256(target), "warmups": [], "samples": []}
                if language == "aquarius":
                    wasm = target.with_suffix(".wasm")
                    build_command = [executables[variant], "build", str(target), "--root", str(target.parent), "-o", str(wasm)]
                    built = subprocess.run(build_command, cwd=stage, capture_output=True, text=True, encoding="utf-8", timeout=120, stdin=subprocess.DEVNULL)
                    if built.returncode != 0 or not wasm.is_file():
                        raise RuntimeError(f"Build failed for {name}/{variant}: {built.stderr}")
                    case["build_command"] = build_command
                    case["wasm_sha256"] = sha256(wasm)
                    command = [executables[variant], "run", str(wasm)]
                case["command"] = command
                report["cases"][name + "/" + variant] = case
        for phase, count in [("warmups", 1), ("samples", args.repetitions)]:
            for round_number in range(1, count + 1):
                keys = list(report["cases"])
                rng.shuffle(keys)
                for key in keys:
                    case = report["cases"][key]
                    spec = report["benchmarks"][case["benchmark"]]
                    sample = execute(case["command"], spec["expected"], spec, 120, stage)
                    sample["round"] = round_number
                    case[phase].append(sample)
                    report["execution_order"].append({"case": key, "phase": phase, "round": round_number})
                print(f"{phase} round {round_number}/{count} completed", flush=True)
        for case in report["cases"].values():
            case["summary"] = summarize(case, args.repetitions)
    report["finished_at"] = datetime.now(clock).isoformat()
    valid = all(c["summary"]["status"] == "ok" for c in report["cases"].values())
    report["valid"] = valid
    if valid:
        medians = {name: {variant: report["cases"][name + "/" + variant]["summary"]["median_ms"] for variant in executables} for name in manifest}
        report["comparison"] = {name: {**values, "speedup": values["before"] / values["after"], "after_over_python": values["after"] / values["python"]} for name, values in medians.items()}
        gm = lambda values: math.exp(sum(math.log(x) for x in values) / len(manifest))
        report["geometric_mean_speedup"] = gm([v["speedup"] for v in report["comparison"].values()])
        report["after_over_python"] = gm([v["after_over_python"] for v in report["comparison"].values()])
        report["before_over_python"] = gm([v["before"] / v["python"] for v in medians.values()])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if valid:
        with args.output.with_suffix(".csv").open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=["benchmark", "before", "after", "python", "node", "speedup", "after_over_python"])
            writer.writeheader()
            for name, row in report["comparison"].items():
                writer.writerow({"benchmark": name, **row})
        print(f"Validated all cases. Geometric speedup: {report['geometric_mean_speedup']:.3f}x; after/Python time: {report['after_over_python']:.3f}x")
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
