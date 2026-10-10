"""繁體中文 README 與跨演算法綜合分數。只使用報告中的既有實測資料。"""
import math

LANGUAGES = {"aquarius": "星泉", "python": "Python", "node": "Node.js"}
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


def composite_scores(report):
    """Python = 100；各演算法的相對速度等權重取幾何平均。"""
    if not report["benchmarks"]:
        return None
    for name in report["benchmarks"]:
        for language in LANGUAGES:
            summary = report["cases"][f"{name}/{language}"]["summary"]
            value = summary.get("median_ms", 0)
            if summary["status"] != "ok" or not math.isfinite(value) or value <= 0:
                return None
    scores = {}
    for language in LANGUAGES:
        ratios = [report["cases"][f"{name}/python"]["summary"]["median_ms"] /
                  report["cases"][f"{name}/{language}"]["summary"]["median_ms"]
                  for name in report["benchmarks"]]
        scores[language] = 100 * math.exp(sum(math.log(ratio) for ratio in ratios) / len(ratios))
    return scores


def md(value):
    return str(value).replace("|", "\\|").replace("\n", " ").replace("\r", " ")


def generate_readme(report):
    config, env = report["config"], report["environment"]
    scores = composite_scores(report)
    aquarius_timing = "程式啟動與預先編譯 Wasm 載入（Wasm 生成不計入耗時，引擎編譯仍計入）" if config.get("aquarius_mode") == "precompiled" else "程式啟動與原始碼載入／編譯"
    lines = ["# 星泉、Python、Node.js 桌面執行效能評比", ""]
    if scores:
        ranking = sorted(scores, key=scores.get, reverse=True)
        top = ranking[0]
        score_text = "、".join(f"{LANGUAGES[lang]} {scores[lang]:.2f} 分" for lang in ranking)
        gaps = "、".join(f"{LANGUAGES[lang]} 分數低 {(1 - scores[lang] / scores[top]) * 100:.1f}%"
                         for lang in ranking[1:])
        lines += [f"**本次綜合效能：{score_text}（越高越快）。** 相較 {LANGUAGES[top]}，{gaps}。", "",
                  f"以 Python 為 100 分，將本次 {len(report['benchmarks'])} 項演算法的相對速度等權重取幾何平均。"
                  f"計時包含{aquarius_timing}，分數代表本機這組腳本的整體執行表現。", "",
                  "| 排名 | 程式語言 | 綜合分數 | 相對 Python 的綜合速度 |",
                  "| ---: | --- | ---: | ---: |"]
        for place, language in enumerate(ranking, 1):
            lines.append(f"| {place} | {LANGUAGES[language]} | {scores[language]:.2f} | {scores[language] / 100:.3f} 倍 |")
    else:
        lines += ["**本次資料不足以計算三種語言的綜合分數。** 至少一項測試失敗、未完成或執行環境無法使用；"
                  "各項測試狀態列於下方。", ""]
    lines += ["", "綜合分數 = 100 × 幾何平均（各項 Python 耗時中位數 ÷ 該語言耗時中位數）。"
              "每項演算法權重相同；只有三種語言在所有選定測試都通過時，才計算綜合分數。"
              "不同測試組合與輸入規模的分數不可直接比較。", "",
              "本專案提供十種經典演算法、三十份可獨立執行的腳本，以及負責驗證結果、產生 README 與 JSON／CSV 報告的 Python 主控程式。", "",
              "## 執行方式", "",
              "需求：Python 3.10 以上、Node.js，以及星泉 Wasm 編譯器與桌面主機（`aqua`、`AquariusDesktop` 與隨附相依檔案）。"
              "不需要安裝 Python 套件或執行 npm install。星泉腳本使用星泉繁體中文版的繁體中文關鍵字與雙語內建函式，"
              "舊版僅支援英文的直譯器無法執行。", "",
              "```powershell", "python run_benchmarks.py", "# 使用較小輸入，快速檢查正確性：",
              "python run_benchmarks.py --profile smoke --repetitions 1 --warmups 0",
              "# 必要時指定執行檔路徑：",
              'python run_benchmarks.py --aquarius "C:\\Aquarius\\AquariusDesktop.exe" --node "C:\\Program Files\\nodejs\\node.exe"',
              "# 僅執行指定演算法：", "python run_benchmarks.py --benchmarks fibonacci sieve matrix", "# 編譯於計時前完成，測量部署的 Wasm 程式：", "python run_benchmarks.py --aquarius C:\\Aquarius\\aqua.exe --aquarius-mode precompiled",
              "# 使用既有資料重新產生 README，不重新測量：",
              "python run_benchmarks.py --report-only results/latest.json",
              "# 執行主控程式與參考答案測試：", "python -m unittest discover -s tests -v", "```", "",
              "若 `python` 是尚未設定版本的 pyenv 代理程式，請直接呼叫已安裝的 `python.exe`。"
              "主控程式預設使用自身的 Python 直譯器執行測試，也可用 `--python PATH` 指定其他版本。"
              "它會搜尋目前程序的 PATH；在 Windows 上也會搜尋使用者與系統的最新 PATH，"
              "因此舊終端工作階段也能找到新加入的星泉路徑。執行環境參數只接受單一執行檔路徑。", "",
              "主控程式會在暫存目錄建立原始碼副本，只將 `benchmark_n` 的宣告替換為所選輸入規模。"
              "直接執行原始腳本時，採用標準規模。每次測量會建立帶有日期的 `results/` 子目錄，"
              "並重新產生 `results/latest.json` 與 `README.md`。"
              "可使用 `--output-dir`、`--readme`、`--timeout`、`--seed`、`--repetitions`、`--warmups` 自訂測試。"
              "結束碼 1 表示至少一個執行環境無法使用或測試驗證失敗；報告仍會保留失敗資訊。", "",
              "## 測量方法", "",
              "- 每筆樣本都啟動新的程序。Python 使用 `perf_counter_ns`，測量從啟動至程序結束並擷取輸出的實際經過時間。"
              "計時包含執行環境啟動、引擎編譯、記憶體配置、垃圾回收、演算法與輸出；source 模式也計入星泉原始碼編譯。",
              "- 星泉 source 模式使用 AquariusDesktop 執行原始碼；precompiled 模式使用 aqua 在計時前建立 Wasm，再計時 aqua run。"
              "Python 執行原始碼，Node.js 使用 V8；沒有 NumPy、原生演算法函式庫、工作執行緒或內建排序。",
              "- 暖身程序的樣本會捨棄，作用是預熱作業系統檔案快取；不同程序之間不保留 JIT 或 VM 狀態。"
              "每輪以記錄的隨機種子打亂所有演算法／語言組合，再依序執行。",
              "- 每筆暖身與正式樣本都必須符合未納入計時的 Python 參考答案。整數必須完全相同；"
              "譜範數平方的相對容許誤差為 1e-9，絕對容許誤差為 1e-12。"
              "非零結束碼、逾時、缺少或多餘的標準輸出、非有限數值、校驗值不符，都會使該測試失敗。",
              "- 星泉的整數 `/` 會截斷小數，Python `//` 與 Node.js `Math.trunc` 使用相對應的運算。"
              "浮點測試採用雙精度（星泉使用 `d` 字面值）；標準輸入的整數中間值均在帶正負號的 32 位元範圍內。",
              "- 星泉的 `push`／`加入` 會複製陣列；Python 與 Node.js 對應的建構步驟也使用複製後追加。"
              "因此篩法、排序與矩陣初始化包含平方級的複製成本。這組測試比較相應的基準實作，未針對各語言做極限最佳化。",
              "- 小型工作負載可能主要反映啟動成本。結果未單獨測量穩態演算法速度，也不代表所有程式的語言排名。"
              "CPU 頻率、溫度、背景工作與排程雜訊未受控制。未測量程序記憶體用量與 CPU 時間；下方 RAM 為機器配備。", "",
              "## 測試日期與環境", "",
              f"- 開始時間：{md(report['started_at'])}", f"- 結束時間：{md(report['finished_at'])}",
              f"- 時區：{md(config['timezone'])}",
              f"- 輸入規模：{'標準' if config['profile'] == 'standard' else '快速檢查'}（`{config['profile']}`）；"
              f"每組 {config['repetitions']} 筆正式樣本、{config['warmups']} 筆捨棄的暖身樣本",
              f"- 排序隨機種子：{config['seed']}；每個程序逾時上限：{config['timeout_seconds']:g} 秒",
              f"- 作業系統：{md(env['os'])}", f"- 架構：{md(env['architecture'])}",
              f"- CPU：{md(env['cpu'])}；邏輯處理器：{env['logical_cpus']}",
              f"- 實體 RAM：{env['ram_bytes'] / 1024**3:.2f} GiB" if env['ram_bytes'] else "- 實體 RAM：無法取得",
              f"- 使用中的電源計畫：{md(env['power_plan'] or '無法取得')}",
              f"- Python 主控程式版本：{md(env['python_runner'])}",
              f"- 行程 CPU 親和性遮罩：`{env.get('process_affinity_mask', '未固定／未取得')}`",
              f"- 計時器解析度：{env['timer_resolution_seconds']:.3g} 秒", "",
              "| 執行環境 | 版本／組建 | 執行檔 |", "| --- | --- | --- |"]
    for lang, title in LANGUAGES.items():
        runtime = report["runtimes"][lang]
        version = runtime.get("version", "無法使用：找不到執行檔")
        if lang == "aquarius" and runtime.get("available"):
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
              "| 演算法 | n | 星泉中位數 | Python 中位數 | Node.js 中位數 | 星泉／Python 耗時倍率 | Node.js／Python 耗時倍率 |",
              "| --- | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for name, spec in report["benchmarks"].items():
        summaries = {lang: report["cases"][f"{name}/{lang}"]["summary"] for lang in LANGUAGES}
        cells = [f"{s['median_ms']:.3f}" if s["status"] == "ok" else STATUS.get(s["status"], s["status"]) for s in summaries.values()]
        def ratio(lang):
            s, py = summaries[lang], summaries["python"]
            return f"{s['median_ms'] / py['median_ms']:.2f} 倍" if s["status"] == py["status"] == "ok" else "—"
        lines.append(f"| {WORKLOADS[name][0]} | {spec['n']} | " + " | ".join(cells) +
                     f" | {ratio('aquarius')} | {ratio('node')} |")
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
        lines.append(f"| {WORKLOADS[record['benchmark']][0]} | {LANGUAGES[record['language']]} | " +
                     " | ".join(values) + f" | {valid}/{config['repetitions']} |")
    failures = []
    for key, record in report["cases"].items():
        if record.get("unavailable"):
            failures.append(f"- `{key}`：找不到執行檔，請指定執行環境路徑。")
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
              "- `benchmarks/aquarius/`、`benchmarks/python/`、`benchmarks/node/`：可獨立執行的測試腳本。",
              "- `reference.py`：未納入計時的參考答案；`tests/`：主控程式與參考答案的回歸測試。", "",
              "本 README 由 `run_benchmarks.py` 產生，下次執行時會覆寫。JSON 保留測量當時的原始與暫存腳本、"
              "測試清單、主控程式及參考答案雜湊。指令中的暫存路徑對應當次執行的檔案，測試後會移除。"
              "比較不同測試時，請保留原始碼與相對應的報告。", ""]
    return "\n".join(lines)
