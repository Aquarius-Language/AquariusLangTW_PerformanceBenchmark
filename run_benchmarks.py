"""Standard-library-only desktop benchmark harness and README generator (Python 3.10+)."""
from __future__ import annotations

import argparse
import csv
import ctypes
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import random
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from reference import expected

ROOT = Path(__file__).resolve().parent
LANGUAGES = {"aquarius": ("AquariusLang", ".aqua"), "python": ("Python", ".py"),
             "node": ("Node.js", ".js")}


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def command_output(command):
    try:
        proc = subprocess.run(command, capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=10, stdin=subprocess.DEVNULL)
        return proc.stdout.strip() if proc.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def search_path():
    paths = [os.environ.get("PATH", "")]
    if os.name == "nt":
        import winreg
        for hive, key in [(winreg.HKEY_CURRENT_USER, "Environment"),
                          (winreg.HKEY_LOCAL_MACHINE,
                           r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment")]:
            try:
                with winreg.OpenKey(hive, key) as handle:
                    paths.append(os.path.expandvars(winreg.QueryValueEx(handle, "Path")[0]))
            except OSError:
                pass
    return os.pathsep.join(paths)


def resolve_executable(override, names):
    candidates = [override] if override else names
    for candidate in candidates:
        located = shutil.which(candidate, path=search_path())
        if located and Path(located).suffix.lower() not in {".bat", ".cmd"}:
            return str(Path(located).resolve())
        file = Path(candidate).expanduser()
        if file.is_file() and file.suffix.lower() not in {".bat", ".cmd"}:
            return str(file.resolve())
    return None


def runtime_info(language, executable):
    if executable is None:
        return {"available": False, "error": "Executable not found; use the explicit runtime option."}
    info = {"available": True, "executable": executable, "executable_sha256": sha256(executable)}
    if language == "aquarius":
        # This VM exposes --help but no --version. Fingerprint the actual shipped VM.
        info["version"] = "No version flag; see binary fingerprint and release directory"
        info["release_directory"] = str(Path(executable).parent)
        for filename in ("AquariusLangVM.dll", "AquariusDesktopVMREPL.dll"):
            path = Path(executable).with_name(filename)
            if path.is_file():
                info.setdefault("assemblies_sha256", {})[filename] = sha256(path)
    else:
        info["version"] = command_output([executable, "--version"]) or "Unavailable"
    return info


def environment_info():
    info = {"os": platform.platform(), "architecture": platform.machine(),
            "logical_cpus": os.cpu_count(), "cpu": platform.processor() or "Unavailable",
            "python_runner": sys.version, "runner_executable": sys.executable,
            "timer": "time.perf_counter_ns", "timer_resolution_seconds": time.get_clock_info("perf_counter").resolution,
            "ram_bytes": None, "power_plan": None}
    if os.name == "nt":
        import winreg
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r"HARDWARE\DESCRIPTION\System\CentralProcessor\0") as key:
                info["cpu"] = winreg.QueryValueEx(key, "ProcessorNameString")[0].strip()
        except OSError:
            pass
        class MemoryStatus(ctypes.Structure):
            _fields_ = [("length", ctypes.c_ulong), ("load", ctypes.c_ulong),
                        ("total_physical", ctypes.c_ulonglong), ("available_physical", ctypes.c_ulonglong),
                        ("total_page", ctypes.c_ulonglong), ("available_page", ctypes.c_ulonglong),
                        ("total_virtual", ctypes.c_ulonglong), ("available_virtual", ctypes.c_ulonglong),
                        ("available_extended_virtual", ctypes.c_ulonglong)]
        memory = MemoryStatus()
        memory.length = ctypes.sizeof(memory)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memory)):
            info["ram_bytes"] = memory.total_physical
        info["power_plan"] = command_output(["powercfg.exe", "/GETACTIVESCHEME"])
    else:
        try:
            info["ram_bytes"] = os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")
        except (ValueError, OSError, AttributeError):
            pass
        if Path("/proc/cpuinfo").is_file():
            match = re.search(r"^model name\s*:\s*(.+)$", Path("/proc/cpuinfo").read_text(), re.M)
            if match:
                info["cpu"] = match.group(1)
    return info


