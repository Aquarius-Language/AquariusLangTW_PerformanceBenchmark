"""English and 繁體中文 READMEs and the cross-benchmark composite scores. Uses only the measurements in the report.

Both READMEs come from the same code: every sentence is written once in each language with `tr(tw, en)`.
"""
import math
from itertools import combinations
from pathlib import Path

LANGUAGES = {
    "tw": {"aquarius": "星泉", "aquarius_typed": "星泉（型別）", "python": "Python", "node": "Node.js", "csharp": "C#"},
    "en": {"aquarius": "AquariusLang", "aquarius_typed": "AquariusLang (typed)", "python": "Python", "node": "Node.js",
           "csharp": "C#"},
}
WORKLOADS = {
    "fibonacci": (("遞迴費波那契", "使用樸素遞迴，不使用記憶化。"),
                  ("Recursive Fibonacci", "Naive recursion, no memoization.")),
    "ackermann": (("阿克曼函數", "計算 A(3, n)，測試巢狀遞迴呼叫。"),
                  ("Ackermann function", "Computes A(3, n), exercising nested recursive calls.")),
    "sieve": (("埃拉托斯特尼篩法", "使用布林陣列，計算 2 至 n（含）的質數數量。"),
              ("Sieve of Eratosthenes", "Counts the primes from 2 to n (inclusive) with a Boolean array.")),
    "quicksort": (("快速排序", "以中間元素為樞紐，原地排序固定種子的線性同餘序列；檢查排序順序與加權校驗值。"),
                  ("Quicksort", "Sorts a fixed-seed linear congruential sequence in place with the middle element as "
                                "pivot; checks the order and a weighted checksum.")),
    "matrix": (("矩陣乘法", "使用列優先的一維陣列與 i/j/k 三層迴圈，計算結果矩陣所有元素的總和。"),
               ("Matrix multiplication", "Row-major one-dimensional arrays and an i/j/k triple loop; sums every "
                                         "element of the result matrix.")),
    "mandelbrot": (("曼德布洛特集合", "在 [-2, 1) × [-1, 1) 上取 n × n 個點，最多迭代 60 次，累計逃逸迭代次數。"),
                   ("Mandelbrot set", "Samples n × n points over [-2, 1) × [-1, 1) with at most 60 iterations and "
                                      "sums the escape iteration counts.")),
    "nqueens": (("N 皇后問題", "以回溯法逐一檢查欄與對角線，計算所有解的數量。"),
                ("N-Queens", "Counts every solution by backtracking, checking columns and diagonals.")),
    "binary_trees": (("二元樹", "建立八棵深度為 n 的完整二元樹，並遞迴計算節點總數。"),
                     ("Binary trees", "Builds eight complete binary trees of depth n and counts their nodes "
                                      "recursively.")),
    "spectral_norm": (("譜範數", "對隱式矩陣執行十輪冪次迭代，輸出譜範數平方，避免使用函式庫平方根。"),
                      ("Spectral norm", "Runs ten power iterations on an implicit matrix and prints the squared "
                                        "spectral norm, avoiding a library square root.")),
    "collatz": (("考拉茲猜想", "累計起始整數 1 至 n 到達 1 的步數，不使用記憶化。"),
                ("Collatz conjecture", "Sums the steps for each start from 1 to n to reach 1, no memoization.")),
}
STATUS = {"tw": {"ok": "通過", "failed": "失敗", "incomplete": "未完成", "unavailable": "無法使用"},
          "en": {"ok": "passed", "failed": "failed", "incomplete": "incomplete", "unavailable": "unavailable"}}
MODE_NAMES = {"tw": {"standard": "標準模式", "warmed": "暖機模式"},
              "en": {"standard": "standard mode", "warmed": "warmed mode"}}
PROFILES = {"tw": {"standard": "標準", "smoke": "快速檢查", "large": "大型"},
            "en": {"standard": "standard", "smoke": "smoke check", "large": "large"}}
LIST_SEPARATOR = {"tw": "、", "en": ", "}
CLAUSE_SEPARATOR = {"tw": "；", "en": "; "}


def translator(lang):
    """`tr(tw, en)` picks the sentence for the README being written."""
    return (lambda tw, en: tw) if lang == "tw" else (lambda tw, en: en)


def workload(name, lang):
    return WORKLOADS[name][0 if lang == "tw" else 1]


def report_languages(report, lang="en"):
    """Keep old reports usable without inventing C# measurements for them."""
    present = report.get("runtimes")
    if present is None:
        present = {key.split("/")[1] for key in report["cases"]}
    return {language: title for language, title in LANGUAGES[lang].items() if language in present}


def mode_views(report):
    """Split a report into (mode, parameters, single-mode report keyed `benchmark/language`).

    Reports before schema 4 measured one mode, labelled from their configuration.
    """
    config = report["config"]
    modes = config.get("modes")
    if not modes:
        warmups = config.get("in_process_warmups", 0)
        return [("warmed" if warmups else "standard", {"in_process_warmups": warmups, "in_process_runs": 1}, report)]
    views = []
    for mode, params in modes.items():
        cases = {key.rsplit("/", 1)[0]: record for key, record in report["cases"].items() if record.get("mode") == mode}
        views.append((mode, params, {**report, "cases": cases}))
    return views


def mode_title(mode, params, lang):
    tr = translator(lang)
    if mode == "standard":
        return tr("標準模式（冷啟動，每個程序計時一次）", "Standard mode (cold start, one timed run per process)")
    warmups, runs = params["in_process_warmups"], params["in_process_runs"]
    if lang == "tw":
        timed = f"再計時 {runs} 次取中位數" if runs > 1 else "再計時 1 次"
        return f"暖機模式（程序內先暖機 {warmups} 次，{timed}）"
    timed = f"then the median of {runs} timed runs" if runs > 1 else "then 1 timed run"
    return f"Warmed mode ({warmups} in-process warm-up {'run' if warmups == 1 else 'runs'}, {timed})"


