"""繁體中文 README 與跨演算法綜合分數。只使用報告中的既有實測資料。"""
import math
from itertools import combinations

LANGUAGES = {"aquarius": "星泉", "aquarius_typed": "星泉（型別）", "python": "Python", "node": "Node.js", "csharp": "C#"}
WORKLOADS = {
    "fibonacci": ("遞迴費波那契", "使用樸素遞迴，不使用記憶化。"),
    "ackermann": ("阿克曼函數", "計算 A(3, n)，測試巢狀遞迴呼叫。"),
    "sieve": ("埃拉托斯特尼篩法", "使用布林陣列，計算 2 至 n（含）的質數數量。"),
    "quicksort": ("快速排序", "以中間元素為樞紐，原地排序固定種子的線性同餘序列；檢查排序順序與加權校驗值。"),
    "matrix": ("矩陣乘法", "使用列優先的一維陣列與 i/j/k 三層迴圈，計算結果矩陣所有元素的總和。"),
    "mandelbrot": ("曼德布洛特集合", "在 [-2, 1) × [-1, 1) 上取 n × n 個點，最多迭代 60 次，累計逃逸迭代次數。"),
    "nqueens": ("N 皇后問題", "以回溯法逐一檢查欄與對角線，計算所有解的數量。"),
    "binary_trees": ("二元樹", "建立八棵深度為 n 的完整二元樹，並遞迴計算節點總數。"),
    "spectral_norm": ("譜範數", "對隱式矩陣執行十輪冪次迭代，輸出譜範數平方，避免使用函式庫平方根。"),
    "collatz": ("考拉茲猜想", "累計起始整數 1 至 n 到達 1 的步數，不使用記憶化。"),
}
STATUS = {"ok": "通過", "failed": "失敗", "incomplete": "未完成", "unavailable": "無法使用"}


def report_languages(report):
    """Keep old reports usable without inventing C# measurements for them."""
    present = report.get("runtimes")
    if present is None:
        present = {key.rsplit("/", 1)[-1] for key in report["cases"]}
    return {language: title for language, title in LANGUAGES.items() if language in present}


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


