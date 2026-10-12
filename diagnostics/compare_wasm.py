"""Compare the legacy VM with source and precompiled Wasm execution.

This diagnostic writes only to its own output directory; it leaves the published
benchmark README and latest.json untouched. Every sample starts a new process.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import random
import re
import statistics
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from reference import expected
from run_benchmarks import environment_info, execute, sha256


def fingerprint(executable):
    paths = [executable] + [executable.with_name(name) for name in (
        "AquariusLangVM.dll", "AquariusDesktopVMREPL.dll", "AquariusCore.dll",
        "AquariusDesktop.dll", "Wasmtime.Dotnet.dll")]
    return {str(path): sha256(path) for path in paths if path.is_file()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--legacy", required=True, type=Path)
    parser.add_argument("--wasm-cli", required=True, type=Path)
    parser.add_argument("--benchmarks", nargs="+")
    parser.add_argument("--repetitions", type=int, default=3)
    parser.add_argument("--warmups", type=int, default=1)
    parser.add_argument("--timeout", type=float, default=120)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    if args.repetitions < 1 or args.warmups < 0:
        parser.error("Require positive repetitions and nonnegative warmups")
    legacy = args.legacy.resolve(strict=True)
    cli = args.wasm_cli.resolve(strict=True)
    desktop = cli.with_name("AquariusDesktop.exe").resolve(strict=True)
    directory = args.output_dir.resolve()
    directory.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((ROOT / "benchmarks.json").read_text(encoding="utf-8"))
    names = args.benchmarks or list(manifest)
    report = {
        "started_at": datetime.now().astimezone().isoformat(),
        "environment": environment_info(),
        "config": {"repetitions": args.repetitions, "warmups": args.warmups,
                   "timeout_seconds": args.timeout, "seed": 20261010, "timing": "process"},
        "fingerprints": {"legacy": fingerprint(legacy), "wasm": fingerprint(cli)},
        "builds": {}, "cases": {}, "execution_order": [],
    }

    def save():
        (directory / "comparison.json").write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    for name in ["noop"] + names:
        source = directory / f"{name}.aqua"
        if name == "noop":
            text, answer, spec = '印出("RESULT", 0);\n', 0, {}
        else:
            spec = manifest[name]
            text = (ROOT / "benchmarks/aquarius" / f"{name}.aqua").read_text(encoding="utf-8")
            # Historical VM releases cannot call the new clock builtin. This
            # diagnostic deliberately compares whole-process startup and work.
            text = re.sub(r'^變數 benchmark_(?:start|elapsed_ms) = .*;\n', '', text, flags=re.M)
            text = re.sub(r'印出\("ELAPSED_MS", benchmark_elapsed_ms\);\s*', '', text)
            answer = expected(name, spec["standard"])
        source.write_text(text, encoding="utf-8")
        wasm = source.with_suffix(".wasm")
        command = [str(cli), "build", str(source), "--root", str(directory), "-o", str(wasm)]
        begin = time.perf_counter_ns()
        build = subprocess.run(command, cwd=directory, capture_output=True, text=True,
                               encoding="utf-8", timeout=args.timeout, stdin=subprocess.DEVNULL)
        report["builds"][name] = {"command": command,
            "elapsed_ms": (time.perf_counter_ns() - begin) / 1e6,
            "exit_code": build.returncode, "stdout": build.stdout, "stderr": build.stderr,
            "source_sha256": sha256(source)}
        if build.returncode:
            save()
            raise RuntimeError(f"Build failed for {name}: {build.stderr}")
        report["builds"][name]["wasm_sha256"] = sha256(wasm)
        for mode, cmd in {
            "legacy_source": [str(legacy), str(source)],
            "wasm_source": [str(desktop), str(source)],
            "wasm_precompiled": [str(cli), "run", str(wasm)],
        }.items():
            report["cases"][f"{name}/{mode}"] = {"command": cmd, "expected": answer,
                "spec": spec, "warmups": [], "samples": []}
        print(f"Built {name}: {wasm.stat().st_size} bytes", flush=True)
        save()
    rng = random.Random(20261010)
    for phase, rounds in [("warmups", args.warmups), ("samples", args.repetitions)]:
        for round_number in range(1, rounds + 1):
            keys = list(report["cases"])
            rng.shuffle(keys)
            for key in keys:
                case = report["cases"][key]
                sample = execute(case["command"], case["expected"], case["spec"], args.timeout, directory, timing="process")
                case[phase].append(sample)
                report["execution_order"].append({"case": key, "phase": phase, "round": round_number})
                print(f"{phase} {round_number}: {key}: {sample['status']} {sample['process_elapsed_ms']:.3f} ms", flush=True)
                save()
    for key, case in report["cases"].items():
        case["median_ms"] = statistics.median(s["process_elapsed_ms"] for s in case["samples"])
        case["valid"] = all(s["status"] == "ok" for phase in ["warmups", "samples"] for s in case[phase])
        print(f"{key}: median {case['median_ms']:.3f} ms, valid={case['valid']}", flush=True)
    report["finished_at"] = datetime.now().astimezone().isoformat()
    save()
    return 0 if all(c["valid"] for c in report["cases"].values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