def mode_method(mode, params, config, has_csharp, lang):
    tr = translator(lang)
    jit = (tr("C# 與 ", "C# and ") if has_csharp else "") + "Node.js"
    repetitions = config["repetitions"]
    if mode == "standard":
        return tr("每個程序只執行一次工作負載並計時，不在程序內暖機，與最初的設計相同。"
                  f"{jit} 的 JIT 編譯與最佳化落在計時區間內，星泉的 Wasm 則已在計時前由 Wasmtime 編譯完成，"
                  "因此此模式反映短程式從程序啟動後第一次執行的表現。"
                  f"每組的值為 {repetitions} 個程序計時值的中位數。",
                  "Each process runs and times the workload once, with no in-process warm-up, as in the original "
                  f"design. The JIT compilation and optimization of {jit} fall inside the timed interval, while "
                  "Wasmtime has already compiled the AquariusLang Wasm before timing starts, so this mode reflects "
                  "a short program's first run after process start. "
                  f"Each value is the median of {repetitions} process timings.")
    warmups, runs = params["in_process_warmups"], params["in_process_runs"]
    if lang == "tw":
        per_process = (f"再於同一程序內連續計時 {runs} 次，該程序的值為這 {runs} 次的中位數"
                       if runs > 1 else "再計時 1 次")
        return (f"每個程序先在同一程序內不計時執行同一工作負載 {warmups} 次，讓 {jit} 的 JIT 在計時前完成最佳化，"
                f"{per_process}；每組的值為 {repetitions} 個程序值的中位數。各語言的暖機與計時次數相同。")
    per_process = (f"then times {runs} consecutive runs in the same process and takes their median as the process "
                   "value" if runs > 1 else "then times 1 run")
    return (f"Each process first runs the same workload {warmups} times untimed in the same process so the JIT of "
            f"{jit} finishes optimizing before timing, {per_process}; each value is the median of {repetitions} "
            "process values. Every language gets the same warm-up and timed run counts.")


def composite_scores(report):
    """各演算法的相對速度等權重取幾何平均，再將最快語言正規化為 100。"""
    languages = report_languages(report)
    if not report["benchmarks"] or "python" not in languages:
        return None
    for name in report["benchmarks"]:
        for language in languages:
            summary = report["cases"].get(f"{name}/{language}", {}).get("summary", {})
            value = summary.get("median_ms", 0)
            if summary.get("status") != "ok" or not math.isfinite(value) or value <= 0:
                return None
    log_speeds = {}
    for language in languages:
        log_ratios = [math.log(report["cases"][f"{name}/python"]["summary"]["median_ms"]) -
                      math.log(report["cases"][f"{name}/{language}"]["summary"]["median_ms"])
                      for name in report["benchmarks"]]
        log_speeds[language] = sum(log_ratios) / len(log_ratios)
    fastest = max(log_speeds.values())
    return {language: 100 * math.exp(speed - fastest) for language, speed in log_speeds.items()}


def md(value):
    return str(value).replace("|", "\\|").replace("\n", " ").replace("\r", " ")


def times(value, digits, lang):
    return f"{value:.{digits}f} 倍" if lang == "tw" else f"{value:.{digits}f}×"


def score_summary(scores, languages, lang):
    tr = translator(lang)
    return LIST_SEPARATOR[lang].join(tr(f"{languages[language]} {scores[language]:.2f} 分",
                                        f"{languages[language]} {scores[language]:.2f}")
                                     for language in sorted(scores, key=scores.get, reverse=True))


def score_lines(view, languages, lang):
    tr = translator(lang)
    scores = composite_scores(view)
    if not scores:
        return [tr(f"**本模式資料不足以計算 {len(languages)} 種語言的綜合分數。** 至少一項測試失敗、未完成或執行環境無法使用；"
                   "各項測試狀態列於下表。",
                   f"**This mode lacks the data for a composite score of all {len(languages)} languages.** At least "
                   "one test failed, did not finish, or had no runtime available; the tables below list each test's "
                   "status."), ""]
    ranking = sorted(scores, key=scores.get, reverse=True)
    comparisons = CLAUSE_SEPARATOR[lang].join(
        tr(f"{languages[faster]} 的綜合速度是 {languages[slower]} 的 {scores[faster] / scores[slower]:.2f} 倍",
           f"{languages[faster]} is {scores[faster] / scores[slower]:.2f}× as fast as {languages[slower]}")
        for faster, slower in combinations(ranking, 2))
    lines = [tr(f"**綜合效能：{score_summary(scores, languages, lang)}（越高越快）。**",
                f"**Composite performance: {score_summary(scores, languages, lang)} (higher is faster).**"), "",
             tr(f"綜合速度兩兩比較：{comparisons}。", f"Pairwise composite speed: {comparisons}."), "",
             tr("| 排名 | 程式語言 | 綜合分數 | ", "| Rank | Language | Composite score | ") +
             " | ".join(tr(f"相對 {languages[language]} 的速度", f"Speed vs {languages[language]}")
                        for language in ranking) + " |",
             "| ---: | --- | ---: | " + " | ".join("---:" for _ in ranking) + " |"]
    for place, language in enumerate(ranking, 1):
        speeds = " | ".join(times(scores[language] / scores[baseline], 3, lang) for baseline in ranking)
        lines.append(f"| {place} | {languages[language]} | {scores[language]:.2f} | {speeds} |")
    return lines + [""]


def median_lines(view, languages, short, lang):
    tr = translator(lang)
    lines = [tr(f"### 各項效能結果（{short}）", f"### Results per benchmark ({short})"), "",
             tr("耗時單位為毫秒（ms），越低越快。耗時倍率 = 該語言耗時中位數 ÷ Python 耗時中位數；"
                "小於 1 表示該項測試比 Python 快。此耗時倍率與綜合分數的方向相反。",
                "Times are in milliseconds (ms); lower is faster. Time ratio = the language's median time ÷ Python's "
                "median time; below 1 means that test ran faster than Python. This ratio points the opposite way "
                "from the composite score."), "",
             tr("| 演算法 | n | ", "| Benchmark | n | ") +
             " | ".join(tr(f"{title} 中位數", f"{title} median") for title in languages.values()) + " | " +
             " | ".join(tr(f"{title}／Python 耗時倍率", f"{title} / Python time ratio")
                        for language, title in languages.items() if language != "python") + " |",
             "| --- | ---: | " + " | ".join("---:" for _ in range(2 * len(languages) - 1)) + " |"]
    for name, spec in view["benchmarks"].items():
        summaries = {language: view["cases"][f"{name}/{language}"]["summary"] for language in languages}
        cells = [f"{s['median_ms']:.3f}" if s["status"] == "ok" else STATUS[lang].get(s["status"], s["status"])
                 for s in summaries.values()]

        def ratio(language):
            s, py = summaries[language], summaries["python"]
            return times(s["median_ms"] / py["median_ms"], 2, lang) if s["status"] == py["status"] == "ok" else "—"
        lines.append(f"| {workload(name, lang)[0]} | {spec['n']} | " + " | ".join(cells) +
                     " | " + " | ".join(ratio(language) for language in languages if language != "python") + " |")
    return lines + [""]


