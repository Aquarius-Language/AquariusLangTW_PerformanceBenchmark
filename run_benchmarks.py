"""Standard-library-only desktop benchmark harness and README generator (Python 3.10+)."""
from __future__ import annotations

import argparse
import csv
import ctypes
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
import hashlib
import itertools
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
from readme_report import composite_scores, generate_readme, mode_views, write_readmes

ROOT = Path(__file__).resolve().parent
# aquarius_typed: the same AquariusLang algorithms with optional type annotations, run by the same aqua compiler.
LANGUAGES = {"aquarius": ("AquariusLang", ".aqua"), "aquarius_typed": ("AquariusLang (optional types)", ".aqua"),
             "python": ("Python", ".py"), "node": ("Node.js", ".js"), "csharp": ("C#", ".cs")}
AQUARIUS = {"aquarius", "aquarius_typed"}
# standard: one cold timed run per process; warmed: untimed in-process runs first, then the median of several timed runs.
MODES = ("standard", "warmed")
TIMERS = {"aquarius": "目前時間() / currentTime() (monotonic milliseconds)",
          "aquarius_typed": "目前時間() / currentTime() (monotonic milliseconds)",
          "python": "time.perf_counter_ns() (nanoseconds / 1e6)",
          "node": "process.hrtime.bigint() (nanoseconds / 1e6)",
          "csharp": "System.Diagnostics.Stopwatch.GetTimestamp() (ticks * 1000 / Frequency)"}


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


def resolve_dotnet(override=None):
    """Prefer a host with an SDK, including the standard per-user installation."""
    host = "dotnet.exe" if os.name == "nt" else "dotnet"
    candidates = [override] if override else ["dotnet", str(Path.home() / ".dotnet" / host)]
    if not override and os.environ.get("DOTNET_ROOT"):
        candidates.insert(1, str(Path(os.environ["DOTNET_ROOT"]) / host))
    fallback = None
    for candidate in candidates:
        executable = resolve_executable(candidate, [])
        if executable:
            fallback = fallback or executable
            sdks = command_output([executable, "--list-sdks"]) or ""
            if any(int(major) >= 8 for major in re.findall(r"^(\d+)\.", sdks, re.M)):
                return executable
    return fallback


def runtime_info(language, executable):
    if executable is None:
        return {"available": False, "error": "Executable not found; use the explicit runtime option."}
    info = {"available": True, "executable": executable, "executable_sha256": sha256(executable),
            "benchmark_timer": TIMERS[language]}
    if language in AQUARIUS:
        # Fingerprint the selected compiler, core, engine and native engine binary.
        info["version"] = "No version flag; see binary fingerprint and release directory"
        info["release_directory"] = str(Path(executable).parent)
        info["backend"] = "compiled-wasm" if Path(executable).with_name("Wasmtime.Dotnet.dll").is_file() else "legacy-vm" if Path(executable).with_name("AquariusLangVM.dll").is_file() else "unknown"
        for filename in ("AquariusCore.dll", "AquariusDesktop.dll", "Wasmtime.Dotnet.dll", "wasmtime.dll", "libwasmtime.so", "libwasmtime.dylib", "AquariusLangVM.dll", "AquariusDesktopVMREPL.dll"):
            path = Path(executable).with_name(filename)
            if path.is_file():
                info.setdefault("assemblies_sha256", {})[filename] = sha256(path)
    elif language == "csharp":
        info["sdks"] = command_output([executable, "--list-sdks"]) or ""
        info["runtimes"] = command_output([executable, "--list-runtimes"]) or ""
        info.update(backend="dotnet-jit", target_framework="net8.0", build_configuration="Release", tiered_compilation=False)
        if not any(int(major) >= 8 for major in re.findall(r"^(\d+)\.", info["sdks"], re.M)):
            info.update(available=False, error="A .NET 8+ SDK is required; use --dotnet with an SDK installation.")
        info["version"] = "SDKs: " + (info["sdks"] or "Unavailable") + "\nRuntimes: " + (info["runtimes"] or "Unavailable")
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
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.GetCurrentProcess.restype = ctypes.c_void_p
        kernel.GetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_size_t), ctypes.POINTER(ctypes.c_size_t)]
        process_mask, system_mask = ctypes.c_size_t(), ctypes.c_size_t()
        if kernel.GetProcessAffinityMask(kernel.GetCurrentProcess(), ctypes.byref(process_mask), ctypes.byref(system_mask)):
            info["process_affinity_mask"] = hex(process_mask.value)

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


