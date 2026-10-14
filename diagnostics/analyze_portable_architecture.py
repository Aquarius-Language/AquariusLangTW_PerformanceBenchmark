"""Validate the preserved evidence and regenerate the portable architecture diagnosis."""
import hashlib
import json
import math
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "results" / "architecture-improvement" / "20261015"
LANGUAGE = ROOT.parent / "AquariusLangTW"


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def gm(values):
    return math.exp(sum(map(math.log, values)) / len(values))


def trx(path):
    counters = ET.parse(path).find(".//{http://microsoft.com/schemas/VisualStudio/TeamTest/2010}Counters")
    row = {key: int(value) for key, value in counters.attrib.items()}
    assert row["total"] == row["passed"] and row["failed"] == 0, (path, row)
    return row["passed"]


def node_tests(path):
    log = path.read_text(encoding="utf-8-sig")
    total = int(re.search(r"tests (\d+)\s*$", log, re.M)[1])
    passed = int(re.search(r"pass (\d+)\s*$", log, re.M)[1])
    assert total == passed and re.search(r"fail 0\s*$", log, re.M) and re.search(r"skipped 0\s*$", log, re.M)
    return passed


def main():
    before = read(EVIDENCE / "before" / "latest.json")
    after = read(EVIDENCE / "after-final" / "latest.json")
    paired = read(EVIDENCE / "paired.json")
    idiomatic = read(EVIDENCE / "idiomatic-python.json")
    profile = read(EVIDENCE / "counters.json")
    backup = read(EVIDENCE / "before" / "backup-manifest.json")
    sources = read(EVIDENCE / "source-changes.json")
    assert digest(EVIDENCE / "before" / "README.md") == backup["readme_sha256"]
    assert digest(EVIDENCE / "before" / "latest.json") == backup["latest_sha256"]
    assert read(ROOT / "results" / "latest.json") == after
    assert paired["valid"]
    for report in (after, paired, idiomatic):
        assert all(case["summary"]["status"] == "ok" for case in report["cases"].values())
    for name in before["benchmarks"]:
        assert before["benchmarks"][name]["n"] == after["benchmarks"][name]["n"]
        for language in ("aquarius", "python", "node"):
            assert before["cases"][name + "/" + language]["source_sha256"] == after["cases"][name + "/" + language]["source_sha256"]
        assert paired["cases"][name + "/before"]["source_sha256"] == paired["cases"][name + "/after"]["source_sha256"]
    for file in sources["files"]:
        assert digest(LANGUAGE / file["path"]) == file["after_sha256"], file["path"]
        if file["before_sha256"] is not None:
            assert digest(EVIDENCE / "source-before" / file["path"]) == file["before_sha256"], file["path"]
    for release, metadata in (("before", before["runtimes"]["aquarius"]), ("after", after["runtimes"]["aquarius"])):
        executable = Path(metadata["executable"])
        assert digest(executable) == metadata["executable_sha256"], release
        for assembly, fingerprint in metadata["assemblies_sha256"].items():
            assert digest(executable.parent / assembly) == fingerprint, (release, assembly)
    tests = {
        "Complete language suite (all native/graphics flags enabled; serialized collections)": trx(EVIDENCE / "tests" / "all-tests.trx"),
        "Browser/WebAssembly suite": node_tests(EVIDENCE / "tests" / "web-tests.log"),
        "Language server suite": node_tests(EVIDENCE / "tests" / "lsp-tests.log"),
        "Final application host and scalar subset (additional rerun)": trx(EVIDENCE / "tests" / "packaged-tests.trx"),
    }
    harness = (EVIDENCE / "tests" / "benchmark-harness.log").read_text(encoding="utf-8-sig")
    assert "Ran 15 tests" in harness and harness.rstrip().endswith("OK") and "skipped=" not in harness
    tests["Benchmark harness with real compiler integration"] = 15
    comparisons = paired["comparison"]
    ratios = {name: idiomatic["cases"][name + "/aquarius"]["summary"]["median_ms"] /
              idiomatic["cases"][name + "/python_idiomatic"]["summary"]["median_ms"] for name in comparisons}
    idiomatic_ratio = gm(list(ratios.values()))
    published_speedup = gm([before["cases"][name + "/aquarius"]["summary"]["median_ms"] /
                            after["cases"][name + "/aquarius"]["summary"]["median_ms"] for name in comparisons])
    samples = lambda report: sum(len(case["samples"]) + len(case["warmups"]) for case in report["cases"].values())
    metrics = {
        "paired_speedup": paired["geometric_mean_speedup"], "published_speedup": published_speedup,
        "paired_time_reduction_percent": 100 * (1 - 1 / paired["geometric_mean_speedup"]),
        "paired_after_over_python_time": paired["after_over_python"],
        "idiomatic_after_over_python_time": idiomatic_ratio,
        "test_pass_counts": tests,
        "validated_executions": {"standard": samples(after), "paired": samples(paired), "idiomatic_diagnosis": samples(idiomatic), "counter_profile": len(profile["rows"])},
        "source_manifest_verified": True, "original_backup_verified": True,
    }
    (EVIDENCE / "diagnosis.json").write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    rows = [f"| {before['benchmarks'][name]['title']} | {row['before']:.3f} | {row['after']:.3f} | {row['speedup']:.2f}× |"
            for name, row in comparisons.items()]
    python_rows = [f"| {before['benchmarks'][name]['title']} | {idiomatic['cases'][name+'/aquarius']['summary']['median_ms']:.3f} | {idiomatic['cases'][name+'/python_idiomatic']['summary']['median_ms']:.3f} | {ratios[name]:.2f}× |"
                   for name in comparisons]
    test_rows = [f"| {name} | {count:,} | 0 | 0 |" for name, count in tests.items()]
    counter_rows = []
    for name in ("fibonacci", "ackermann", "spectral_norm", "matrix", "binary_trees"):
        old = profile["rows"][name + "/before"]
        new = profile["rows"][name + "/after"]
        c = new["counters"]
        counter_rows.append(f"| {name} | {old['run_entries']} → {new['run_entries']} | {c['aqua_numeric_fast_calls']:,} | {c['aqua_numeric_fallback_calls']:,} | {c['aqua_numeric_depth_fallbacks']} |")
    report = f"""# Portable architecture performance diagnosis

October 15, 2026, Asia/Taipei. Final code and rebuilt release; unchanged algorithms.

Aquarius is **{paired['geometric_mean_speedup']:.2f}× faster than its original release** across the ten
workloads in the interleaved comparison, reducing aggregate geometric-mean workload
time by **{metrics['paired_time_reduction_percent']:.1f}%**. Fibonacci improves
**{comparisons['fibonacci']['speedup']:.1f}×**, matrix multiplication
**{comparisons['matrix']['speedup']:.1f}×**, and Mandelbrot
**{comparisons['mandelbrot']['speedup']:.1f}×**. Every new median is at least as fast in this paired run;
Ackermann is essentially unchanged, and the small tree difference is not a large gain.

On the existing matched-semantics suite Aquarius now has **{1/paired['after_over_python']:.2f}× Python's
geometric-mean speed**. Against the separate idiomatic Python variants, Aquarius
still takes **{idiomatic_ratio:.3f}× as long overall** ({100*(idiomatic_ratio-1):.1f}% slower).
The implementation improves the architecture substantially; it does not establish
universal superiority over Python or optimized native libraries.

## What changed

The implemented portable portion of the [architecture proposal](PERFORMANCE_ARCHITECTURE.md)
selects an execution representation according to the function's proven behavior:

- Closed, effect-free scalar functions use resolved Wasm locals, structured control
  flow and private typed calling conventions. A successful call needs no guest
  lexical scope or language frame. Mixed numeric helpers retain tag/payload registers.
- A control-flow/type proof gives integer-only functions untagged `i32` locals and
  direct integer recursive calls. Checked `i64` arithmetic preserves Aquarius overflow
  conversion; division guards zero and minimum-integer divided by minus one.
- Recursive target identity, argument type/payload, initialization, fuel and depth
  guards retain the generic path when assumptions fail. Failed pure speculation
  restores its original budget before generic execution, preserving call state at
  an observable yield. Deep recursion disables repeated speculative entry.
- The compiler resolves candidate bindings through enclosing lexical scopes.
  Capture, count and name guards retain dynamic lookup after host insertion,
  closure mutation, conditional declarations or shadowing.

These are shared compiler/Wasm changes. No operating-system-specific fast path,
CPU-specific backend, engine tuning, algorithm rewrite, Boolean short-circuit
change or floating-point reassociation is introduced. General arrays still hold
tagged elements. Full SSA, typed array storage, capture cells and materialized
optimized continuations remain future architectural work.

See the language's [implementation notes]({(LANGUAGE/'docs/portable-numeric-architecture.md').as_posix()}).
The external capability ABI remains version 2. New artifacts use 32-byte function
definitions and require the rebuilt hosts. Current hosts retain compatibility with
older ABI 2 artifacts that use the original 24-byte layout.

## Old versus new under the same conditions

Each benchmark uses one warmup and nine measured repetitions for four variants:
preserved Aquarius, new Aquarius, CPython and Node. Their execution order is shuffled
each round. Aquarius programs are compiled before timing; the workload timer includes
initialization and computation, and excludes process startup, initial compilation
and output. This is not a startup-performance measurement. Source hashes, inputs,
checksums and tolerances match across old/new cases.

| Workload | Original median ms | New median ms | Original / new speed |
| --- | ---: | ---: | ---: |
{chr(10).join(rows)}

The normal published suite independently shows **{published_speedup:.2f}×** improvement
against the preserved published medians. The original publication used five measured
repetitions; the new publication uses nine. The interleaved result above is preferred
for attributing gains because it measures both releases in the same run.
All **{samples(after)}** normal-suite executions and **{samples(paired)}** paired executions
passed their reference checks. Environment details and executable/Core/engine
fingerprints are retained in the raw JSON reports.

## Why the improvements differ

Counter collection runs separately from timing. It executes both old and new
artifacts on the final host, checks their results, and observes guest exports.
Fast-call counts include successful adapter entries; internal direct recursive
calls are not counted individually. Run entries are scheduler invocations, not
instruction counts or CPU-time shares.

| Workload | Scheduler entries old → new | Successful scalar entries | Failed attempts | Depth failures |
| --- | ---: | ---: | ---: | ---: |
{chr(10).join(counter_rows)}

Fibonacci benefits from avoiding repeated tag checks, numeric normalization,
scope allocation and frame dispatch inside integer recursion. Fuel guards still
require some resumable execution; the new path does not skip scheduler checks.
Ackermann reaches the direct-call depth limit once and then stays stackless, so
it retains nearly all of its original costs. Spectral norm's scalar coefficient
helper uses the typed adapter 144,000 times, with no failed attempts in this profile.

Matrix and Mandelbrot have zero scalar adapter entries. Their substantial gains
come from resolved ancestor bindings in nested loops. Quicksort, N-Queens and
Collatz also retain generic functions/loops and receive smaller binding gains.
Binary trees allocate arrays and return heap objects, so their recursive functions
are ineligible for scalar execution. The guest heap high-water remains approximately
2.11 MB; these measurements do not show allocation-churn elimination for tree code.

An initial tag/payload recursive implementation regressed Fibonacci from about
104 ms to 251 ms in the paired trial. That trial is preserved. The final implementation
adds proven integer representation and keeps recursive noninteger arguments on the
resumable path. The final paired Fibonacci result is {comparisons['fibonacci']['after']:.3f} ms.

## The remaining Python gap

The existing Python suite deliberately mirrors Aquarius's copy-and-append setup.
The additional diagnostic replaces those Python constructions with `append` or
preallocation in five workloads, retaining algorithm inputs and reference results.
It also retains separate inlining/predicate experiments; those modified Aquarius
variants are not included in the production score or old/new improvement claim.

| Workload | New Aquarius ms | Idiomatic Python ms | Aquarius / Python time |
| --- | ---: | ---: | ---: |
{chr(10).join(python_rows)}

Lower ratios are better. The remaining overall ratio is **{idiomatic_ratio:.3f}×**.
The strongest next portable steps are:

1. Materialize optimized continuations at fuel/depth boundaries, allowing deep
   recursive functions such as Ackermann to keep typed values across resumptions.
   Increasing depth or changing the scheduling contract would not solve that safely.
2. Introduce homogeneous array backing storage with mutation/alias guards, and
   avoid physical copy-and-append when ownership proves the old contents cannot be
   observed. Keep the public copy/alias behavior unchanged.
3. Extend resolved values and type/effect analysis through loop regions and known
   callees, so N-Queens predicates, Quicksort and spectral loops stop paying generic
   operand-stack and binding costs for their stable scalar state.
4. Apply escape analysis/scalar replacement to temporary tree objects, followed
   by allocator work for objects that still escape. Changing the tree benchmark's
   algorithm would not be a language-runtime improvement.

These explain the measured gaps; they are not claimed as implemented speedups.
Idiomatic diagnostics validated **{samples(idiomatic)}** executions, and the separate
counter pass validated **{len(profile['rows'])}** executions.

## Correctness and build verification

| Suite | Passed | Failed | Skipped |
| --- | ---: | ---: | ---: |
{chr(10).join(test_rows)}

Differential tests compare optimized and generic execution over 1,452 mixed-type
operator pairs and 324 integer boundary pairs, plus return/type/error behavior,
overflow, nonfinite values, division, compound assignment, eager Boolean evaluation,
duplicate parameters, conditional locals, captured scope mutation, self-rebinding,
deep recursion and a recursive-binding mutation during a yield. Browser tests
exercise the same artifact on JavaScript WebAssembly, including integer arithmetic,
depth/fuel fallback and old metadata compatibility. This is broad regression evidence,
not a formal proof for every possible program.

The pinned Zig 0.15.1 source/binary check passed. The compiler and existing application
host were rebuilt from the changed source, and the 52-test packaged/scalar subset
was rerun with the final runtime pack. The first parallel native run encountered a
window-creation race; the final full run serialized collections and passed every test.
One added counter assertion was corrected to account for accumulation between executions.
No production window behavior or scheduling limit was changed to make tests pass.

## Preserved evidence and reproduction

- [Original performance backup](../results/architecture-improvement/20261015/before/README.md),
  [original raw results](../results/architecture-improvement/20261015/before/latest.json),
  and [backup fingerprints](../results/architecture-improvement/20261015/before/backup-manifest.json).
- [Published new report](../README.md),
  [new raw results](../results/architecture-improvement/20261015/after-final/latest.json),
  [paired results](../results/architecture-improvement/20261015/paired.json),
  [paired CSV](../results/architecture-improvement/20261015/paired.csv),
  and [idiomatic Python diagnosis](../results/architecture-improvement/20261015/idiomatic-python.json).
- [Counter profile](../results/architecture-improvement/20261015/counters.json),
  [initial regression trial](../results/architecture-improvement/20261015/paired-initial.json),
  [source before/after fingerprints](../results/architecture-improvement/20261015/source-changes.json),
  and [test evidence](../results/architecture-improvement/20261015/tests/all-tests.trx).
- [Machine-readable diagnosis](../results/architecture-improvement/20261015/diagnosis.json).

Final compiler: [aqua.exe]({Path(after['runtimes']['aquarius']['executable']).as_posix()}).
Original release and original edited source files remain preserved. The large old
application host backup remains on disk under `source-before/runtime-pack/host.exe`
and is excluded from Git tracking.

Regenerate and revalidate this diagnosis with:

```powershell
python diagnostics/analyze_portable_architecture.py
```

Repeat the same old/new experiment using the recorded executable paths and
`diagnostics/compare_performance.py --before ORIGINAL --after FINAL --output NEW_JSON --repetitions 9`.
The counter profiler source is in `diagnostics/architecture-profile`; build it with
the final release directory as the `AquariusRelease` MSBuild property, then run it
with before/after artifact folders, original results JSON and an output JSON path.
"""
    (ROOT / "diagnostics" / "PORTABLE_ARCHITECTURE_RESULTS.md").write_text(report, encoding="utf-8")
    print(f"Verified source and backups; {paired['geometric_mean_speedup']:.3f}x speedup; idiomatic Python time ratio {idiomatic_ratio:.3f}x.")


if __name__ == "__main__":
    main()
