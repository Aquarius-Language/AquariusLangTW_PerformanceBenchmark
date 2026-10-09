import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from reference import expected
from run_benchmarks import ROOT, execute, generate_readme, parse_result, summarize


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
                observed = parse_result(output)
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
        self.assertEqual(self.run_child("print('RESULT 7')")["status"], "ok")
        self.assertEqual(self.run_child("print('RESULT 8')")["status"], "invalid")
        self.assertEqual(self.run_child("print('RESULT 7'); raise SystemExit(2)")["status"], "invalid")
        self.assertEqual(self.run_child("import time; time.sleep(2)", timeout=0.05)["status"], "timeout")

    def test_float_tolerance(self):
        spec = {"relative_tolerance": 1e-9, "absolute_tolerance": 1e-12}
        self.assertEqual(self.run_child("print('RESULT 1.0000000001')", 1.0, spec)["status"], "ok")
        self.assertEqual(self.run_child("print('RESULT 1.001')", 1.0, spec)["status"], "invalid")

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
                                   "--repetitions", "1", "--aquarius", str(path / "missing-runtime.exe"),
                                   "--node", str(path / "missing-node.exe"),
                                   "--output-dir", str(path / "results"), "--readme", str(path / "README.md")],
                                  capture_output=True, text=True, timeout=30)
            self.assertEqual(proc.returncode, 1, proc.stderr)
            report = json.loads((path / "results/latest.json").read_text(encoding="utf-8"))
            self.assertEqual(report["cases"]["fibonacci/aquarius"]["summary"]["status"], "unavailable")
            self.assertEqual(report["cases"]["fibonacci/python"]["summary"]["status"], "ok")
            self.assertIn("UNAVAILABLE", generate_readme(report))
            before = (path / "README.md").read_bytes()
            subprocess.run([sys.executable, str(ROOT / "run_benchmarks.py"), "--report-only",
                            str(path / "results/latest.json"), "--readme", str(path / "README.md")],
                           check=True, capture_output=True, timeout=30)
            self.assertEqual((path / "README.md").read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