def parse_sample(stdout, runs=1):
    """Require a checksum and an in-process duration for every timed run; never fall back to startup time.

    Returns one (result, elapsed_ms) pair per timed run, in order.
    """
    lines = [line.strip() for line in stdout.splitlines() if line.strip()]
    if len(lines) != 2 * runs or not all(line.startswith("ELAPSED_MS ") for line in lines[1::2]):
        raise ValueError(f"Expected exactly {runs} pair(s) of 'RESULT <number>' and 'ELAPSED_MS <milliseconds>' lines")
    pairs = []
    for result_line, elapsed_line in zip(lines[0::2], lines[1::2]):
        value = parse_result(result_line)
        try:
            elapsed = float(elapsed_line[11:].strip())
        except ValueError as error:
            raise ValueError("Invalid elapsed time") from error
        if not math.isfinite(elapsed) or elapsed <= 0:
            raise ValueError("Elapsed time must be finite and positive")
        pairs.append((value, elapsed))
    return pairs


def execute(command, expected_value, spec, timeout, cwd, *, timing="in-process", runs=1):
    # The historical VM diagnostic explicitly uses process timing because old
    # Aquarius versions have no clock builtin. Published benchmarks always use
    # the default in-process protocol and cannot fall back to process timing.
    if timing not in {"in-process", "process"}:
        raise ValueError(f"Unknown timing mode: {timing}")
    if timing == "process" and runs != 1:
        raise ValueError("Process timing measures exactly one run per process")
    begin = time.perf_counter_ns()
    try:
        proc = subprocess.run(command, cwd=cwd, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=timeout,
                              stdin=subprocess.DEVNULL)
        process_elapsed = (time.perf_counter_ns() - begin) / 1e6
    except subprocess.TimeoutExpired as error:
        return {"status": "timeout", "elapsed_ms": None, "process_elapsed_ms": (time.perf_counter_ns() - begin) / 1e6,
                "error": f"Exceeded {timeout:g} seconds", "stdout": decode(error.stdout),
                "stderr": decode(error.stderr)}
    except OSError as error:
        return {"status": "error", "elapsed_ms": None, "process_elapsed_ms": (time.perf_counter_ns() - begin) / 1e6,
                "error": str(error), "stdout": "", "stderr": ""}
    sample = {"elapsed_ms": None, "process_elapsed_ms": process_elapsed, "exit_code": proc.returncode,
              "stdout": proc.stdout, "stderr": proc.stderr}
    try:
        if proc.returncode != 0:
            raise ValueError(f"Exit code {proc.returncode}")
        if timing == "process":
            pairs = [(parse_result(proc.stdout), process_elapsed)]
        else:
            pairs = parse_sample(proc.stdout, runs)
        # A process's value is the median of its timed runs (the single run in standard mode).
        sample["run_elapsed_ms"] = [elapsed for _, elapsed in pairs]
        sample["elapsed_ms"] = statistics.median(sample["run_elapsed_ms"])
        for value, _ in pairs:  # Every timed run must reproduce the reference answer.
            if "relative_tolerance" in spec:
                valid = math.isclose(float(value), float(expected_value),
                                     rel_tol=spec["relative_tolerance"], abs_tol=spec["absolute_tolerance"])
            else:
                valid = value == Decimal(expected_value)
            if not valid:
                raise ValueError(f"Incorrect output: {value}; expected {expected_value}")
        sample.update(status="ok", result=str(pairs[0][0]))
    except ValueError as error:
        sample.update(status="invalid", error=str(error))
    return sample