def parse_result(stdout):
    lines = [line.strip() for line in stdout.splitlines() if line.strip()]
    # Refuse extra output so diagnostics cannot accidentally masquerade as success.
    if len(lines) != 1 or not lines[0].startswith("RESULT "):
        raise ValueError("Expected exactly one 'RESULT <number>' line")
    try:
        value = Decimal(lines[0][7:].strip())
    except InvalidOperation as error:
        raise ValueError("Invalid numeric result") from error
    if not value.is_finite():
        raise ValueError("Result must be finite")
    return value


def execute(command, expected_value, spec, timeout, cwd):
    begin = time.perf_counter_ns()
    try:
        proc = subprocess.run(command, cwd=cwd, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=timeout,
                              stdin=subprocess.DEVNULL)
        elapsed = (time.perf_counter_ns() - begin) / 1e6
    except subprocess.TimeoutExpired as error:
        return {"status": "timeout", "elapsed_ms": (time.perf_counter_ns() - begin) / 1e6,
                "error": f"Exceeded {timeout:g} seconds", "stdout": decode(error.stdout),
                "stderr": decode(error.stderr)}
    except OSError as error:
        return {"status": "error", "elapsed_ms": (time.perf_counter_ns() - begin) / 1e6,
                "error": str(error), "stdout": "", "stderr": ""}
    sample = {"elapsed_ms": elapsed, "exit_code": proc.returncode,
              "stdout": proc.stdout, "stderr": proc.stderr}
    try:
        if proc.returncode != 0:
            raise ValueError(f"Exit code {proc.returncode}")
        value = parse_result(proc.stdout)
        if "relative_tolerance" in spec:
            valid = math.isclose(float(value), float(expected_value),
                                 rel_tol=spec["relative_tolerance"], abs_tol=spec["absolute_tolerance"])
        else:
            valid = value == Decimal(expected_value)
        if not valid:
            raise ValueError(f"Incorrect output: {value}; expected {expected_value}")
        sample.update(status="ok", result=str(value))
    except ValueError as error:
        sample.update(status="invalid", error=str(error))
    return sample


def decode(data):
    return data.decode("utf-8", errors="replace") if isinstance(data, bytes) else (data or "")


def summarize(record, repetitions):
    if record.get("unavailable"):
        return {"status": "unavailable"}
    if any(sample["status"] != "ok" for sample in record["warmups"] + record["samples"]):
        return {"status": "failed"}
    if len(record["samples"]) != repetitions:
        return {"status": "incomplete"}
    values = [s["elapsed_ms"] for s in record["samples"]]
    return {"status": "ok", "median_ms": statistics.median(values), "min_ms": min(values),
            "max_ms": max(values), "mean_ms": statistics.mean(values),
            "stdev_ms": statistics.stdev(values) if len(values) > 1 else 0.0,
            "cv_percent": statistics.stdev(values) / statistics.mean(values) * 100 if len(values) > 1 else 0.0}


def md(value):
    return str(value).replace("|", "\\|").replace("\n", " ").replace("\r", " ")


