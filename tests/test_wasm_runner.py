import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from run_benchmarks import ROOT, runtime_info

class WasmRunnerTests(unittest.TestCase):
    def test_fingerprints_core_and_engine_instead_of_legacy_assemblies(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            executable = path / 'aqua.exe'
            executable.write_bytes(b'compiler')
            for name in ['AquariusCore.dll', 'AquariusDesktop.dll', 'Wasmtime.Dotnet.dll', 'wasmtime.dll']:
                (path / name).write_bytes(name.encode())
            info = runtime_info('aquarius', str(executable))
            self.assertEqual(info['backend'], 'compiled-wasm')
            self.assertEqual(set(info['assemblies_sha256']), {'AquariusCore.dll', 'AquariusDesktop.dll', 'Wasmtime.Dotnet.dll', 'wasmtime.dll'})

    @unittest.skipUnless(os.environ.get('AQUARIUS_COMPILER_EXE'), 'Set AQUARIUS_COMPILER_EXE for the current compiler integration check')
    def test_precompiled_mode_builds_before_timing_and_validates_real_wasm_result(self):
        work = ROOT / '.benchmark-work'
        work.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=work) as directory:
            path = Path(directory)
            result = subprocess.run([sys.executable, str(ROOT / 'run_benchmarks.py'), '--profile', 'smoke', '--benchmarks', 'fibonacci', '--repetitions', '1', '--warmups', '0', '--aquarius', os.environ['AQUARIUS_COMPILER_EXE'], '--aquarius-mode', 'precompiled', '--output-dir', str(path / 'results'), '--readme', str(path / 'README.md')], capture_output=True, text=True, encoding='utf-8', timeout=60)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            report = json.loads((path / 'results/latest.json').read_text(encoding='utf-8'))
            case = report['cases']['fibonacci/aquarius']
            self.assertEqual(case['build']['command'][1], 'build')
            self.assertEqual(case['build']['exit_code'], 0)
            self.assertEqual(case['command'][1], 'run')
            self.assertEqual(case['summary']['status'], 'ok')
            self.assertEqual(len(case['wasm_sha256']), 64)
            self.assertEqual(report['runtimes']['aquarius']['backend'], 'compiled-wasm')
            self.assertIn('Wasm', (path / 'README.md').read_text(encoding='utf-8'))