def decode(data):
    return data.decode("utf-8", errors="replace") if isinstance(data, bytes) else (data or "")


def summarize(record, repetitions):
    if record.get("unavailable"):
        return {"status": "unavailable"}
    if record.get("build", {}).get("error"):
        return {"status": "failed"}
    if any(sample["status"] != "ok" for sample in record["warmups"] + record["samples"]):
        return {"status": "failed"}
    if len(record["samples"]) != repetitions:
        return {"status": "incomplete"}
    values = [s["elapsed_ms"] for s in record["samples"]]
    return {"status": "ok", "median_ms": statistics.median(values), "min_ms": min(values),
            "max_ms": max(values), "mean_ms": statistics.mean(values),
            "stdev_ms": statistics.stdev(values) if len(values) > 1 else 0.0,
            "cv_percent": statistics.stdev(values) / statistics.mean(values) * 100 if len(values) > 1 else 0.0}


def write_artifacts(report, directory, readme):
    directory.mkdir(parents=True, exist_ok=True)
    report["scores"] = {mode: composite_scores(view) for mode, _, view in mode_views(report)}
    json_path = directory / "results.json"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (directory.parent / "latest.json").write_text(json_path.read_text(encoding="utf-8"), encoding="utf-8")
    with (directory / "summary.csv").open("w", newline="", encoding="utf-8") as file:
        fields = ["benchmark", "language", "mode", "n", "status", "median_ms", "min_ms", "max_ms", "mean_ms", "stdev_ms", "cv_percent"]
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for record in report["cases"].values():
            writer.writerow({"benchmark": record["benchmark"], "language": record["language"], "mode": record["mode"],
                             "n": record["n"], **record["summary"]})
    with (directory / "samples.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["benchmark", "language", "mode", "phase", "round", "status", "elapsed_ms",
                         "run_elapsed_ms", "process_elapsed_ms", "result", "error"])
        for record in report["cases"].values():
            for phase in ("warmups", "samples"):
                for sample in record[phase]:
                    runs = ";".join(repr(value) for value in sample.get("run_elapsed_ms", []))
                    writer.writerow([record["benchmark"], record["language"], record["mode"], phase, sample["round"],
                                     sample["status"], sample["elapsed_ms"], runs, sample["process_elapsed_ms"],
                                     sample.get("result", ""), sample.get("error", "")])
    return write_readmes(report, readme)


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


def substitute(text, name, value, source):
    """Replace the single numeric declaration of a driver variable; typed scripts annotate it (benchmark_n: 整數 = 28)."""
    text, count = re.subn(rf"(\b{name}(?:\s*:\s*\S+)?\s*=\s*)\d+", lambda match: match.group(1) + str(value), text)
    if count != 1:
        raise ValueError(f"Expected one {name} declaration in {source}")
    return text


def build_csharp(executable, source, stage, timeout):
    """Compile one workload outside sample timing, retaining build diagnostics."""
    project = source.parent / "Benchmark.csproj"
    for filename in ("Benchmark.csproj", "NuGet.Config"):
        shutil.copyfile(ROOT / "benchmarks" / "csharp" / filename, source.parent / filename)
    output = source.parent / "out"
    command = [executable, "build", str(project), "--configuration", "Release",
               "--output", str(output), "--nologo", "--verbosity", "quiet",
               f"-p:BenchmarkSource={source.name}", "-p:UseSharedCompilation=false"]
    env = {**os.environ, "DOTNET_CLI_HOME": str(stage / "dotnet-home"),
           "DOTNET_CLI_TELEMETRY_OPTOUT": "1", "DOTNET_SKIP_FIRST_TIME_EXPERIENCE": "1",
           "DOTNET_NOLOGO": "1", "DOTNET_CLI_WORKLOAD_UPDATE_NOTIFY_DISABLE": "true"}
    begin = time.perf_counter_ns()
    build = {"command": command, "configuration": "Release", "target_framework": "net8.0"}
    assembly = output / "Benchmark.dll"
    try:
        proc = subprocess.run(command, cwd=stage, env=env, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=timeout, stdin=subprocess.DEVNULL)
        build.update(exit_code=proc.returncode, stdout=proc.stdout, stderr=proc.stderr)
        if proc.returncode != 0 or not assembly.is_file():
            build["error"] = "C# Release build failed; see build stdout/stderr."
    except subprocess.TimeoutExpired as error:
        build.update(error=f"C# build exceeded {timeout:g} seconds", stdout=decode(error.stdout), stderr=decode(error.stderr))
    except OSError as error:
        build.update(error=str(error), stdout="", stderr="")
    build["elapsed_ms"] = (time.perf_counter_ns() - begin) / 1e6
    return build, assembly