def generate_readme(report):
    config, env = report["config"], report["environment"]
    lines = ["# AquariusLang vs. Python vs. Node.js", "",
             "A desktop execution benchmark with ten classic algorithms, 30 standalone source scripts, "
             "and a Python runner that validates results and generates this README plus JSON/CSV reports.", "",
             "## Run it", "", "Requirements: Python 3.10+, Node.js, and the AquariusLang desktop VM "
             "(`AquariusDesktopVMREPL`, including its bundled dependencies). No Python packages or npm install required. "
             "The Aquarius scripts use AquariusLangTW keywords and bilingual built-ins; older English-only interpreters are not compatible.", "",
             "```powershell", "python run_benchmarks.py", "# Fast correctness check with smaller inputs:",
             "python run_benchmarks.py --profile smoke --repetitions 1 --warmups 0",
             "# Override runtime discovery when necessary:",
             'python run_benchmarks.py --aquarius "C:\\Aquarius\\AquariusDesktopVMREPL.exe" --node "C:\\Program Files\\nodejs\\node.exe"',
             "# Limit the workload selection:", "python run_benchmarks.py --benchmarks fibonacci sieve matrix",
             "# Rebuild README from an existing report without running benchmarks:",
             "python run_benchmarks.py --report-only results/latest.json",
             "# Harness and reference checks:", "python -m unittest discover -s tests -v", "```", "",
             "If `python` is an unconfigured pyenv shim, invoke an installed `python.exe` directly. "
             "The runner uses its own interpreter for the Python benchmarks by default. Use `--python PATH` to override it. "
             "It searches the process PATH and, on Windows, current user/system PATH entries, so a newly added Aquarius PATH works "
             "even in an older terminal session. Runtime overrides accept one executable path, not shell command strings.", "",
             "The runner stages source copies in a temporary directory and replaces only each script's `benchmark_n` declaration "
             "with its selected manifest size. Original scripts run directly with the standard sizes. "
             "Outputs go into a dated `results/` directory; `results/latest.json` and `README.md` are regenerated after each run. "
             "Use `--output-dir`, `--readme`, `--timeout`, `--seed`, `--repetitions`, and `--warmups` to customize a run. "
             "Exit code 1 means at least one runtime was unavailable or a case failed validation; failures remain visible in reports.", "",
             "## Measurement method", "",
             "- Each sample launches a fresh process; Python measures elapsed wall time with `perf_counter_ns` around "
             "process launch through exit and captured output. Source loading, parsing/compilation, runtime startup, "
             "allocation, garbage collection, algorithm execution, and output are included.",
             "- Aquarius executes `.aqua` source on its desktop VM. Python uses CPython source execution; Node.js uses V8 source execution. "
             "No precompiled bottles, NumPy, native algorithm libraries, worker threads, or built-in sort are used in timed workloads.",
             "- Discarded warmup processes prime OS file caches; they do **not** preserve a JIT or VM across measured processes. "
             "Each round shuffles all benchmark/language cases with a recorded seed and runs them sequentially.",
             "- Every warmup and measured sample must match an untimed Python correctness oracle. Integers match exactly; "
             "spectral norm squared uses relative tolerance 1e-9 and absolute tolerance 1e-12. "
             "Nonzero exits, timeouts, missing/extra output, nonfinite results, and checksum mismatches fail the case.",
             "- Aquarius integer `/` truncates; matching Python `//` and Node.js `Math.trunc` implement that arithmetic. "
             "Floating workloads use doubles (`d` literals in Aquarius). Standard inputs keep integer intermediates within signed 32-bit range.",
             "- Aquarius `push`/`加入` copies the array. Python and Node.js deliberately use copy-and-append "
             "during corresponding array construction. Thus sieve, sorting, and matrix setup include quadratic copying; "
             "these are matched baseline implementations, not idiomatic peak-performance versions of each language.",
             "- Medians describe these scripts on this machine. Small workloads can be dominated by startup; "
             "results do not isolate steady-state algorithm speed or establish a universal language ranking. "
             "CPU frequency, thermal state, background work, and scheduler noise are uncontrolled. "
             "Memory use and CPU time are not measured; RAM below describes the machine.", "",
             "## Latest run", "",
             f"- Started: {md(report['started_at'])}", f"- Finished: {md(report['finished_at'])}",
             f"- Timezone: {md(config['timezone'])}",
             f"- Profile: `{config['profile']}`; {config['repetitions']} measured samples and {config['warmups']} discarded warmups per case",
             f"- Order seed: {config['seed']}; per-process timeout: {config['timeout_seconds']:g} seconds",
             f"- OS: {md(env['os'])}", f"- Architecture: {md(env['architecture'])}",
             f"- CPU: {md(env['cpu'])}; logical CPUs: {env['logical_cpus']}",
             f"- Installed RAM: {env['ram_bytes'] / 1024**3:.2f} GiB" if env['ram_bytes'] else "- Installed RAM: unavailable",
             f"- Active power plan: {md(env['power_plan'] or 'Unavailable')}",
             f"- Python orchestrator: {md(env['python_runner'])}",
             f"- Timer resolution: {env['timer_resolution_seconds']:.3g} seconds", "",
             "| Runtime | Version / build | Executable |", "| --- | --- | --- |"]
    for lang, (title, _) in LANGUAGES.items():
        runtime = report["runtimes"][lang]
        lines.append(f"| {title} | {md(runtime.get('version', runtime.get('error')))} | "
                     f"{md(runtime.get('executable', 'Unavailable'))} |")
    aqua = report["runtimes"]["aquarius"]
    if aqua.get("available"):
        lines += ["", f"Aquarius release directory: `{aqua['release_directory']}`.", "",
                  f"Aquarius apphost SHA-256: `{aqua['executable_sha256']}`."]
        for filename, fingerprint in aqua.get("assemblies_sha256", {}).items():
            lines.append(f"- `{filename}` SHA-256: `{fingerprint}`")
    lines += ["", "## Results", "", "All durations are milliseconds. Lower is faster. "
              "Ratios are median runtime / median Python runtime; values below 1 mean faster than Python for this workload.", "",
              "| Algorithm | n | Aquarius median | Python median | Node.js median | Aquarius / Python | Node.js / Python |",
              "| --- | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for name in report["benchmarks"]:
        spec = report["benchmarks"][name]
        summaries = {lang: report["cases"][f"{name}/{lang}"]["summary"] for lang in LANGUAGES}
        cells = [f"{s['median_ms']:.3f}" if s["status"] == "ok" else s["status"].upper() for s in summaries.values()]
        def ratio(lang):
            s, py = summaries[lang], summaries["python"]
            return f"{s['median_ms'] / py['median_ms']:.2f}x" if s["status"] == py["status"] == "ok" else "—"
        lines.append(f"| {spec['title']} | {spec['n']} | " + " | ".join(cells) +
                     f" | {ratio('aquarius')} | {ratio('node')} |")
    lines += ["", "### Timing variability", "", "CV is sample standard deviation / mean. "
              "With one sample, variability cannot be estimated and is shown as a dash.", "",
              "| Algorithm | Runtime | Min ms | Max ms | Std. dev. ms | CV | Valid samples |",
              "| --- | --- | ---: | ---: | ---: | ---: | ---: |"]
    for record in report["cases"].values():
        summary = record["summary"]
        valid = sum(s["status"] == "ok" for s in record["samples"])
        if summary["status"] == "ok":
            sd = f"{summary['stdev_ms']:.3f}" if config["repetitions"] > 1 else "—"
            cv = f"{summary['cv_percent']:.1f}%" if config["repetitions"] > 1 else "—"
            lines.append(f"| {record['benchmark']} | {LANGUAGES[record['language']][0]} | "
                         f"{summary['min_ms']:.3f} | {summary['max_ms']:.3f} | {sd} | {cv} | {valid}/{config['repetitions']} |")
        else:
            lines.append(f"| {record['benchmark']} | {LANGUAGES[record['language']][0]} | — | — | — | — | {valid}/{config['repetitions']} |")
    failures = []
    for key, record in report["cases"].items():
        if record.get("unavailable"):
            failures.append(f"- `{key}`: {md(record['unavailable'])}")
        for phase in ("warmups", "samples"):
            for index, sample in enumerate(record[phase]):
                if sample["status"] != "ok":
                    failures.append(f"- `{key}` {phase} #{index + 1}: {md(sample['error'])}")
    lines += ["", "## Validation", ""]
    if failures:
        lines += failures
    else:
        lines.append("All runtime outputs matched the correctness oracles for every warmup and measured sample.")
    lines += ["", "| Algorithm | Expected result | Workload |", "| --- | ---: | --- |"]
    for spec in report["benchmarks"].values():
        lines.append(f"| {spec['title']} | {spec['expected']} | {spec['description']} |")
    lines += ["", "## Reproducibility artifacts", "",
              f"- Raw samples, output, commands, execution order, metadata, executable hashes, and source hashes: `{report['artifacts']['json']}`",
              f"- Summary statistics and raw samples as CSV: `{report['artifacts']['summary_csv']}` and `{report['artifacts']['samples_csv']}`",
              "- `benchmarks.json`: standard/smoke input sizes and workload definitions.",
              "- `benchmarks/aquarius/`, `benchmarks/python/`, `benchmarks/node/`: standalone scripts.",
              "- `reference.py`: untimed correctness oracles; `tests/`: harness/reference regression checks.", "",
              "This README is generated by `run_benchmarks.py`; edits will be overwritten on the next run. "
              "The JSON preserves hashes of both original and staged scripts and the manifest, runner, and oracle. "
              "Temporary command paths identify the files used during the run; they are removed afterward. "
              "Keep the source and its matching report together when comparing runs.", ""]
    return "\n".join(lines)


def write_artifacts(report, directory, readme):
    directory.mkdir(parents=True, exist_ok=True)
    json_path = directory / "results.json"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (directory.parent / "latest.json").write_text(json_path.read_text(encoding="utf-8"), encoding="utf-8")
    with (directory / "summary.csv").open("w", newline="", encoding="utf-8") as file:
        fields = ["benchmark", "language", "n", "status", "median_ms", "min_ms", "max_ms", "mean_ms", "stdev_ms", "cv_percent"]
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for record in report["cases"].values():
            writer.writerow({"benchmark": record["benchmark"], "language": record["language"], "n": record["n"], **record["summary"]})
    with (directory / "samples.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["benchmark", "language", "phase", "round", "status", "elapsed_ms", "result", "error"])
        for record in report["cases"].values():
            for phase in ("warmups", "samples"):
                for sample in record[phase]:
                    writer.writerow([record["benchmark"], record["language"], phase, sample["round"],
                                     sample["status"], sample["elapsed_ms"], sample.get("result", ""), sample.get("error", "")])
    readme.parent.mkdir(parents=True, exist_ok=True)
    readme.write_text(generate_readme(report), encoding="utf-8")


def positive(value):
    parsed = int(value)
    if parsed < 1:
        raise argparse.ArgumentTypeError("Must be at least 1")
    return parsed


def nonnegative(value):
    parsed = int(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("Must be nonnegative")
    return parsed


def timeout_value(value):
    parsed = float(value)
    if not math.isfinite(parsed) or parsed <= 0:
        raise argparse.ArgumentTypeError("Must be a finite positive number")
    return parsed


def main(argv=None):
    manifest_path = ROOT / "benchmarks.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=["standard", "smoke"], default="standard")
    parser.add_argument("--benchmarks", choices=list(manifest), nargs="+", default=list(manifest))
    parser.add_argument("--repetitions", type=positive, default=5)
    parser.add_argument("--warmups", type=nonnegative, default=1)
    parser.add_argument("--timeout", type=timeout_value, default=120.0)
    parser.add_argument("--seed", type=int, default=20261010)
    parser.add_argument("--timezone", default="Asia/Taipei")
    parser.add_argument("--aquarius", help="Path to AquariusDesktopVMREPL executable")
    parser.add_argument("--python", default=sys.executable, help="Python executable (defaults to this interpreter)")
    parser.add_argument("--node", help="Node.js executable")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results")
    parser.add_argument("--readme", type=Path, default=ROOT / "README.md")
    parser.add_argument("--report-only", type=Path, help="Generate README from a saved JSON report, without executing scripts")
    args = parser.parse_args(argv)
    if args.report_only:
        report = json.loads(args.report_only.read_text(encoding="utf-8"))
        args.readme.parent.mkdir(parents=True, exist_ok=True)
        args.readme.write_text(generate_readme(report), encoding="utf-8")
        print(f"README generated: {args.readme.resolve()}")
        return 0
    try:
        tz = ZoneInfo(args.timezone)
    except ZoneInfoNotFoundError:
        if args.timezone == "Asia/Taipei":
            tz = timezone(timedelta(hours=8), "Asia/Taipei")
        else:
            parser.error("Timezone database unavailable or unknown timezone; use Asia/Taipei or install tzdata")
    started = datetime.now(tz)
    directory = args.output_dir.resolve() / started.strftime("%Y%m%d-%H%M%S-%f")
    executables = {"aquarius": resolve_executable(args.aquarius, ["AquariusDesktopVMREPL.exe", "AquariusDesktopVMREPL"]),
                   "python": resolve_executable(args.python, []),
                   "node": resolve_executable(args.node, ["node"])}
    report = {"schema_version": 1, "started_at": started.isoformat(),
              "config": {"profile": args.profile, "repetitions": args.repetitions, "warmups": args.warmups,
                         "timeout_seconds": args.timeout, "seed": args.seed, "timezone": args.timezone},
              "environment": environment_info(),
              "runtimes": {lang: runtime_info(lang, exe) for lang, exe in executables.items()},
              "benchmarks": {}, "cases": {}, "execution_order": [],
              "source_sha256": {p.name: sha256(p) for p in (manifest_path, Path(__file__), ROOT / "reference.py")},
              "artifacts": {"json": str(directory / "results.json"),
                            "summary_csv": str(directory / "summary.csv"), "samples_csv": str(directory / "samples.csv")}}
    rng = random.Random(args.seed)
    work_root = ROOT / ".benchmark-work"
    if not work_root.resolve().is_relative_to(ROOT):
        raise ValueError("Benchmark staging directory must remain inside the workspace")
    work_root.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="run-", dir=work_root) as temporary:
        stage = Path(temporary)
        for name in dict.fromkeys(args.benchmarks):
            spec = manifest[name]
            n = spec[args.profile]
            report["benchmarks"][name] = {**spec, "n": n, "expected": expected(name, n)}
            for lang, (_, extension) in LANGUAGES.items():
                source = ROOT / "benchmarks" / lang / (name + extension)
                text = source.read_text(encoding="utf-8")
                text, count = re.subn(r"(benchmark_n\s*=\s*)\d+", lambda match: match.group(1) + str(n), text)
                if count != 1:
                    raise ValueError(f"Expected one benchmark_n declaration in {source}")
                target = stage / lang / source.name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(text, encoding="utf-8")
                exe = executables[lang]
                record = {"benchmark": name, "language": lang, "n": n,
                          "source": str(source.relative_to(ROOT)), "source_sha256": sha256(source),
                          "staged_sha256": sha256(target), "command": [exe, str(target)] if exe else None,
                          "warmups": [], "samples": []}
                if not exe:
                    record["unavailable"] = report["runtimes"][lang]["error"]
                report["cases"][f"{name}/{lang}"] = record
        for phase, rounds in [("warmups", args.warmups), ("samples", args.repetitions)]:
            for round_number in range(1, rounds + 1):
                keys = [key for key, record in report["cases"].items() if not record.get("unavailable")]
                rng.shuffle(keys)
                for key in keys:
                    record = report["cases"][key]
                    spec = report["benchmarks"][record["benchmark"]]
                    sample = execute(record["command"], spec["expected"], spec, args.timeout, stage)
                    sample["round"] = round_number
                    record[phase].append(sample)
                    report["execution_order"].append({"case": key, "phase": phase, "round": round_number})
                    print(f"{phase} {round_number}/{rounds} {key}: {sample['status']} {sample['elapsed_ms']:.3f} ms", flush=True)
        for record in report["cases"].values():
            record["summary"] = summarize(record, args.repetitions)
    report["finished_at"] = datetime.now(tz).isoformat()
    write_artifacts(report, directory, args.readme.resolve())
    print(f"Report: {directory / 'results.json'}\nREADME: {args.readme.resolve()}")
    return 0 if all(r["summary"]["status"] == "ok" for r in report["cases"].values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