def typed_vs_node_lines(view, languages, short, lang):
    """The project's goal: typed AquariusLang against Node.js, benchmark by benchmark."""
    if not {"aquarius_typed", "node"} <= set(languages):
        return []
    tr = translator(lang)
    typed_title = languages["aquarius_typed"]
    lines = [f"### {typed_title} vs Node.js（{short}）" if lang == "tw" else f"### {typed_title} vs Node.js ({short})", "",
             tr("倍率 = Node.js 耗時中位數 ÷ 星泉（型別）耗時中位數；大於 1 表示星泉（型別）較快，小於 1 表示 Node.js 較快。",
                "Ratio = Node.js median time ÷ AquariusLang (typed) median time; above 1 means AquariusLang (typed) "
                "is faster, below 1 means Node.js is faster."), "",
             tr(f"| 演算法 | n | {typed_title} 中位數 | Node.js 中位數 | Node.js ÷ {typed_title} | 較快者 |",
                f"| Benchmark | n | {typed_title} median | Node.js median | Node.js ÷ {typed_title} | Faster |"),
             "| --- | ---: | ---: | ---: | ---: | --- |"]

    def faster(value):
        if value > 1:
            return tr(f"{typed_title} 快 {value:.2f} 倍", f"{typed_title}, {value:.2f}× faster")
        return tr(f"Node.js 快 {1 / value:.2f} 倍", f"Node.js, {1 / value:.2f}× faster")
    logs = []
    for name, spec in view["benchmarks"].items():
        typed = view["cases"][f"{name}/aquarius_typed"]["summary"]
        node = view["cases"][f"{name}/node"]["summary"]
        cells = [f"{s['median_ms']:.3f}" if s["status"] == "ok" else STATUS[lang].get(s["status"], s["status"])
                 for s in (typed, node)]
        ratio, winner = "—", "—"
        if typed["status"] == node["status"] == "ok":
            value = node["median_ms"] / typed["median_ms"]
            logs.append(math.log(value))
            ratio, winner = times(value, 2, lang), faster(value)
        lines.append(f"| {workload(name, lang)[0]} | {spec['n']} | {cells[0]} | {cells[1]} | {ratio} | {winner} |")
    if logs and len(logs) == len(view["benchmarks"]):
        mean = math.exp(sum(logs) / len(logs))
        lines.append(tr("| **幾何平均** |", "| **Geometric mean** |") + f" | | | **{times(mean, 2, lang)}** | " +
                     faster(mean) + " |")
    return lines + [""]


def variability_lines(view, languages, short, repetitions, lang):
    tr = translator(lang)
    lines = [tr(f"### 耗時波動（{short}）", f"### Timing variability ({short})"), "",
             tr("變異係數（CV）= 程序值的樣本標準差 ÷ 平均值。只有一筆樣本時，無法估計波動，以破折號表示。",
                "Coefficient of variation (CV) = sample standard deviation of the process values ÷ their mean. With "
                "a single sample the variability cannot be estimated and a dash is shown."), "",
             tr("| 演算法 | 語言 | 最小值 ms | 最大值 ms | 標準差 ms | 變異係數 | 有效樣本 |",
                "| Benchmark | Language | Min ms | Max ms | Std dev ms | CV | Valid samples |"),
             "| --- | --- | ---: | ---: | ---: | ---: | ---: |"]
    for record in view["cases"].values():
        summary = record["summary"]
        valid = sum(s["status"] == "ok" for s in record["samples"])
        values = ["—"] * 4
        if summary["status"] == "ok":
            values = [f"{summary['min_ms']:.3f}", f"{summary['max_ms']:.3f}",
                      f"{summary['stdev_ms']:.3f}" if repetitions > 1 else "—",
                      f"{summary['cv_percent']:.1f}%" if repetitions > 1 else "—"]
        lines.append(f"| {workload(record['benchmark'], lang)[0]} | {languages[record['language']]} | " +
                     " | ".join(values) + f" | {valid}/{repetitions} |")
    return lines + [""]


def switcher(lang, english, chinese):
    """The language switcher at the top of each README, linking the two generated files."""
    if lang == "tw":
        return f'<p><strong>繁體中文</strong> | <a href="{english}">English</a></p>'
    return f'<p><a href="{chinese}">繁體中文</a> | <strong>English</strong></p>'


def chinese_readme_path(readme):
    """`README.md` → `README.tw.md`, beside the English README."""
    return readme.with_name(f"{readme.stem}.tw{readme.suffix}")


def write_readmes(report, readme):
    """Write the English README to `readme` and the 繁體中文 one beside it, so both always come from one report."""
    readme = Path(readme)
    readme.parent.mkdir(parents=True, exist_ok=True)
    chinese = chinese_readme_path(readme)
    readme.write_text(generate_readme(report, "en", readme.name, chinese.name), encoding="utf-8")
    chinese.write_text(generate_readme(report, "tw", readme.name, chinese.name), encoding="utf-8")
    return readme, chinese