def main(argv=None):
    manifest_path = ROOT / "benchmarks.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=["standard", "smoke", "large"], default="standard")
    parser.add_argument("--benchmarks", choices=list(manifest), nargs="+", default=list(manifest))
    parser.add_argument("--repetitions", type=positive, default=5, help="measured processes per case")
    parser.add_argument("--warmups", type=nonnegative, default=1, help="discarded warm-up processes per case and round")
    parser.add_argument("--modes", choices=list(MODES), nargs="+", default=list(MODES),
                        help="standard: one cold timed run per process; warmed: in-process warm-up runs, then timed runs")
    parser.add_argument("--in-process-warmups", type=nonnegative, default=5, help="untimed runs per process in warmed mode")
    parser.add_argument("--in-process-runs", type=positive, default=5, help="timed runs per process in warmed mode (median)")
    parser.add_argument("--timeout", type=timeout_value, default=120.0)
    parser.add_argument("--seed", type=int, default=20261010)
    parser.add_argument("--timezone", default="Asia/Taipei")
    parser.add_argument("--aquarius", help="aqua compiler executable (defaults to searching PATH); builds Wasm before timing")
    parser.add_argument("--python", default=sys.executable, help="Python executable (defaults to this interpreter)")
    parser.add_argument("--node", help="Node.js executable")
    parser.add_argument("--dotnet", help=".NET SDK host executable for C# (net8.0, Release)")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results")
    parser.add_argument("--readme", type=Path, default=ROOT / "README.md",
                        help="English README; the Traditional Chinese README is written beside it as .tw.md")
    parser.add_argument("--report-only", type=Path, help="Generate the READMEs from a saved JSON report, without executing scripts")
    args = parser.parse_args(argv)
    if args.report_only:
        report = json.loads(args.report_only.read_text(encoding="utf-8"))
        for readme in write_readmes(report, args.readme):
            print(f"README generated: {readme.resolve()}")
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
    aqua = resolve_executable(args.aquarius, ["aqua.exe", "aqua"])
    executables = {"aquarius": aqua, "aquarius_typed": aqua,
                   "python": resolve_executable(args.python, []),
                   "node": resolve_executable(args.node, ["node"]),
                   "csharp": resolve_dotnet(args.dotnet)}
    modes = {mode: {"in_process_warmups": 0, "in_process_runs": 1} if mode == "standard" else
             {"in_process_warmups": args.in_process_warmups, "in_process_runs": args.in_process_runs}
             for mode in MODES if mode in args.modes}
    report = {"schema_version": 4, "started_at": started.isoformat(),
              "config": {"profile": args.profile, "repetitions": args.repetitions, "warmups": args.warmups,
                         "timeout_seconds": args.timeout, "seed": args.seed, "timezone": args.timezone, "aquarius_mode": "precompiled",
                         "csharp_tiered_compilation": False, "modes": modes,
                         "timing": "in-process", "timing_boundary": "data initialization and computation; startup/compilation/output excluded",
                         "score_normalization": "fastest language = 100; equal-weight geometric mean of relative speeds"},
              "environment": environment_info(),
              "runtimes": {lang: runtime_info(lang, exe) for lang, exe in executables.items()},
              "benchmarks": {}, "cases": {}, "execution_order": [],
              "source_sha256": {p.name: sha256(p) for p in (manifest_path, Path(__file__), ROOT / "reference.py", ROOT / "readme_report.py")},
              "artifacts": {"json": str(directory / "results.json"),
                            "summary_csv": str(directory / "summary.csv"), "samples_csv": str(directory / "samples.csv")}}
    report["source_sha256"].update({f"benchmarks/csharp/{name}": sha256(ROOT / "benchmarks" / "csharp" / name)
                                    for name in ("Benchmark.csproj", "NuGet.Config")})
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
            for (lang, (_, extension)), (mode, params) in itertools.product(LANGUAGES.items(), modes.items()):
                source = ROOT / "benchmarks" / lang / (name + extension)
                text = substitute(source.read_text(encoding="utf-8"), "benchmark_n", n, source)
                # The mode only changes the driver's counts, so each mode gets its own staged copy.
                text = substitute(text, "benchmark_warmups", params["in_process_warmups"], source)
                text = substitute(text, "benchmark_timed_runs", params["in_process_runs"], source)
                target = stage / mode / lang / source.name
                if lang == "csharp":
                    target = stage / mode / lang / name / source.name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(text, encoding="utf-8")
                exe = executables[lang]
                record = {"benchmark": name, "language": lang, "mode": mode, "n": n, **params,
                          "source": str(source.relative_to(ROOT)), "source_sha256": sha256(source),
                          "staged_sha256": sha256(target), "command": [exe, str(target)] if exe else None,
                          "warmups": [], "samples": []}
                if exe and lang in AQUARIUS:
                    wasm = target.with_suffix(".wasm")
                    command = [exe, "build", str(target), "--root", str(target.parent), "-o", str(wasm)]
                    begin = time.perf_counter_ns()
                    build = subprocess.run(command, cwd=stage, capture_output=True, text=True, encoding="utf-8", timeout=args.timeout, stdin=subprocess.DEVNULL)
                    record["build"] = {"command": command, "elapsed_ms": (time.perf_counter_ns() - begin) / 1e6, "exit_code": build.returncode, "stdout": build.stdout, "stderr": build.stderr}
                    if build.returncode != 0 or not wasm.is_file():
                        raise RuntimeError(f"Wasm build failed for {name}: {build.stderr}")
                    record["wasm_sha256"] = sha256(wasm)
                    record["command"] = [exe, "run", str(wasm)]
                if not report["runtimes"][lang]["available"]:
                    record["unavailable"] = report["runtimes"][lang]["error"]
                    record["command"] = None
                elif lang == "csharp":
                    record["build"], assembly = build_csharp(exe, target, stage, args.timeout)
                    record["command"] = None
                    if not record["build"].get("error"):
                        record["assembly_sha256"] = sha256(assembly)
                        record["command"] = [exe, str(assembly)]
                report["cases"][f"{name}/{lang}/{mode}"] = record
        for phase, rounds in [("warmups", args.warmups), ("samples", args.repetitions)]:
            for round_number in range(1, rounds + 1):
                keys = [key for key, record in report["cases"].items() if record["command"]]
                rng.shuffle(keys)
                for key in keys:
                    record = report["cases"][key]
                    spec = report["benchmarks"][record["benchmark"]]
                    sample = execute(record["command"], spec["expected"], spec, args.timeout, stage,
                                     runs=record["in_process_runs"])
                    sample["round"] = round_number
                    record[phase].append(sample)
                    report["execution_order"].append({"case": key, "phase": phase, "round": round_number})
                    duration = f"{sample['elapsed_ms']:.6f} ms" if sample["elapsed_ms"] is not None else "no workload timing"
                    print(f"{phase} {round_number}/{rounds} {key}: {sample['status']} {duration}", flush=True)
        for record in report["cases"].values():
            record["summary"] = summarize(record, args.repetitions)
    report["finished_at"] = datetime.now(tz).isoformat()
    english, chinese = write_artifacts(report, directory, args.readme.resolve())
    print(f"Report: {directory / 'results.json'}\nREADME: {english}\nREADME: {chinese}")
    return 0 if all(r["summary"]["status"] == "ok" for r in report["cases"].values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