def generate_readme(report):
    config, env = report["config"], report["environment"]
    languages = report_languages(report)
    has_csharp = "csharp" in languages
    language_count = f"{len(languages)} 種語言"
    scores = composite_scores(report)
    internal_timing = config.get("timing") == "in-process"
    # Reports before the fairness fix ran C# with tiered compilation (unoptimized code first).
    csharp_optimized = config.get("csharp_tiered_compilation") is False
    warm_runs = config.get("in_process_warmups", 0)
    timing_description = ("計時採用各語言程序內的單調計時器，涵蓋資料初始化與演算法／校驗值計算，排除程序啟動、原始碼／Wasm 載入與初始編譯、輸出。"
                          if internal_timing else "此歷史報告採用程序外計時，包含程序啟動、載入與輸出；不能與程序內計時結果直接比較。")
    lines = ["# " + "、".join(languages.values()) + " 桌面執行效能評比", ""]
    if scores:
        ranking = sorted(scores, key=scores.get, reverse=True)
        score_text = "、".join(f"{languages[lang]} {scores[lang]:.2f} 分" for lang in ranking)
        comparisons = "；".join(
            f"{languages[faster]} 的綜合速度是 {languages[slower]} 的 {scores[faster] / scores[slower]:.2f} 倍"
            for faster, slower in combinations(ranking, 2))
        speed_columns = " | ".join(f"相對 {languages[language]} 的速度" for language in ranking)
        if config["profile"] == "standard":
            lines += ["> **注意：標準規模多數項目只需約 1 毫秒，結果主要反映短程式的啟動後延遲（JIT 暖機、記憶體初始配置），"
                      "不代表持續執行的速度。比較語言速度請參考 `--profile large`。**", ""]
        if warm_runs:
            lines += [f"每個程序先在同一程序內不計時執行同一工作 {warm_runs} 次，讓 JIT 完成最佳化，再計時第 {warm_runs + 1} 次；"
                      "各語言規則相同。", ""]
        lines += [f"**本次綜合效能：{score_text}（越高越快）。**", "",
                  f"綜合速度兩兩比較：{comparisons}。", "",
                  f"將本次 {len(report['benchmarks'])} 項演算法的相對速度等權重取幾何平均，再以最快語言為 100 分。"
                  f"{timing_description}", "",
                  "表中速度倍率 = 該列語言綜合分數 ÷ 欄位基準語言綜合分數，使用未四捨五入的分數計算；"
                  "大於 1 表示比該基準語言快，小於 1 表示較慢。", "",
                  f"| 排名 | 程式語言 | 綜合分數 | {speed_columns} |",
                  "| ---: | --- | ---: | " + " | ".join("---:" for _ in ranking) + " |"]
        for place, language in enumerate(ranking, 1):
            speeds = " | ".join(f"{scores[language] / scores[baseline]:.3f} 倍" for baseline in ranking)
            lines.append(f"| {place} | {languages[language]} | {scores[language]:.2f} | {speeds} |")
    else:
        lines += [f"**本次資料不足以計算{language_count}的綜合分數。** 至少一項測試失敗、未完成或執行環境無法使用；"
                  "各項測試狀態列於下方。", ""]
    lines += ["", "相對速度 G = 幾何平均（各項 Python 耗時中位數 ÷ 該語言耗時中位數）；"
              f"綜合分數 = 100 × G ÷ {language_count}中最大的 G，因此最高分固定為 100。"
              f"每項演算法權重相同；只有{language_count}在所有選定測試都通過時，才計算綜合分數。"
              "不同測試組合與輸入規模的分數不可直接比較。", "",
              f"本專案提供十種經典演算法、{len(WORKLOADS) * len(languages)} 份可獨立執行的測試程式，以及負責驗證結果、產生 README 與 JSON／CSV 報告的 Python 主控程式。", "",
              "## 執行方式", "",
              "需求：Python 3.10 以上、Node.js、" + (".NET 8 SDK（含 net8.0 目標套件與執行階段）、" if has_csharp else "") +
              "以及支援 `目前時間()`／`currentTime()` 的星泉 Wasm 編譯器（`aqua` 與隨附相依檔案）。"
              "不需要安裝 Python 套件或執行 npm install。星泉腳本使用星泉繁體中文版的繁體中文關鍵字與雙語內建函式，"
              "舊版僅支援英文的直譯器無法執行。", "",
              "```powershell", "python run_benchmarks.py", "# 使用較小輸入，快速檢查正確性：",
              "python run_benchmarks.py --profile smoke --repetitions 1 --warmups 0",
              "# 使用較大輸入，降低 JIT 暖機的影響：", "python run_benchmarks.py --profile large --timeout 300",
              "# 必要時指定執行檔路徑：",
              'python run_benchmarks.py --aquarius "C:\\Aquarius\\aqua.exe" --node "C:\\Program Files\\nodejs\\node.exe"' +
              (' --dotnet "C:\\Program Files\\dotnet\\dotnet.exe"' if has_csharp else ''),
              "# 僅執行指定演算法：", "python run_benchmarks.py --benchmarks fibonacci sieve matrix",
              "# 使用既有資料重新產生 README，不重新測量：",
              "python run_benchmarks.py --report-only results/latest.json",
              "# 執行主控程式與參考答案測試：", "python -m unittest discover -s tests -v", "```", "",
              "若 `python` 是尚未設定版本的 pyenv 代理程式，請直接呼叫已安裝的 `python.exe`。"
              "主控程式預設使用自身的 Python 直譯器執行測試，也可用 `--python PATH` 指定其他版本。"
              "它會搜尋目前程序的 PATH；在 Windows 上也會搜尋使用者與系統的最新 PATH，"
              "因此舊終端工作階段也能找到新加入的星泉路徑。執行環境參數只接受單一執行檔路徑。" +
              ("C# 會優先選用具有 SDK 的 dotnet，也會搜尋 DOTNET_ROOT 與使用者的 `.dotnet` 目錄；可用 `--dotnet PATH` 指定。" if has_csharp else ""), "",
              *((["單獨執行 C# 測試（例如篩法）：", "", "```powershell",
                   "dotnet run --project benchmarks/csharp/Benchmark.csproj --configuration Release -p:BenchmarkSource=sieve.cs",
                   "```", ""] if has_csharp else [])),
              "主控程式會在暫存目錄建立原始碼副本，只將 `benchmark_n` 的宣告替換為所選輸入規模。"
              "直接執行原始腳本時，採用標準規模。每次測量會建立帶有日期的 `results/` 子目錄，"
              "並重新產生 `results/latest.json` 與 `README.md`。"
              "可使用 `--output-dir`、`--readme`、`--timeout`、`--seed`、`--repetitions`、`--warmups` 自訂測試。"
              "結束碼 1 表示至少一個執行環境無法使用或測試驗證失敗；報告仍會保留失敗資訊。", "",
              "## 測量方法", "",
              ("- 每筆樣本都啟動新的程序，但排名只採用腳本自行回報的 `ELAPSED_MS`。"
               "星泉使用 `目前時間()`（毫秒）、Python 使用 `time.perf_counter_ns()`（奈秒差值 ÷ 1e6）、"
               "Node.js 使用 `process.hrtime.bigint()`（奈秒差值 ÷ 1e6）。" +
               ("C# 使用 `Stopwatch.GetTimestamp()`（刻度差值 × 1000 ÷ Frequency）。" if has_csharp else "") + "所有計時器皆為單調計時器。"
               if internal_timing else "- 此歷史報告的樣本以主控程式 `time.perf_counter_ns()` 測量完整程序經過時間，包含啟動、載入、編譯與輸出。"),
              (f"- {language_count}皆在函式定義完成後、資料初始化前開始計時，並在演算法與校驗值計算完成後、輸出前停止。"
               "執行中的記憶體配置、垃圾回收及按需 JIT 仍計入。JSON／CSV 的 `elapsed_ms` 為程序內耗時；"
               "`process_elapsed_ms` 另保留完整程序耗時供診斷，不參與統計與排名。"
               if internal_timing else "- 歷史資料保留原始測量值，重新產生報告不會將程序外耗時轉換成程序內耗時。"),
              "- 星泉一律使用 `aqua build` 在測量前建立 Wasm，再執行 `aqua run`；Wasm 生成不計入樣本耗時。"
              "「星泉（型別）」使用同一個編譯器與相同演算法，只在變數、參數與回傳值加上選用型別標註（`benchmarks/aquarius_typed/`）；"
              "型別函式必須宣告回傳型別，因此快速排序與譜範數的原地修改函式多了一行 `回傳 0;`，"
              "二元樹的樹狀陣列無法標註，只標註計數變數。"
              "Python 執行原始碼，Node.js 使用 V8。" +
              ("C# 以 `dotnet build --configuration Release` 預先編譯為 net8.0 組件，再直接以 `dotnet Benchmark.dll` 執行；"
               "建置與還原不計時，不使用外部 NuGet 套件。進入 Main 前的初始 JIT 不計時，計時區間內的按需 JIT 仍計入。" +
               ("組件關閉分層編譯（`TieredCompilation=false`），每個方法第一次呼叫就以最佳化 JIT 編譯，"
                "對應星泉在計時前完成的 Wasmtime 最佳化編譯。" if csharp_optimized else "") if has_csharp else "") +
              "沒有 NumPy、原生演算法函式庫、工作執行緒或內建排序。",
              (f"- 程序內暖身：每支腳本把計時工作包成函式，先不計時呼叫 {warm_runs} 次，再計時一次；" +
               ("C# 與 " if has_csharp else "") + "Node.js 的 JIT 因此能在計時前完成最佳化，星泉與 Python 也執行相同次數。\n" if warm_runs else "") +
              "- 暖身程序的樣本會捨棄，作用是預熱作業系統檔案快取；不同程序之間不保留 JIT 或 VM 狀態。"
              "每輪以記錄的隨機種子打亂所有演算法／語言組合，再依序執行。",
              "- 每筆暖身與正式樣本都必須符合未納入計時的 Python 參考答案。整數必須完全相同；"
              "譜範數平方的相對容許誤差為 1e-9，絕對容許誤差為 1e-12。"
              "非零結束碼、逾時、缺少或多餘的標準輸出、非有限數值、校驗值不符，都會使該測試失敗。"
              + ("計時輸出必須為有限且大於零的毫秒值；缺少計時值時不會退回程序外計時。" if internal_timing else ""),
              "- 星泉的整數 `/` 會截斷小數，Python `//` 與 Node.js `Math.trunc` 使用相對應的運算。"
              "浮點測試採用雙精度（星泉使用 `d` 字面值）；標準輸入的整數中間值均在帶正負號的 32 位元範圍內。",
              ("- 陣列建構在各語言採用相同的線性成本：星泉使用 `陣列.建立` 預先配置（快速排序以預留容量的 `陣列.追加`），"
               "Python 使用 `[值] * n`／`append`，Node.js 使用 `push`" + ("，C# 使用 `new T[n]`（必要時 `Array.Fill`）" if has_csharp else "") +
               "；不使用每次複製整個陣列的追加方式。"
               if report.get("schema_version", 0) >= 3 else
               "- 此歷史報告中，Python、Node.js" + (" 與 C#" if has_csharp else "") +
               " 的陣列建構使用每次複製整個陣列的追加方式（平方級成本），星泉則可能已改用預先配置；"
               "篩法、快速排序、矩陣、譜範數與 N 皇后的比較因此偏向星泉。"),
              ("- 編譯時機：星泉的 Wasm 在計時開始前已由 Wasmtime 完整編譯為機器碼。" +
               ("C# 關閉分層編譯，方法在第一次呼叫時即以最佳化 JIT 編譯；" if has_csharp else "") +
               "Node.js（V8）無法預先最佳化，靠程序內暖身讓熱點函式在計時前完成最佳化。"
               "暖身後仍可能有少量 JIT 或垃圾回收落在計時區間內。"
               if warm_runs else
               "- 編譯時機：星泉的 Wasm 在計時開始前已由 Wasmtime 完整編譯為機器碼。" +
               ("C# 關閉分層編譯，方法在第一次呼叫時直接產生最佳化機器碼，但這次 JIT 仍在計時區間內；" if has_csharp else "") +
               "Node.js（V8）無法預先最佳化，先以直譯器與基準編譯器執行，熱點函式的最佳化發生在計時區間內，因此仍偏向星泉。"
               if csharp_optimized or not has_csharp else
               "- 編譯時機不對稱：星泉的 Wasm 在計時開始前已由 Wasmtime 完整編譯為機器碼；" +
               "C#（分層編譯）與 Node.js（V8）的 JIT 編譯與最佳化發生在計時區間內，C# 在約 100 毫秒內幾乎只執行未最佳化程式碼。") +
              ("標準規模每項只需約 1 毫秒，計時器與記憶體配置雜訊比例較高；" if warm_runs else "標準規模每項只需數毫秒，這部分成本偏向星泉；") +
              "`--profile large` 以較大輸入降低此影響，兩種規模的分數不可混用。",
              ("- 小型工作負載可能受計時器與函式呼叫成本影響；只暖身數次，不等於長時間執行的穩態速度，也不代表所有程式的語言排名。"
               if warm_runs else
               "- 小型工作負載可能受計時器與函式呼叫成本影響；每筆樣本使用新程序，未測量持續暖身後的穩態速度，也不代表所有程式的語言排名。") +
              "CPU 頻率、溫度、背景工作與排程雜訊未受控制。未測量程序記憶體用量與 CPU 時間；下方 RAM 為機器配備。", "",
              "## 測試日期與環境", "",
              f"- 開始時間：{md(report['started_at'])}", f"- 結束時間：{md(report['finished_at'])}",
              f"- 時區：{md(config['timezone'])}",
              f"- 輸入規模：{ {'standard': '標準', 'smoke': '快速檢查', 'large': '大型'}.get(config['profile'], config['profile']) }（`{config['profile']}`）；"
              f"每組 {config['repetitions']} 筆正式樣本、{config['warmups']} 筆捨棄的暖身樣本",
              f"- 排序隨機種子：{config['seed']}；每個程序逾時上限：{config['timeout_seconds']:g} 秒",
              f"- 作業系統：{md(env['os'])}", f"- 架構：{md(env['architecture'])}",
              f"- CPU：{md(env['cpu'])}；邏輯處理器：{env['logical_cpus']}",
              f"- 實體 RAM：{env['ram_bytes'] / 1024**3:.2f} GiB" if env['ram_bytes'] else "- 實體 RAM：無法取得",
              f"- 使用中的電源計畫：{md(env['power_plan'] or '無法取得')}",
              f"- Python 主控程式版本：{md(env['python_runner'])}",
              f"- 行程 CPU 親和性遮罩：`{env.get('process_affinity_mask', '未固定／未取得')}`",
              f"- 主控程式診斷計時器解析度：{env['timer_resolution_seconds']:.3g} 秒（非所有語言的計時器解析度）", "",
              "| 執行環境 | 版本／組建 | 執行檔 |", "| --- | --- | --- |"]
    for lang, title in languages.items():
        runtime = report["runtimes"][lang]
        version = runtime.get("version", "無法使用：找不到執行檔")
        if not runtime.get("available"):
            version = "無法使用：" + runtime.get("error", "找不到執行檔")
        if lang in ("aquarius", "aquarius_typed") and runtime.get("available"):
            version = "未提供版本參數；以發行目錄與二進位檔雜湊識別"
        lines.append(f"| {title} | {md(version)} | {md(runtime.get('executable', '無法取得'))} |")
    aqua = report["runtimes"]["aquarius"]
    if aqua.get("available"):
        lines += ["", f"星泉發行目錄：`{aqua['release_directory']}`。", "",
                  f"星泉啟動執行檔 SHA-256：`{aqua['executable_sha256']}`。", ""]
        for filename, fingerprint in aqua.get("assemblies_sha256", {}).items():
            lines.append(f"- `{filename}` SHA-256：`{fingerprint}`")
    lines += ["", "## 各項效能結果", "",
              "耗時單位為毫秒（ms），越低越快。耗時倍率 = 該語言耗時中位數 ÷ Python 耗時中位數；"
              "小於 1 表示該項測試比 Python 快。此耗時倍率與開頭的速度分數方向相反。", "",
              "| 演算法 | n | " + " | ".join(f"{title} 中位數" for title in languages.values()) + " | " +
              " | ".join(f"{title}／Python 耗時倍率" for lang, title in languages.items() if lang != "python") + " |",
              "| --- | ---: | " + " | ".join("---:" for _ in range(2 * len(languages) - 1)) + " |"]
    for name, spec in report["benchmarks"].items():
        summaries = {lang: report["cases"][f"{name}/{lang}"]["summary"] for lang in languages}
        cells = [f"{s['median_ms']:.3f}" if s["status"] == "ok" else STATUS.get(s["status"], s["status"]) for s in summaries.values()]
        def ratio(lang):
            s, py = summaries[lang], summaries["python"]
            return f"{s['median_ms'] / py['median_ms']:.2f} 倍" if s["status"] == py["status"] == "ok" else "—"
        lines.append(f"| {WORKLOADS[name][0]} | {spec['n']} | " + " | ".join(cells) +
                     " | " + " | ".join(ratio(lang) for lang in languages if lang != "python") + " |")
    lines += ["", "### 耗時波動", "", "變異係數（CV）= 樣本標準差 ÷ 平均值。"
              "只有一筆樣本時，無法估計波動，以破折號表示。", "",
              "| 演算法 | 語言 | 最小值 ms | 最大值 ms | 標準差 ms | 變異係數 | 有效樣本 |",
              "| --- | --- | ---: | ---: | ---: | ---: | ---: |"]
    for record in report["cases"].values():
        summary = record["summary"]
        valid = sum(s["status"] == "ok" for s in record["samples"])
        values = ["—"] * 4
        if summary["status"] == "ok":
            values = [f"{summary['min_ms']:.3f}", f"{summary['max_ms']:.3f}",
                      f"{summary['stdev_ms']:.3f}" if config["repetitions"] > 1 else "—",
                      f"{summary['cv_percent']:.1f}%" if config["repetitions"] > 1 else "—"]
        lines.append(f"| {WORKLOADS[record['benchmark']][0]} | {languages[record['language']]} | " +
                     " | ".join(values) + f" | {valid}/{config['repetitions']} |")
    failures = []
    for key, record in report["cases"].items():
        if record.get("unavailable"):
            failures.append(f"- `{key}`：{md(record['unavailable'])}")
        if record.get("build", {}).get("error"):
            failures.append(f"- `{key}`：{md(record['build']['error'])}")
        for phase in ("warmups", "samples"):
            for index, sample in enumerate(record[phase]):
                if sample["status"] != "ok":
                    failures.append(f"- `{key}` {'暖身' if phase == 'warmups' else '正式樣本'} #{index + 1}：{md(sample['error'])}")
    lines += ["", "## 正確性驗證", ""]
    lines += failures or ["所有語言的每筆暖身與正式樣本輸出，均符合 Python 參考答案。"]
    lines += ["", "| 演算法 | 預期結果 | 工作負載 |", "| --- | ---: | --- |"]
    for name, spec in report["benchmarks"].items():
        title, description = WORKLOADS[name]
        lines.append(f"| {title} | {spec['expected']} | {description} |")
    lines += ["", "## 可重現測試資料", "",
              f"- 原始樣本、輸出、指令、執行順序、環境資訊與執行檔／原始碼雜湊：`{report['artifacts']['json']}`",
              f"- 統計摘要與逐筆樣本 CSV：`{report['artifacts']['summary_csv']}`、`{report['artifacts']['samples_csv']}`",
              "- `benchmarks.json`：標準／快速檢查的輸入規模與工作負載定義。",
              "- " + "、".join(f"`benchmarks/{lang}/`" for lang in languages) + "：可獨立執行的測試程式。",
              "- `reference.py`：未納入計時的參考答案；`tests/`：主控程式與參考答案的回歸測試。", "",
              "本 README 由 `run_benchmarks.py` 產生，下次執行時會覆寫。JSON 保留測量當時的原始與暫存腳本、"
              "測試清單、主控程式及參考答案雜湊。指令中的暫存路徑對應當次執行的檔案，測試後會移除。"
              "比較不同測試時，請保留原始碼與相對應的報告。", ""]
    return "\n".join(lines)