def generate_readme(report, lang="en", english="README.md", chinese="README.tw.md"):
    tr = translator(lang)
    sep, clause = LIST_SEPARATOR[lang], CLAUSE_SEPARATOR[lang]
    config, env = report["config"], report["environment"]
    languages = report_languages(report, lang)
    has_csharp = "csharp" in languages
    count = len(languages)
    language_count = tr(f"{count} 種語言", f"all {count} languages")
    views = mode_views(report)
    internal_timing = config.get("timing") == "in-process"
    # Reports before the fairness fix ran C# with tiered compilation (unoptimized code first).
    csharp_optimized = config.get("csharp_tiered_compilation") is False
    cold = any(params["in_process_warmups"] == 0 for _, params, _ in views)
    warm = any(params["in_process_warmups"] > 0 for _, params, _ in views)
    timing_description = (
        tr("計時採用各語言程序內的單調計時器，涵蓋資料初始化與演算法／校驗值計算，排除程序啟動、原始碼／Wasm 載入與初始編譯、輸出。",
           "Timing uses each language's in-process monotonic timer and covers data initialization and the "
           "algorithm and checksum, excluding process start, source or Wasm loading and initial compilation, and "
           "output.")
        if internal_timing else
        tr("此歷史報告採用程序外計時，包含程序啟動、載入與輸出；不能與程序內計時結果直接比較。",
           "This historical report timed whole processes from outside, including start-up, loading and output; it "
           "cannot be compared directly with in-process timings."))
    lines = [tr("# " + sep.join(languages.values()) + " 桌面執行效能評比",
                "# Desktop performance benchmark: " + sep.join(languages.values())), "",
             switcher(lang, english, chinese), ""]
    if config["profile"] == "standard":
        lines += [tr("> **注意：標準規模多數項目只需約 1 毫秒，結果主要反映短程式的啟動後延遲（JIT 暖機、記憶體初始配置），"
                     "不代表持續執行的速度。比較語言速度請參考 `--profile large`。**",
                     "> **Note: at the standard size most tests take about 1 millisecond, so the results mainly "
                     "reflect a short program's latency after start-up (JIT warm-up, initial memory allocation), not "
                     "sustained speed. To compare language speed, use `--profile large`.**"), ""]
    lines += [tr(f"本次測量 {len(views)} 種模式，各自計算綜合分數（越高越快，最快語言為 100 分）：",
                 f"This run measured {len(views)} {'mode' if len(views) == 1 else 'modes'}, each with its own "
                 "composite score (higher is faster; the fastest language scores 100):"), ""]
    for mode, params, view in views:
        scores = composite_scores(view)
        summary = score_summary(scores, languages, lang) if scores else tr("資料不足，無法計算", "not enough data to compute")
        lines.append(tr(f"- **{mode_title(mode, params, lang)}**：{summary}",
                        f"- **{mode_title(mode, params, lang)}**: {summary}"))
    lines += ["", tr(f"本專案提供十種經典演算法、{len(WORKLOADS) * count} 份可獨立執行的測試程式，"
                     "以及負責驗證結果、產生 README 與 JSON／CSV 報告的 Python 主控程式。",
                     f"The project provides ten classic algorithms, {len(WORKLOADS) * count} standalone benchmark "
                     "programs, and a Python harness that validates the results and generates the READMEs and the "
                     "JSON and CSV reports."), ""]
    for mode, params, view in views:
        short = MODE_NAMES[lang].get(mode, mode)
        lines += [f"## {mode_title(mode, params, lang)}", "", mode_method(mode, params, config, has_csharp, lang), ""]
        lines += score_lines(view, languages, lang)
        lines += median_lines(view, languages, short, lang)
        lines += typed_vs_node_lines(view, languages, short, lang)
        lines += variability_lines(view, languages, short, config["repetitions"], lang)
    lines += [tr("## 綜合分數計算方式", "## How the composite score is computed"), "",
              tr(f"每個模式分別將本次 {len(report['benchmarks'])} 項演算法的相對速度等權重取幾何平均，再以最快語言為 100 分。"
                 f"{timing_description}",
                 f"For each mode, the relative speeds on this run's {len(report['benchmarks'])} algorithms are "
                 f"combined with equal weights as a geometric mean, and the fastest language is set to 100. "
                 f"{timing_description}"), "",
              tr("相對速度 G = 幾何平均（各項 Python 耗時中位數 ÷ 該語言耗時中位數）；"
                 f"綜合分數 = 100 × G ÷ {language_count}中最大的 G，因此最高分固定為 100。"
                 f"每項演算法權重相同；只有{language_count}在該模式所有選定測試都通過時，才計算該模式的綜合分數。"
                 "不同模式、測試組合與輸入規模的分數不可直接比較。",
                 "Relative speed G = geometric mean (Python median time ÷ the language's median time, per "
                 f"benchmark); composite score = 100 × G ÷ the largest G among {language_count}, so the top score "
                 "is always 100. Every algorithm has the same weight; a mode gets composite scores only when "
                 f"{language_count} pass every selected test in that mode. Scores from different modes, test sets "
                 "or input sizes cannot be compared directly."), "",
              tr("排名表中速度倍率 = 該列語言綜合分數 ÷ 欄位基準語言綜合分數，使用未四捨五入的分數計算；"
                 "大於 1 表示比該基準語言快，小於 1 表示較慢。",
                 "In the ranking tables, speed = the row language's composite score ÷ the column's baseline "
                 "language's composite score, computed from unrounded scores; above 1 is faster than that baseline, "
                 "below 1 slower."), "",
              tr("## 執行方式", "## Running"), "",
              tr("需求：Python 3.10 以上、Node.js、" + (".NET 8 SDK（含 net8.0 目標套件與執行階段）、" if has_csharp else "") +
                 "以及支援 `目前時間()`／`currentTime()` 的星泉 Wasm 編譯器（`aqua` 與隨附相依檔案）。"
                 "不需要安裝 Python 套件或執行 npm install。星泉腳本使用星泉繁體中文版的繁體中文關鍵字與雙語內建函式，"
                 "舊版僅支援英文的直譯器無法執行。",
                 "Requirements: Python 3.10 or later, Node.js, " +
                 (".NET 8 SDK (with the net8.0 targeting pack and runtime), " if has_csharp else "") +
                 "and an AquariusLang Wasm compiler that supports `目前時間()` / `currentTime()` (`aqua` with its "
                 "bundled files). No Python packages or npm install are needed. The AquariusLang scripts use the "
                 "Traditional Chinese keywords and bilingual built-ins of AquariusLang's Traditional Chinese edition, "
                 "so the older English-only interpreter cannot run them."), "",
              "```powershell", "python run_benchmarks.py",
              tr("# 使用較小輸入，快速檢查正確性：", "# Small inputs, a quick correctness check:"),
              "python run_benchmarks.py --profile smoke --repetitions 1 --warmups 0",
              tr("# 使用較大輸入，降低 JIT 暖機的影響：", "# Larger inputs, reducing the effect of JIT warm-up:"),
              "python run_benchmarks.py --profile large --timeout 300",
              tr("# 只測暖機模式，並自訂程序內暖機與計時次數：",
                 "# Warmed mode only, with custom in-process warm-up and timed run counts:"),
              "python run_benchmarks.py --modes warmed --in-process-warmups 10 --in-process-runs 7",
              tr("# 必要時指定執行檔路徑：", "# Executable paths, when needed:"),
              'python run_benchmarks.py --aquarius "C:\\Aquarius\\aqua.exe" --node "C:\\Program Files\\nodejs\\node.exe"' +
              (' --dotnet "C:\\Program Files\\dotnet\\dotnet.exe"' if has_csharp else ''),
              tr("# 僅執行指定演算法：", "# Selected algorithms only:"),
              "python run_benchmarks.py --benchmarks fibonacci sieve matrix",
              tr("# 使用既有資料重新產生 README，不重新測量：", "# Regenerate the READMEs from saved data, without measuring:"),
              "python run_benchmarks.py --report-only results/latest.json",
              tr("# 執行主控程式與參考答案測試：", "# Run the harness and reference-answer tests:"),
              "python -m unittest discover -s tests -v", "```", "",
              tr("若 `python` 是尚未設定版本的 pyenv 代理程式，請直接呼叫已安裝的 `python.exe`。"
                 "主控程式預設使用自身的 Python 直譯器執行測試，也可用 `--python PATH` 指定其他版本。"
                 "它會搜尋目前程序的 PATH；在 Windows 上也會搜尋使用者與系統的最新 PATH，"
                 "因此舊終端工作階段也能找到新加入的星泉路徑。執行環境參數只接受單一執行檔路徑。" +
                 ("C# 會優先選用具有 SDK 的 dotnet，也會搜尋 DOTNET_ROOT 與使用者的 `.dotnet` 目錄；可用 `--dotnet PATH` 指定。"
                  if has_csharp else ""),
                 "If `python` is a pyenv shim with no version set, call the installed `python.exe` directly. The "
                 "harness runs the Python tests with its own interpreter by default; `--python PATH` selects "
                 "another. It searches the current process's PATH, and on Windows also the latest user and system "
                 "PATH, so an older terminal session still finds a newly added AquariusLang path. Runtime options "
                 "take a single executable path." +
                 (" C# prefers a dotnet that has the SDK and also searches DOTNET_ROOT and the user's `.dotnet` "
                  "folder; `--dotnet PATH` selects one." if has_csharp else "")), "",
              *(([tr("單獨執行 C# 測試（例如篩法）：", "To run one C# test on its own (the sieve, for example):"), "",
                  "```powershell",
                  "dotnet run --project benchmarks/csharp/Benchmark.csproj --configuration Release -p:BenchmarkSource=sieve.cs",
                  "```", ""] if has_csharp else [])),
              tr("主控程式會在暫存目錄為每個模式建立原始碼副本，只替換 `benchmark_n`（輸入規模）、"
                 "`benchmark_warmups`（程序內暖機次數）與 `benchmark_timed_runs`（程序內計時次數）三個宣告。"
                 "直接執行原始腳本時，採用標準規模與標準模式（不暖機、計時一次）。每次測量會建立帶有日期的 `results/` 子目錄，"
                 f"並重新產生 `results/latest.json`、`{english}`（英文）與 `{chinese}`（繁體中文）。"
                 "`--modes` 選擇模式（預設 `standard warmed` 兩者），`--in-process-warmups`（預設 5）與 `--in-process-runs`（預設 5）"
                 "設定暖機模式的程序內次數；`--repetitions` 是每組計入統計的程序數，`--warmups` 是每組捨棄的暖身程序數。"
                 "也可使用 `--output-dir`、`--readme`（英文 README 的路徑，繁體中文版寫在旁邊的 `.tw.md`）、`--timeout`、`--seed` 自訂測試。"
                 "結束碼 1 表示至少一個執行環境無法使用或測試驗證失敗；報告仍會保留失敗資訊。",
                 "For each mode the harness copies the sources into a temporary folder and replaces only three "
                 "declarations: `benchmark_n` (input size), `benchmark_warmups` (in-process warm-up runs) and "
                 "`benchmark_timed_runs` (in-process timed runs). Running a script directly uses the standard size "
                 "and standard mode (no warm-up, one timed run). Each measurement creates a dated subfolder of "
                 f"`results/` and regenerates `results/latest.json`, `{english}` (English) and `{chinese}` "
                 "(Traditional Chinese). `--modes` selects the modes (both `standard warmed` by default); "
                 "`--in-process-warmups` (default 5) and `--in-process-runs` (default 5) set the in-process counts "
                 "of warmed mode; `--repetitions` is the number of processes per case that count toward the "
                 "statistics, and `--warmups` the number of discarded warm-up processes per case. `--output-dir`, "
                 "`--readme` (the English README's path; the Traditional Chinese one is written beside it as "
                 "`.tw.md`), `--timeout` and `--seed` customize a run further. Exit code 1 means at least one runtime "
                 "was unavailable or a test failed validation; the report still keeps the failure details."), "",
              tr("## 測量方法", "## Methodology"), "",
              (tr("- 每筆樣本都啟動新的程序，但排名只採用腳本自行回報的 `ELAPSED_MS`。"
                  "星泉使用 `目前時間()`（毫秒）、Python 使用 `time.perf_counter_ns()`（奈秒差值 ÷ 1e6）、"
                  "Node.js 使用 `process.hrtime.bigint()`（奈秒差值 ÷ 1e6）。" +
                  ("C# 使用 `Stopwatch.GetTimestamp()`（刻度差值 × 1000 ÷ Frequency）。" if has_csharp else "") +
                  "所有計時器皆為單調計時器。",
                  "- Every sample starts a new process, but the ranking uses only the `ELAPSED_MS` each script "
                  "reports itself. AquariusLang uses `目前時間()` (`currentTime()`, milliseconds), Python "
                  "`time.perf_counter_ns()` (nanosecond difference ÷ 1e6), Node.js `process.hrtime.bigint()` "
                  "(nanosecond difference ÷ 1e6)" +
                  (", C# `Stopwatch.GetTimestamp()` (tick difference × 1000 ÷ Frequency)" if has_csharp else "") +
                  ". All timers are monotonic.")
               if internal_timing else
               tr("- 此歷史報告的樣本以主控程式 `time.perf_counter_ns()` 測量完整程序經過時間，包含啟動、載入、編譯與輸出。",
                  "- The samples of this historical report are whole-process times measured by the harness with "
                  "`time.perf_counter_ns()`, including start-up, loading, compilation and output.")),
              (tr(f"- {language_count}皆在函式定義完成後、資料初始化前開始計時，並在演算法與校驗值計算完成後、輸出前停止。"
                  "執行中的記憶體配置、垃圾回收及按需 JIT 仍計入。JSON／CSV 的 `elapsed_ms` 為程序值"
                  "（程序內各次計時的中位數，`run_elapsed_ms` 保留每次計時）；"
                  "`process_elapsed_ms` 另保留完整程序耗時供診斷，不參與統計與排名。",
                  f"- {language_count[0].upper() + language_count[1:]} start timing after the function definitions "
                  "and before data initialization, and stop after the algorithm and checksum, before output. Memory "
                  "allocation, garbage collection and on-demand JIT during the run still count. `elapsed_ms` in the "
                  "JSON and CSV is the process value (the median of the in-process timed runs; `run_elapsed_ms` "
                  "keeps each run); `process_elapsed_ms` also keeps the whole-process time for diagnosis and takes "
                  "no part in the statistics or ranking.")
               if internal_timing else
               tr("- 歷史資料保留原始測量值，重新產生報告不會將程序外耗時轉換成程序內耗時。",
                  "- Historical data keeps its original measurements; regenerating the report does not convert "
                  "whole-process times into in-process times.")),
              *(f"- {MODE_NAMES[lang].get(mode, mode)[0].upper() + MODE_NAMES[lang].get(mode, mode)[1:]}"
                f"{tr('：', ': ')}{mode_method(mode, params, config, has_csharp, lang)}" for mode, params, _ in views),
              tr("- 每支腳本把計時工作包成 `benchmark_run` 函式；程序內暖機只多呼叫這個函式，不改變演算法或計時區間。",
                 "- Each script wraps the timed work in a `benchmark_run` function; in-process warm-up only calls "
                 "that function more often and changes neither the algorithm nor the timed interval."),
              tr("- 星泉一律使用 `aqua build` 在測量前建立 Wasm，再執行 `aqua run`；Wasm 生成不計入樣本耗時，每個模式的副本各自建立。"
                 "「星泉（型別）」使用同一個編譯器與相同演算法，只在變數、參數與回傳值加上選用型別標註（`benchmarks/aquarius_typed/`）；"
                 "型別函式必須宣告回傳型別，因此快速排序與譜範數的原地修改函式多了一行 `回傳 0;`，"
                 "二元樹以 `陣列`（元素可為任何值的陣列）標註樹狀陣列。"
                 "Python 執行原始碼，Node.js 使用 V8。" +
                 ("C# 以 `dotnet build --configuration Release` 預先編譯為 net8.0 組件，再直接以 `dotnet Benchmark.dll` 執行；"
                  "建置與還原不計時，不使用外部 NuGet 套件。進入 Main 前的初始 JIT 不計時，計時區間內的按需 JIT 仍計入。" +
                  ("組件關閉分層編譯（`TieredCompilation=false`），每個方法第一次呼叫就以最佳化 JIT 編譯，"
                   "對應星泉在計時前完成的 Wasmtime 最佳化編譯。" if csharp_optimized else "") if has_csharp else "") +
                 "沒有 NumPy、原生演算法函式庫、工作執行緒或內建排序。",
                 "- AquariusLang always builds the Wasm with `aqua build` before measuring, then runs `aqua run`; "
                 "Wasm generation is not part of the sample time, and each mode's copy is built separately. "
                 "\"AquariusLang (typed)\" uses the same compiler and the same algorithms, adding only optional type "
                 "annotations on variables, parameters and return values (`benchmarks/aquarius_typed/`); typed "
                 "functions must declare a return type, so the in-place functions of quicksort and spectral norm "
                 "gain a `回傳 0;` (`return 0;`) line, and binary trees annotate the tree arrays as `陣列` (`Array`, "
                 "an array whose elements can be any value). Python runs the source, and Node.js uses V8. " +
                 ("C# is compiled ahead of time into a net8.0 assembly with `dotnet build --configuration Release` "
                  "and run directly as `dotnet Benchmark.dll`; build and restore are not timed, and no external "
                  "NuGet packages are used. The initial JIT before Main is not timed; on-demand JIT inside the timed "
                  "interval still counts. " +
                  ("The assembly turns tiered compilation off (`TieredCompilation=false`), so each method is "
                   "compiled by the optimizing JIT on its first call, matching the optimized Wasmtime compilation "
                   "AquariusLang finishes before timing. " if csharp_optimized else "") if has_csharp else "") +
                 "No NumPy, native algorithm libraries, worker threads or built-in sorts are used."),
              tr("- 暖身程序的樣本會捨棄，作用是預熱作業系統檔案快取；不同程序之間不保留 JIT 或 VM 狀態。"
                 "每輪以記錄的隨機種子打亂所有演算法／語言／模式組合，再依序執行。",
                 "- Warm-up process samples are discarded; they warm the operating system's file cache, and no JIT "
                 "or VM state carries over between processes. Each round shuffles every algorithm, language and mode "
                 "combination with the recorded random seed, then runs them in that order."),
              tr("- 每筆暖身與正式樣本的每次計時結果都必須符合未納入計時的 Python 參考答案。整數必須完全相同；"
                 "譜範數平方的相對容許誤差為 1e-9，絕對容許誤差為 1e-12。"
                 "非零結束碼、逾時、缺少或多餘的標準輸出、非有限數值、校驗值不符，都會使該測試失敗。" +
                 ("計時輸出必須為有限且大於零的毫秒值；缺少計時值時不會退回程序外計時。" if internal_timing else ""),
                 "- Every timed run of every warm-up and counted sample must match the untimed Python reference "
                 "answer. Integers must be identical; the squared spectral norm allows a relative error of 1e-9 and "
                 "an absolute error of 1e-12. A non-zero exit code, a timeout, missing or extra standard output, a "
                 "non-finite value or a checksum mismatch fails the test." +
                 (" The timing output must be a finite millisecond value above zero; a missing timing does not fall "
                  "back to whole-process timing." if internal_timing else "")),
              tr("- 星泉的整數 `/` 會截斷小數，Python `//` 與 Node.js `Math.trunc` 使用相對應的運算。"
                 "浮點測試採用雙精度（星泉使用 `d` 字面值）；標準輸入的整數中間值均在帶正負號的 32 位元範圍內。",
                 "- AquariusLang's integer `/` truncates; Python uses `//` and Node.js `Math.trunc` to match. "
                 "Floating-point tests use double precision (AquariusLang uses `d` literals); at the standard size "
                 "every intermediate integer stays within the signed 32-bit range."),
              (tr("- 陣列建構在各語言採用相同的線性成本：星泉使用 `陣列.建立` 預先配置（快速排序以預留容量的 `陣列.追加`），"
                  "Python 使用 `[值] * n`／`append`，Node.js 使用 `push`" +
                  ("，C# 使用 `new T[n]`（必要時 `Array.Fill`）" if has_csharp else "") +
                  "；不使用每次複製整個陣列的追加方式。",
                  "- Array construction has the same linear cost in every language: AquariusLang preallocates with "
                  "`陣列.建立` (`Array.Make`; quicksort uses `陣列.追加`, `Array.Append`, with reserved capacity), "
                  "Python uses `[value] * n` / `append`, Node.js `push`" +
                  (", C# `new T[n]` (with `Array.Fill` where needed)" if has_csharp else "") +
                  "; no append that copies the whole array each time is used.")
               if report.get("schema_version", 0) >= 3 else
               tr("- 此歷史報告中，Python、Node.js" + (" 與 C#" if has_csharp else "") +
                  " 的陣列建構使用每次複製整個陣列的追加方式（平方級成本），星泉則可能已改用預先配置；"
                  "篩法、快速排序、矩陣、譜範數與 N 皇后的比較因此偏向星泉。",
                  "- In this historical report, " + ("Python, Node.js and C#" if has_csharp else "Python and Node.js") +
                  " build arrays with appends that copy the whole array each time (quadratic cost), while "
                  "AquariusLang may already preallocate; the sieve, quicksort, matrix, spectral norm and N-Queens "
                  "comparisons therefore favor AquariusLang.")),
              (tr("- 編譯時機：星泉的 Wasm 在計時開始前已由 Wasmtime 完整編譯為機器碼。" +
                  (("C# 關閉分層編譯，方法在第一次呼叫時即以最佳化 JIT 編譯" +
                    ("；標準模式中這次 JIT 仍在計時區間內。" if cold else "。")) if has_csharp else "") +
                  "Node.js（V8）無法預先最佳化，先以直譯器與基準編譯器執行" +
                  ("；標準模式中熱點函式的最佳化發生在計時區間內，因此偏向星泉" if cold else "") +
                  ("；暖機模式靠程序內暖機讓熱點函式在計時前完成最佳化，但仍可能有少量 JIT 或垃圾回收落在計時區間內" if warm else "") +
                  "。",
                  "- Compilation timing: Wasmtime has fully compiled the AquariusLang Wasm to machine code before "
                  "timing starts. " +
                  (("C# has tiered compilation off, so methods are compiled by the optimizing JIT on their first "
                    "call" + ("; in standard mode that JIT is still inside the timed interval. " if cold else ". "))
                   if has_csharp else "") +
                  "Node.js (V8) cannot optimize ahead of time and starts in its interpreter and baseline compiler" +
                  ("; in standard mode hot functions are optimized inside the timed interval, which favors "
                   "AquariusLang" if cold else "") +
                  ("; warmed mode relies on in-process warm-up to optimize hot functions before timing, though a "
                   "little JIT or garbage collection may still fall inside the timed interval" if warm else "") +
                  ". ")
               if csharp_optimized or not has_csharp else
               tr("- 編譯時機不對稱：星泉的 Wasm 在計時開始前已由 Wasmtime 完整編譯為機器碼；"
                  "C#（分層編譯）與 Node.js（V8）的 JIT 編譯與最佳化發生在計時區間內，C# 在約 100 毫秒內幾乎只執行未最佳化程式碼。",
                  "- Asymmetric compilation timing: Wasmtime has fully compiled the AquariusLang Wasm to machine code "
                  "before timing starts; the JIT compilation and optimization of C# (tiered compilation) and Node.js "
                  "(V8) happen inside the timed interval, and for about the first 100 milliseconds C# runs almost "
                  "only unoptimized code. ")) +
              tr("標準規模每項只需約 1 毫秒，計時器與記憶體配置雜訊比例較高；"
                 "`--profile large` 以較大輸入降低此影響，兩種規模的分數不可混用。",
                 "At the standard size each test takes about 1 millisecond, so timer and allocation noise weigh "
                 "more; `--profile large` reduces this with larger inputs, and the scores of the two sizes must not "
                 "be mixed."),
              tr("- 小型工作負載可能受計時器與函式呼叫成本影響；暖機模式只暖機數次，不等於長時間執行的穩態速度，"
                 "標準模式則只反映第一次執行；兩者都不代表所有程式的語言排名。"
                 "CPU 頻率、溫度、背景工作與排程雜訊未受控制。未測量程序記憶體用量與 CPU 時間；下方 RAM 為機器配備。",
                 "- Small workloads can be affected by timer and function call costs; warmed mode warms up only a "
                 "few times and is not the steady-state speed of a long run, while standard mode reflects only the "
                 "first run; neither represents a language ranking for every program. CPU frequency, temperature, "
                 "background work and scheduling noise are not controlled. Process memory use and CPU time are not "
                 "measured; the RAM below is the machine's installed memory."), "",
              tr("## 測試日期與環境", "## Test date and environment"), "",
              tr(f"- 開始時間：{md(report['started_at'])}", f"- Started: {md(report['started_at'])}"),
              tr(f"- 結束時間：{md(report['finished_at'])}", f"- Finished: {md(report['finished_at'])}"),
              tr(f"- 時區：{md(config['timezone'])}", f"- Time zone: {md(config['timezone'])}"),
              tr(f"- 輸入規模：{PROFILES[lang].get(config['profile'], config['profile'])}（`{config['profile']}`）；"
                 f"每組 {config['repetitions']} 個計入統計的程序、{config['warmups']} 個捨棄的暖身程序",
                 f"- Input size: {PROFILES[lang].get(config['profile'], config['profile'])} (`{config['profile']}`); "
                 f"{config['repetitions']} counted and {config['warmups']} discarded warm-up processes per case"),
              tr("- 模式：", "- Modes: ") + clause.join(mode_title(mode, params, lang) for mode, params, _ in views),
              tr(f"- 排序隨機種子：{config['seed']}；每個程序逾時上限：{config['timeout_seconds']:g} 秒",
                 f"- Order random seed: {config['seed']}; timeout per process: {config['timeout_seconds']:g} s"),
              tr(f"- 作業系統：{md(env['os'])}", f"- Operating system: {md(env['os'])}"),
              tr(f"- 架構：{md(env['architecture'])}", f"- Architecture: {md(env['architecture'])}"),
              tr(f"- CPU：{md(env['cpu'])}；邏輯處理器：{env['logical_cpus']}",
                 f"- CPU: {md(env['cpu'])}; logical processors: {env['logical_cpus']}"),
              (tr(f"- 實體 RAM：{env['ram_bytes'] / 1024**3:.2f} GiB", f"- Physical RAM: {env['ram_bytes'] / 1024**3:.2f} GiB")
               if env['ram_bytes'] else tr("- 實體 RAM：無法取得", "- Physical RAM: unavailable")),
              tr(f"- 使用中的電源計畫：{md(env['power_plan'] or '無法取得')}",
                 f"- Active power plan: {md(env['power_plan'] or 'unavailable')}"),
              tr(f"- Python 主控程式版本：{md(env['python_runner'])}", f"- Python harness version: {md(env['python_runner'])}"),
              tr(f"- 行程 CPU 親和性遮罩：`{env.get('process_affinity_mask', '未固定／未取得')}`",
                 f"- Process CPU affinity mask: `{env.get('process_affinity_mask', 'not pinned / unavailable')}`"),
              tr(f"- 主控程式診斷計時器解析度：{env['timer_resolution_seconds']:.3g} 秒（非所有語言的計時器解析度）",
                 f"- Harness diagnostic timer resolution: {env['timer_resolution_seconds']:.3g} s (not the resolution "
                 "of every language's timer)"), "",
              tr("| 執行環境 | 版本／組建 | 執行檔 |", "| Runtime | Version / build | Executable |"), "| --- | --- | --- |"]
    for language, title in languages.items():
        runtime = report["runtimes"][language]
        version = runtime.get("version", tr("無法使用：找不到執行檔", "unavailable: executable not found"))
        if not runtime.get("available"):
            version = tr("無法使用：", "unavailable: ") + runtime.get("error", tr("找不到執行檔", "executable not found"))
        if language in ("aquarius", "aquarius_typed") and runtime.get("available"):
            version = tr("未提供版本參數；以發行目錄與二進位檔雜湊識別",
                         "no version option; identified by release folder and binary hashes")
        lines.append(f"| {title} | {md(version)} | {md(runtime.get('executable', tr('無法取得', 'unavailable')))} |")
    aqua = report["runtimes"]["aquarius"]
    if aqua.get("available"):
        lines += ["", tr(f"星泉發行目錄：`{aqua['release_directory']}`。",
                         f"AquariusLang release folder: `{aqua['release_directory']}`."), "",
                  tr(f"星泉啟動執行檔 SHA-256：`{aqua['executable_sha256']}`。",
                     f"AquariusLang launcher SHA-256: `{aqua['executable_sha256']}`."), ""]
        for filename, fingerprint in aqua.get("assemblies_sha256", {}).items():
            lines.append(f"- `{filename}` SHA-256{tr('：', ': ')}`{fingerprint}`")
    failures = []
    for key, record in report["cases"].items():
        if record.get("unavailable"):
            failures.append(f"- `{key}`{tr('：', ': ')}{md(record['unavailable'])}")
        if record.get("build", {}).get("error"):
            failures.append(f"- `{key}`{tr('：', ': ')}{md(record['build']['error'])}")
        for phase in ("warmups", "samples"):
            for index, sample in enumerate(record[phase]):
                if sample["status"] != "ok":
                    kind = tr("暖身", "warm-up") if phase == "warmups" else tr("正式樣本", "sample")
                    failures.append(f"- `{key}` {kind} #{index + 1}{tr('：', ': ')}{md(sample['error'])}")
    lines += ["", tr("## 正確性驗證", "## Correctness"), ""]
    lines += failures or [tr("所有語言、所有模式的每筆暖身與正式樣本輸出，均符合 Python 參考答案。",
                             "Every warm-up and counted sample output, in every language and mode, matches the Python "
                             "reference answer.")]
    lines += ["", tr("| 演算法 | 預期結果 | 工作負載 |", "| Benchmark | Expected result | Workload |"), "| --- | ---: | --- |"]
    for name, spec in report["benchmarks"].items():
        title, description = workload(name, lang)
        lines.append(f"| {title} | {spec['expected']} | {description} |")
    lines += ["", tr("## 可重現測試資料", "## Reproducible data"), "",
              tr(f"- 原始樣本、輸出、指令、執行順序、環境資訊與執行檔／原始碼雜湊：`{report['artifacts']['json']}`",
                 "- Raw samples, outputs, commands, execution order, environment and executable and source hashes: "
                 f"`{report['artifacts']['json']}`"),
              tr(f"- 統計摘要與逐筆樣本 CSV：`{report['artifacts']['summary_csv']}`、`{report['artifacts']['samples_csv']}`",
                 f"- Summary and per-sample CSV: `{report['artifacts']['summary_csv']}`, "
                 f"`{report['artifacts']['samples_csv']}`"),
              tr("- `benchmarks.json`：標準／快速檢查的輸入規模與工作負載定義。",
                 "- `benchmarks.json`: the standard and smoke-check input sizes and workload definitions."),
              "- " + sep.join(f"`benchmarks/{language}/`" for language in languages) +
              tr("：可獨立執行的測試程式。", ": the standalone benchmark programs."),
              tr("- `reference.py`：未納入計時的參考答案；`tests/`：主控程式與參考答案的回歸測試。",
                 "- `reference.py`: the untimed reference answers; `tests/`: regression tests for the harness and "
                 "reference answers."), "",
              tr(f"本 README 與 `{english}`（英文）由 `run_benchmarks.py` 以同一份報告產生，下次執行時會覆寫。"
                 "JSON 保留測量當時的原始與暫存腳本、測試清單、主控程式及參考答案雜湊。指令中的暫存路徑對應當次執行的檔案，測試後會移除。"
                 "比較不同測試時，請保留原始碼與相對應的報告。",
                 f"This README and `{chinese}` (Traditional Chinese) are generated by `run_benchmarks.py` from the "
                 "same report and are overwritten on the next run. The JSON keeps the hashes of the original and "
                 "staged scripts, the test list, the harness and the reference answers at measurement time. "
                 "Temporary paths in the commands refer to that run's files and are removed after the run. Keep the "
                 "sources and the matching report when comparing different runs."), ""]
    return "\n".join(lines)
