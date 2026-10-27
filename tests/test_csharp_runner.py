import csv
import itertools
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from reference import expected
from run_benchmarks import ROOT, build_csharp, resolve_dotnet, runtime_info, summarize


class CSharpRunnerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work = ROOT / ".benchmark-work"
        cls.work.mkdir(exist_ok=True)

    def test_dotnet_discovery_prefers_an_sdk_over_a_runtime_only_host(self):
        with patch("run_benchmarks.resolve_executable", side_effect=lambda path, _: path), \
             patch("run_benchmarks.command_output", side_effect=["", "8.0.425 [sdk]"]):
            self.assertNotEqual(resolve_dotnet(), "dotnet")
        with patch("run_benchmarks.resolve_executable", return_value="chosen-dotnet") as resolve, \
             patch("run_benchmarks.command_output", return_value=""):
            self.assertEqual(resolve_dotnet("chosen-dotnet"), "chosen-dotnet")
            resolve.assert_called_once_with("chosen-dotnet", [])

    def test_runtime_only_host_is_unavailable_with_actionable_error(self):
        with patch("run_benchmarks.sha256", return_value="fingerprint"), \
             patch("run_benchmarks.command_output", side_effect=["", "Microsoft.NETCore.App 8.0.31"]):
            info = runtime_info("csharp", "runtime-only-dotnet")
        self.assertFalse(info["available"])
        self.assertIn("--dotnet", info["error"])
        self.assertIn("SDK", info["error"])

    def test_build_failure_and_timeout_are_retained_as_failed_cases(self):
        with tempfile.TemporaryDirectory(dir=self.work) as directory:
            stage = Path(directory)
            source = stage / "fibonacci.cs"
            source.write_text("broken C#", encoding="utf-8")
            outcomes = [subprocess.CompletedProcess([], 1, "compiler error", "details"),
                        subprocess.TimeoutExpired(["dotnet"], 1, output=b"partial", stderr=b"timeout")]
            for outcome in outcomes:
                with self.subTest(outcome=type(outcome).__name__):
                    kwargs = {"side_effect": outcome} if isinstance(outcome, Exception) else {"return_value": outcome}
                    with patch("run_benchmarks.subprocess.run", **kwargs):
                        build, assembly = build_csharp("dotnet", source, stage, 1)
                    self.assertIn("error", build)
                    self.assertTrue(build["stdout"])
                    self.assertFalse(assembly.exists())
                    self.assertEqual(summarize({"build": build, "warmups": [], "samples": []}, 1)["status"], "failed")

    def test_all_workloads_match_reference_at_smoke_and_standard_sizes(self):
        dotnet = resolve_dotnet()
        if not runtime_info("csharp", dotnet)["available"]:
            self.skipTest("Install a .NET 8 SDK for the C# integration check")
        # Both modes at the smoke size; the standard size checks the cold mode only to limit builds.
        for profile, modes in [("smoke", ["standard", "warmed"]), ("standard", ["standard"])]:
            with self.subTest(profile=profile), tempfile.TemporaryDirectory(dir=self.work) as directory:
                path = Path(directory)
                proc = subprocess.run(
                    [sys.executable, str(ROOT / "run_benchmarks.py"), "--profile", profile,
                     "--modes", *modes, "--in-process-warmups", "1", "--in-process-runs", "2",
                     "--repetitions", "1", "--warmups", "1", "--dotnet", dotnet,
                     "--aquarius", str(path / "missing-aqua"), "--node", str(path / "missing-node"),
                     "--output-dir", str(path / "results"), "--readme", str(path / "README.md")],
                    capture_output=True, text=True, encoding="utf-8", timeout=180)
                self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)  # Other runtimes deliberately absent.
                report = json.loads((path / "results/latest.json").read_text(encoding="utf-8"))
                for (name, spec), mode in itertools.product(report["benchmarks"].items(), modes):
                    case = report["cases"][f"{name}/csharp/{mode}"]
                    self.assertEqual(len(case["samples"][0]["run_elapsed_ms"]), case["in_process_runs"])
                    self.assertEqual(case["summary"]["status"], "ok", case)
                    self.assertEqual(case["n"], spec[profile])
                    self.assertEqual(case["build"]["exit_code"], 0)
                    self.assertIn("Release", case["build"]["command"])
                    self.assertEqual(case["command"][0], dotnet)
                    self.assertTrue(case["command"][1].endswith("Benchmark.dll"))
                    self.assertEqual(len(case["assembly_sha256"]), 64)
                    for sample in case["warmups"] + case["samples"]:
                        answer = expected(name, spec[profile])
                        self.assertTrue(math.isclose(float(sample["result"]), answer, rel_tol=1e-9, abs_tol=1e-12))
                        self.assertGreater(sample["elapsed_ms"], 0)
                        self.assertGreater(sample["process_elapsed_ms"], sample["elapsed_ms"])
                readme = (path / "README.md").read_text(encoding="utf-8")
                self.assertIn("C# 中位數", readme)
                self.assertIn("C#／Python 耗時倍率", readme)
                with Path(report["artifacts"]["summary_csv"]).open(encoding="utf-8", newline="") as file:
                    rows = [row for row in csv.DictReader(file) if row["language"] == "csharp"]
                self.assertEqual(len(rows), 10 * len(modes))
                self.assertTrue(all(row["status"] == "ok" for row in rows))


if __name__ == "__main__":
    unittest.main()
