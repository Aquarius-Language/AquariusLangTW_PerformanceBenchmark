import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from reference import expected
from readme_report import composite_scores, mode_views, typed_vs_node_lines
from run_benchmarks import (LANGUAGES, ROOT, execute, generate_readme, parse_result, parse_sample,
                            resolve_executable, substitute, summarize)


class ReferenceTests(unittest.TestCase):
    def test_known_answers(self):
        for name, n, answer in [("fibonacci", 28, 317811), ("ackermann", 6, 509),
                                ("sieve", 10000, 1229), ("nqueens", 8, 92),
                                ("binary_trees", 12, 65528), ("matrix", 1, 0),
                                ("collatz", 10, 67), ("spectral_norm", 1, 1.0)]:
            with self.subTest(name=name):
                self.assertEqual(expected(name, n), answer)

    def test_python_scripts_match_oracles(self):
        manifest = json.loads((ROOT / "benchmarks.json").read_text(encoding="utf-8"))
        for name, spec in manifest.items():
            with self.subTest(name=name):
                output = subprocess.check_output([sys.executable, str(ROOT / "benchmarks/python" / f"{name}.py")],
                                                 text=True, timeout=30)
                [(observed, elapsed)] = parse_sample(output)  # Standalone scripts run the standard mode.
                self.assertGreater(elapsed, 0)
                answer = expected(name, spec["standard"])
                if "relative_tolerance" in spec:
                    self.assertTrue(math.isclose(float(observed), answer, rel_tol=1e-9, abs_tol=1e-12))
                else:
                    self.assertEqual(observed, answer)


class HarnessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work_root = ROOT / ".benchmark-work"
        cls.work_root.mkdir(exist_ok=True)

    def test_rejects_invalid_output(self):
        for output in ["", "42", "RESULT NaN", "RESULT Infinity", "RESULT 1\nRESULT 1",
                       "diagnostic\nRESULT 1", "RESULT nope"]:
            with self.subTest(output=output):
                with self.assertRaises(ValueError):
                    parse_result(output)
        self.assertEqual(parse_result("RESULT 1\r\n"), 1)

    def run_child(self, code, answer=7, spec=None, timeout=5):
        with tempfile.TemporaryDirectory(dir=self.work_root) as directory:
            return execute([sys.executable, "-c", code], answer, spec or {}, timeout, Path(directory))

    def test_correctness_exit_and_timeout(self):
        self.assertEqual(self.run_child("print('RESULT 7'); print('ELAPSED_MS 1')")["status"], "ok")
        self.assertEqual(self.run_child("print('RESULT 8'); print('ELAPSED_MS 1')")["status"], "invalid")
        self.assertEqual(self.run_child("print('RESULT 7'); print('ELAPSED_MS 1'); raise SystemExit(2)")["status"], "invalid")
        timeout = self.run_child("import time; time.sleep(2)", timeout=0.05)
        self.assertEqual(timeout["status"], "timeout")
        self.assertIsNone(timeout["elapsed_ms"])
        self.assertGreater(timeout["process_elapsed_ms"], 0)

    def test_requires_valid_in_process_timing(self):
        for output in ["RESULT 7", "ELAPSED_MS 1\nRESULT 7", "RESULT 7\nELAPSED_MS 1\nextra",
                       "RESULT 7\nELAPSED_MS 1\nELAPSED_MS 2", "RESULT 7\nELAPSED_MS",
                       *[f"RESULT 7\nELAPSED_MS {value}" for value in
                         ["NaN", "Infinity", "-Infinity", "0", "-1", "nope", "1e309"]]]:
            with self.subTest(output=output), self.assertRaises(ValueError):
                parse_sample(output)
        self.assertEqual(parse_sample("RESULT 7\r\nELAPSED_MS 0.0001\r\n"), [(7, 0.0001)])
        missing = self.run_child("print('RESULT 7')")
        self.assertEqual(missing["status"], "invalid")
        self.assertIsNone(missing["elapsed_ms"])

    def test_every_timed_run_is_parsed_and_validated(self):
        three = "RESULT 7\nELAPSED_MS 3\nRESULT 7\nELAPSED_MS 1\nRESULT 7\nELAPSED_MS 2"
        self.assertEqual(parse_sample(three, 3), [(7, 3.0), (7, 1.0), (7, 2.0)])
        for output in ["RESULT 7\nELAPSED_MS 1\nRESULT 7\nELAPSED_MS 1",  # missing run
                       three + "\nRESULT 7\nELAPSED_MS 1",  # extra run
                       three + "\nRESULT 7",  # trailing result
                       "RESULT 7\nRESULT 7\nELAPSED_MS 1\nELAPSED_MS 1\nRESULT 7\nELAPSED_MS 1",
                       three.replace("ELAPSED_MS 2", "ELAPSED_MS 0")]:
            with self.subTest(output=output), self.assertRaises(ValueError):
                parse_sample(output, 3)
        with tempfile.TemporaryDirectory(dir=self.work_root) as directory:
            code = "for t in (3, 1, 2): print('RESULT 7'); print('ELAPSED_MS', t)"
            sample = execute([sys.executable, "-c", code], 7, {}, 5, Path(directory), runs=3)
            self.assertEqual(sample["status"], "ok")
            self.assertEqual(sample["run_elapsed_ms"], [3, 1, 2])
            self.assertEqual(sample["elapsed_ms"], 2)  # The process's value is the median of its timed runs.
            # One wrong timed run fails the whole sample, even when the others are correct.
            code = "for r in (7, 8, 7): print('RESULT', r); print('ELAPSED_MS 1')"
            self.assertEqual(execute([sys.executable, "-c", code], 7, {}, 5, Path(directory), runs=3)["status"], "invalid")
            self.assertEqual(execute([sys.executable, "-c", "print('RESULT 7'); print('ELAPSED_MS 1')"],
                                     7, {}, 5, Path(directory), runs=3)["status"], "invalid")

    def test_every_script_declares_substitutable_driver_counts(self):
        for language, (_, extension) in LANGUAGES.items():
            for source in sorted((ROOT / "benchmarks" / language).glob("*" + extension)):
                with self.subTest(source=source.name, language=language):
                    text = source.read_text(encoding="utf-8")
                    for name, default in [("benchmark_warmups", 0), ("benchmark_timed_runs", 1)]:
                        self.assertRegex(text, rf"\b{name}(?:: 整數)? = {default}\b")  # Standalone = standard mode.
                        self.assertRegex(substitute(text, name, 9, source), rf"\b{name}(?:: 整數)? = 9\b")
                    if language == "aquarius_typed":
                        self.assertIn("benchmark_timed_runs: 整數 = 4", substitute(text, "benchmark_timed_runs", 4, source))
        with self.assertRaises(ValueError):
            substitute("benchmark_n = 1\nbenchmark_n = 2", "benchmark_n", 3, "duplicate")
        with self.assertRaises(ValueError):
            substitute("x = 1", "benchmark_warmups", 3, "missing")

    def test_substituted_drivers_warm_up_and_time_every_run(self):
        manifest = json.loads((ROOT / "benchmarks.json").read_text(encoding="utf-8"))
        runners = {"python": (sys.executable, ".py"), "node": (resolve_executable(None, ["node"]), ".js")}
        for language, (executable, extension) in runners.items():
            if executable is None:
                continue
            for name, spec in manifest.items():
                with self.subTest(language=language, name=name), tempfile.TemporaryDirectory(dir=self.work_root) as directory:
                    source = ROOT / "benchmarks" / language / (name + extension)
                    text = substitute(source.read_text(encoding="utf-8"), "benchmark_n", spec["smoke"], source)
                    text = substitute(substitute(text, "benchmark_warmups", 2, source), "benchmark_timed_runs", 3, source)
                    target = Path(directory) / source.name
                    target.write_text(text, encoding="utf-8")
                    sample = execute([executable, str(target)], expected(name, spec["smoke"]), spec, 30, Path(directory), runs=3)
                    self.assertEqual(sample["status"], "ok", sample)
                    self.assertEqual(len(sample["run_elapsed_ms"]), 3)

    def test_statistics_use_reported_duration_excluding_process_overhead(self):
        sample = self.run_child("import time; time.sleep(0.1); print('RESULT 7'); print('ELAPSED_MS 0.125')")
        self.assertEqual(sample["status"], "ok")
        self.assertEqual(sample["elapsed_ms"], 0.125)
        self.assertGreater(sample["process_elapsed_ms"], 100)
        summary = summarize({"warmups": [], "samples": [sample]}, 1)
        self.assertEqual(summary["median_ms"], 0.125)

    def test_historical_diagnostic_requires_explicit_process_timing(self):
        with tempfile.TemporaryDirectory(dir=self.work_root) as directory:
            command = [sys.executable, "-c", "print('RESULT 7')"]
            sample = execute(command, 7, {}, 5, Path(directory), timing="process")
            self.assertEqual(sample["status"], "ok")
            self.assertEqual(sample["elapsed_ms"], sample["process_elapsed_ms"])

    def test_float_tolerance(self):
        spec = {"relative_tolerance": 1e-9, "absolute_tolerance": 1e-12}
        self.assertEqual(self.run_child("print('RESULT 1.0000000001'); print('ELAPSED_MS 1')", 1.0, spec)["status"], "ok")
        self.assertEqual(self.run_child("print('RESULT 1.001'); print('ELAPSED_MS 1')", 1.0, spec)["status"], "invalid")

    def test_failed_warmup_invalidates_case(self):
        valid = {"status": "ok", "elapsed_ms": 10.0}
        record = {"warmups": [{"status": "invalid"}], "samples": [valid]}
        self.assertEqual(summarize(record, 1)["status"], "failed")
        record["warmups"] = []
        self.assertEqual(summarize(record, 2)["status"], "incomplete")
        self.assertEqual(summarize(record, 1)["median_ms"], 10)

    def test_missing_runtime_is_reported(self):
        with tempfile.TemporaryDirectory(dir=self.work_root) as temporary:
            path = Path(temporary)
            proc = subprocess.run([sys.executable, str(ROOT / "run_benchmarks.py"),
                                   "--profile", "smoke", "--benchmarks", "fibonacci", "--warmups", "0",
                                   "--repetitions", "1", "--in-process-warmups", "2", "--in-process-runs", "3",
                                   "--aquarius", str(path / "missing-runtime.exe"),
                                   "--node", str(path / "missing-node.exe"),
                                   "--dotnet", str(path / "missing-dotnet.exe"),
                                   "--output-dir", str(path / "results"), "--readme", str(path / "README.md")],
                                  capture_output=True, text=True, timeout=30)
            self.assertEqual(proc.returncode, 1, proc.stderr)
            report = json.loads((path / "results/latest.json").read_text(encoding="utf-8"))
            self.assertEqual(report["schema_version"], 4)
            self.assertEqual(report["config"]["modes"], {"standard": {"in_process_warmups": 0, "in_process_runs": 1},
                                                         "warmed": {"in_process_warmups": 2, "in_process_runs": 3}})
            for mode, runs in [("standard", 1), ("warmed", 3)]:
                self.assertEqual(report["cases"][f"fibonacci/aquarius/{mode}"]["summary"]["status"], "unavailable")
                self.assertEqual(report["cases"][f"fibonacci/csharp/{mode}"]["summary"]["status"], "unavailable")
                python = report["cases"][f"fibonacci/python/{mode}"]
                self.assertEqual(python["summary"]["status"], "ok")
                self.assertEqual(python["in_process_runs"], runs)
                self.assertEqual(len(python["samples"][0]["run_elapsed_ms"]), runs)
            self.assertNotEqual(report["cases"]["fibonacci/python/standard"]["staged_sha256"],
                                report["cases"]["fibonacci/python/warmed"]["staged_sha256"])
            self.assertEqual({entry["case"].rsplit("/", 1)[1] for entry in report["execution_order"]}, {"standard", "warmed"})
            readme = (path / "README.tw.md").read_text(encoding="utf-8")
            self.assertEqual(readme, generate_readme(report, "tw"))
            self.assertIn('<p><strong>繁體中文</strong> | <a href="README.md">English</a></p>', readme)
            self.assertIn("無法使用", readme)
            self.assertIn("## 標準模式（冷啟動，每個程序計時一次）", readme)
            self.assertIn("## 暖機模式（程序內先暖機 2 次，再計時 3 次取中位數）", readme)
            self.assertIn("### 星泉（型別） vs Node.js（暖機模式）", readme)
            english = (path / "README.md").read_text(encoding="utf-8")
            self.assertEqual(english, generate_readme(report))
            self.assertIn('<p><a href="README.tw.md">繁體中文</a> | <strong>English</strong></p>', english)
            self.assertIn("unavailable", english)
            self.assertIn("## Standard mode (cold start, one timed run per process)", english)
            self.assertIn("## Warmed mode (2 in-process warm-up runs, then the median of 3 timed runs)", english)
            self.assertIn("### AquariusLang (typed) vs Node.js (warmed mode)", english)
            self.assertEqual(report["scores"], {"standard": None, "warmed": None})
            with Path(report["artifacts"]["samples_csv"]).open(encoding="utf-8") as file:
                self.assertIn("run_elapsed_ms", file.readline())
            before = [(path / name).read_bytes() for name in ("README.md", "README.tw.md")]
            subprocess.run([sys.executable, str(ROOT / "run_benchmarks.py"), "--report-only",
                            str(path / "results/latest.json"), "--readme", str(path / "README.md")],
                           check=True, capture_output=True, timeout=30)
            self.assertEqual([(path / name).read_bytes() for name in ("README.md", "README.tw.md")], before)
            # Saved single-mode reports (schema 3 and older) keyed `benchmark/language` still render, labelled
            # from their configuration, and score only the languages that were actually measured.
            legacy = {**report, "schema_version": 3,
                      "config": {**{k: v for k, v in report["config"].items() if k != "modes"}, "in_process_warmups": 3},
                      "cases": {key.rsplit("/", 1)[0]: record for key, record in report["cases"].items()
                                if record["mode"] == "warmed"}}
            for record in legacy["cases"].values():
                del record["mode"]
            legacy_readme = generate_readme(legacy, "tw")
            self.assertIn("## 暖機模式（程序內先暖機 3 次，再計時 1 次）", legacy_readme)
            self.assertNotIn("## 標準模式（", legacy_readme)
            for language in ("csharp", "aquarius_typed"):
                del legacy["runtimes"][language]
                del legacy["cases"][f"fibonacci/{language}"]
            legacy_readme = generate_readme(legacy, "tw")
            self.assertTrue(legacy_readme.startswith("# 星泉、Python、Node.js 桌面執行效能評比"))
            self.assertNotIn("C#", legacy_readme)
            self.assertNotIn("星泉（型別） vs Node.js", legacy_readme)
            self.assertTrue(generate_readme(legacy).startswith(
                "# Desktop performance benchmark: AquariusLang, Python, Node.js"))
            legacy["config"]["in_process_warmups"] = 0  # The original cold design.
            self.assertIn("## 標準模式（冷啟動，每個程序計時一次）", generate_readme(legacy, "tw"))

    def test_committed_report_renders(self):
        report = json.loads((ROOT / "results" / "latest.json").read_text(encoding="utf-8"))
        self.assertIn("模式（", generate_readme(report, "tw"))
        self.assertIn("mode (", generate_readme(report))

    def test_modes_are_scored_separately(self):
        report = {"benchmarks": {"first": {}}, "runtimes": {"python": {}, "node": {}},
                  "config": {"modes": {"standard": {"in_process_warmups": 0, "in_process_runs": 1},
                                       "warmed": {"in_process_warmups": 5, "in_process_runs": 5}}}, "cases": {}}
        for mode, times in [("standard", {"python": 10, "node": 20}), ("warmed", {"python": 10, "node": 5})]:
            for language, duration in times.items():
                report["cases"][f"first/{language}/{mode}"] = {"mode": mode, "summary": {"status": "ok", "median_ms": duration}}
        scores = {mode: composite_scores(view) for mode, _, view in mode_views(report)}
        self.assertAlmostEqual(scores["standard"]["node"], 50)
        self.assertAlmostEqual(scores["warmed"]["node"], 100)
        self.assertAlmostEqual(scores["warmed"]["python"], 50)

    def test_typed_aquarius_against_node_ratio(self):
        titles = {"aquarius_typed": "星泉（型別）", "node": "Node.js"}
        view = {"benchmarks": {"fibonacci": {"n": 1}, "sieve": {"n": 2}}, "cases": {
            "fibonacci/aquarius_typed": {"summary": {"status": "ok", "median_ms": 2.0}},
            "fibonacci/node": {"summary": {"status": "ok", "median_ms": 8.0}},
            "sieve/aquarius_typed": {"summary": {"status": "ok", "median_ms": 4.0}},
            "sieve/node": {"summary": {"status": "ok", "median_ms": 2.0}}}}
        lines = "\n".join(typed_vs_node_lines(view, titles, "暖機模式", "tw"))
        self.assertIn("| 4.00 倍 | 星泉（型別） 快 4.00 倍 |", lines)
        self.assertIn("| 0.50 倍 | Node.js 快 2.00 倍 |", lines)
        self.assertIn("**1.41 倍**", lines)  # Geometric mean of 4 and 0.5.
        english = "\n".join(typed_vs_node_lines(view, {"aquarius_typed": "AquariusLang (typed)", "node": "Node.js"},
                                                 "warmed mode", "en"))
        self.assertIn("| 4.00× | AquariusLang (typed), 4.00× faster |", english)
        self.assertIn("| 0.50× | Node.js, 2.00× faster |", english)
        self.assertIn("| **Geometric mean** | | | | **1.41×** |", english)
        view["cases"]["sieve/node"]["summary"] = {"status": "failed"}
        lines = "\n".join(typed_vs_node_lines(view, titles, "暖機模式", "tw"))
        self.assertIn("失敗", lines)
        self.assertNotIn("幾何平均", lines)
        self.assertEqual(typed_vs_node_lines(view, {"node": "Node.js"}, "暖機模式", "tw"), [])

    def test_composite_score_uses_equal_weight_geometric_mean(self):
        report = {"benchmarks": {"first": {}, "second": {}}, "cases": {}}
        for name, times in [("first", {"python": 10, "node": 5, "aquarius": 40}),
                            ("second", {"python": 1000, "node": 2000, "aquarius": 4000})]:
            for language, duration in times.items():
                report["cases"][f"{name}/{language}"] = {
                    "summary": {"status": "ok", "median_ms": duration}}
        scores = composite_scores(report)
        self.assertAlmostEqual(scores["python"], 100)
        self.assertAlmostEqual(scores["node"], 100)
        self.assertAlmostEqual(scores["aquarius"], 25)
        report["cases"]["second/node"]["summary"]["status"] = "failed"
        self.assertIsNone(composite_scores(report))

    def test_fastest_language_is_always_normalized_to_100(self):
        for fastest in ["node", "aquarius", "python", "csharp"]:
            with self.subTest(fastest=fastest):
                times = {"python": 10, "node": 20, "aquarius": 40, "csharp": 30}
                times[fastest] = 5
                report = {"benchmarks": {"first": {}}, "cases": {
                    f"first/{language}": {"summary": {"status": "ok", "median_ms": duration}}
                    for language, duration in times.items()}}
                scores = composite_scores(report)
                self.assertEqual(max(scores.values()), 100)
                self.assertEqual(scores[fastest], 100)
                for language, duration in times.items():
                    self.assertAlmostEqual(scores[language], 100 * 5 / duration)

    def test_four_language_scores_require_every_csharp_case(self):
        report = {"benchmarks": {"first": {}, "second": {}},
                  "runtimes": {language: {} for language in ["aquarius", "python", "node", "csharp"]},
                  "cases": {}}
        for name, factor in [("first", 1), ("second", 100)]:
            for language, duration in {"python": 10, "node": 5, "aquarius": 40, "csharp": 20}.items():
                report["cases"][f"{name}/{language}"] = {
                    "summary": {"status": "ok", "median_ms": duration * factor}}
        scores = composite_scores(report)
        self.assertAlmostEqual(scores["csharp"], 25)
        self.assertEqual(set(scores), set(report["runtimes"]))
        report["cases"]["second/csharp"]["summary"]["status"] = "failed"
        self.assertIsNone(composite_scores(report))
        del report["cases"]["second/csharp"]
        self.assertIsNone(composite_scores(report))


if __name__ == "__main__":
    unittest.main()
