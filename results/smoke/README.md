# AquariusLang、Python、Node.js 桌面執行效能評比

**本次綜合效能：Python 100.00 分、Node.js 73.90 分、AquariusLang 25.47 分（越高越快）。** 相較 Python，Node.js 分數低 26.1%、AquariusLang 分數低 74.5%。

以 Python 為 100 分，將本次 10 項演算法的相對速度等權重取幾何平均。計時包含程式啟動與原始碼載入／編譯，分數代表本機這組腳本的整體執行表現。

| 排名 | 程式語言 | 綜合分數 | 相對 Python 的綜合速度 |
| ---: | --- | ---: | ---: |
| 1 | Python | 100.00 | 1.000 倍 |
| 2 | Node.js | 73.90 | 0.739 倍 |
| 3 | AquariusLang | 25.47 | 0.255 倍 |

綜合分數 = 100 × 幾何平均（各項 Python 耗時中位數 ÷ 該語言耗時中位數）。每項演算法權重相同；只有三種語言在所有選定測試都通過時，才計算綜合分數。不同測試組合與輸入規模的分數不可直接比較。

本專案提供十種經典演算法、三十份可獨立執行的腳本，以及負責驗證結果、產生 README 與 JSON／CSV 報告的 Python 主控程式。

## 執行方式

需求：Python 3.10 以上、Node.js，以及 AquariusLang 桌面 VM（`AquariusDesktopVMREPL` 與隨附相依檔案）。不需要安裝 Python 套件或執行 npm install。Aquarius 腳本使用 AquariusLangTW 的繁體中文關鍵字與雙語內建函式，舊版僅支援英文的直譯器無法執行。

```powershell
python run_benchmarks.py
# 使用較小輸入，快速檢查正確性：
python run_benchmarks.py --profile smoke --repetitions 1 --warmups 0
# 必要時指定執行檔路徑：
python run_benchmarks.py --aquarius "C:\Aquarius\AquariusDesktopVMREPL.exe" --node "C:\Program Files\nodejs\node.exe"
# 僅執行指定演算法：
python run_benchmarks.py --benchmarks fibonacci sieve matrix
# 使用既有資料重新產生 README，不重新測量：
python run_benchmarks.py --report-only results/latest.json
# 執行主控程式與參考答案測試：
python -m unittest discover -s tests -v
```

若 `python` 是尚未設定版本的 pyenv 代理程式，請直接呼叫已安裝的 `python.exe`。主控程式預設使用自身的 Python 直譯器執行測試，也可用 `--python PATH` 指定其他版本。它會搜尋目前程序的 PATH；在 Windows 上也會搜尋使用者與系統的最新 PATH，因此舊終端工作階段也能找到新加入的 Aquarius 路徑。執行環境參數只接受單一執行檔路徑。

主控程式會在暫存目錄建立原始碼副本，只將 `benchmark_n` 的宣告替換為所選輸入規模。直接執行原始腳本時，採用標準規模。每次測量會建立帶有日期的 `results/` 子目錄，並重新產生 `results/latest.json` 與 `README.md`。可使用 `--output-dir`、`--readme`、`--timeout`、`--seed`、`--repetitions`、`--warmups` 自訂測試。結束碼 1 表示至少一個執行環境無法使用或測試驗證失敗；報告仍會保留失敗資訊。

## 測量方法

- 每筆樣本都啟動新的程序。Python 使用 `perf_counter_ns`，測量從啟動至程序結束並擷取輸出的實際經過時間。計時包含原始碼載入、解析／編譯、執行環境啟動、記憶體配置、垃圾回收、演算法與輸出。
- Aquarius 桌面 VM 執行 `.aqua` 原始碼，Python 執行 Python 原始碼，Node.js 使用 V8 執行 JavaScript。計時腳本不使用預編譯腳本瓶、NumPy、原生演算法函式庫、工作執行緒或內建排序。
- 暖身程序的樣本會捨棄，作用是預熱作業系統檔案快取；不同程序之間不保留 JIT 或 VM 狀態。每輪以記錄的隨機種子打亂所有演算法／語言組合，再依序執行。
- 每筆暖身與正式樣本都必須符合未納入計時的 Python 參考答案。整數必須完全相同；譜範數平方的相對容許誤差為 1e-9，絕對容許誤差為 1e-12。非零結束碼、逾時、缺少或多餘的標準輸出、非有限數值、校驗值不符，都會使該測試失敗。
- Aquarius 的整數 `/` 會截斷小數，Python `//` 與 Node.js `Math.trunc` 使用相對應的運算。浮點測試採用雙精度（Aquarius 使用 `d` 字面值）；標準輸入的整數中間值均在帶正負號的 32 位元範圍內。
- Aquarius 的 `push`／`加入` 會複製陣列；Python 與 Node.js 對應的建構步驟也使用複製後追加。因此篩法、排序與矩陣初始化包含平方級的複製成本。這組測試比較相應的基準實作，未針對各語言做極限最佳化。
- 小型工作負載可能主要反映啟動成本。結果未單獨測量穩態演算法速度，也不代表所有程式的語言排名。CPU 頻率、溫度、背景工作與排程雜訊未受控制。未測量程序記憶體用量與 CPU 時間；下方 RAM 為機器配備。

## 測試日期與環境

- 開始時間：2026-10-10T01:29:10.915910+08:00
- 結束時間：2026-10-10T01:29:13.976773+08:00
- 時區：Asia/Taipei
- 輸入規模：快速檢查（`smoke`）；每組 1 筆正式樣本、0 筆捨棄的暖身樣本
- 排序隨機種子：20261010；每個程序逾時上限：120 秒
- 作業系統：Windows-11-10.0.26200-SP0
- 架構：AMD64
- CPU：13th Gen Intel(R) Core(TM) i9-13900H；邏輯處理器：20
- 實體 RAM：31.71 GiB
- 使用中的電源計畫：Power Scheme GUID: 381b4222-f694-41f0-9685-ff5bb260df2e  (Balanced)
- Python 主控程式版本：3.12.10 (tags/v3.12.10:0cc8128, Apr  8 2025, 12:21:36) [MSC v.1943 64 bit (AMD64)]
- 計時器解析度：1e-07 秒

| 執行環境 | 版本／組建 | 執行檔 |
| --- | --- | --- |
| AquariusLang | 未提供版本參數；以發行目錄與二進位檔雜湊識別 | C:\OfficialProjects\AquariusLangTW\dist\releases\AquariusCompiler-win-x64-20261010-003556-3f551a82\aqua\AquariusDesktopVMREPL.exe |
| Python | Python 3.12.10 | C:\Users\templ\.pyenv\pyenv-win\versions\3.12.10\python.exe |
| Node.js | v24.18.0 | C:\Program Files\nodejs\node.EXE |

Aquarius 發行目錄：`C:\OfficialProjects\AquariusLangTW\dist\releases\AquariusCompiler-win-x64-20261010-003556-3f551a82\aqua`。

Aquarius 啟動執行檔 SHA-256：`3d18c10c9b681d6297671b81abaa3f5944de631c272a8b2d532afe1fad42fb7b`。

- `AquariusLangVM.dll` SHA-256：`779f1f8b4e008fe5947f17684e2f12e3b4a9433e61ad11b70774363d4999c8b2`
- `AquariusDesktopVMREPL.dll` SHA-256：`0375b3a4b50d8a017ff23db9893e3ddc3155f4323f4477a603c395eba03c3c05`

## 各項效能結果

耗時單位為毫秒（ms），越低越快。耗時倍率 = 該語言耗時中位數 ÷ Python 耗時中位數；小於 1 表示該項測試比 Python 快。此耗時倍率與開頭的速度分數方向相反。

| 演算法 | n | Aquarius 中位數 | Python 中位數 | Node.js 中位數 | Aquarius／Python 耗時倍率 | Node.js／Python 耗時倍率 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 遞迴費波那契 | 12 | 120.150 | 30.377 | 41.943 | 3.96 倍 | 1.38 倍 |
| 阿克曼函數 | 3 | 130.402 | 33.237 | 44.314 | 3.92 倍 | 1.33 倍 |
| 埃拉托斯特尼篩法 | 100 | 127.984 | 37.562 | 49.623 | 3.41 倍 | 1.32 倍 |
| 快速排序 | 50 | 137.666 | 31.645 | 42.866 | 4.35 倍 | 1.35 倍 |
| 矩陣乘法 | 5 | 124.357 | 38.687 | 48.046 | 3.21 倍 | 1.24 倍 |
| 曼德布洛特集合 | 8 | 143.141 | 39.800 | 42.071 | 3.60 倍 | 1.06 倍 |
| N 皇后問題 | 5 | 140.608 | 34.103 | 44.730 | 4.12 倍 | 1.31 倍 |
| 二元樹 | 5 | 129.305 | 35.163 | 42.387 | 3.68 倍 | 1.21 倍 |
| 譜範數 | 8 | 139.920 | 30.175 | 43.524 | 4.64 倍 | 1.44 倍 |
| 考拉茲猜想 | 100 | 135.405 | 29.118 | 60.812 | 4.65 倍 | 2.09 倍 |

### 耗時波動

變異係數（CV）= 樣本標準差 ÷ 平均值。只有一筆樣本時，無法估計波動，以破折號表示。

| 演算法 | 語言 | 最小值 ms | 最大值 ms | 標準差 ms | 變異係數 | 有效樣本 |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 遞迴費波那契 | AquariusLang | 120.150 | 120.150 | — | — | 1/1 |
| 遞迴費波那契 | Python | 30.377 | 30.377 | — | — | 1/1 |
| 遞迴費波那契 | Node.js | 41.943 | 41.943 | — | — | 1/1 |
| 阿克曼函數 | AquariusLang | 130.402 | 130.402 | — | — | 1/1 |
| 阿克曼函數 | Python | 33.237 | 33.237 | — | — | 1/1 |
| 阿克曼函數 | Node.js | 44.314 | 44.314 | — | — | 1/1 |
| 埃拉托斯特尼篩法 | AquariusLang | 127.984 | 127.984 | — | — | 1/1 |
| 埃拉托斯特尼篩法 | Python | 37.562 | 37.562 | — | — | 1/1 |
| 埃拉托斯特尼篩法 | Node.js | 49.623 | 49.623 | — | — | 1/1 |
| 快速排序 | AquariusLang | 137.666 | 137.666 | — | — | 1/1 |
| 快速排序 | Python | 31.645 | 31.645 | — | — | 1/1 |
| 快速排序 | Node.js | 42.866 | 42.866 | — | — | 1/1 |
| 矩陣乘法 | AquariusLang | 124.357 | 124.357 | — | — | 1/1 |
| 矩陣乘法 | Python | 38.687 | 38.687 | — | — | 1/1 |
| 矩陣乘法 | Node.js | 48.046 | 48.046 | — | — | 1/1 |
| 曼德布洛特集合 | AquariusLang | 143.141 | 143.141 | — | — | 1/1 |
| 曼德布洛特集合 | Python | 39.800 | 39.800 | — | — | 1/1 |
| 曼德布洛特集合 | Node.js | 42.071 | 42.071 | — | — | 1/1 |
| N 皇后問題 | AquariusLang | 140.608 | 140.608 | — | — | 1/1 |
| N 皇后問題 | Python | 34.103 | 34.103 | — | — | 1/1 |
| N 皇后問題 | Node.js | 44.730 | 44.730 | — | — | 1/1 |
| 二元樹 | AquariusLang | 129.305 | 129.305 | — | — | 1/1 |
| 二元樹 | Python | 35.163 | 35.163 | — | — | 1/1 |
| 二元樹 | Node.js | 42.387 | 42.387 | — | — | 1/1 |
| 譜範數 | AquariusLang | 139.920 | 139.920 | — | — | 1/1 |
| 譜範數 | Python | 30.175 | 30.175 | — | — | 1/1 |
| 譜範數 | Node.js | 43.524 | 43.524 | — | — | 1/1 |
| 考拉茲猜想 | AquariusLang | 135.405 | 135.405 | — | — | 1/1 |
| 考拉茲猜想 | Python | 29.118 | 29.118 | — | — | 1/1 |
| 考拉茲猜想 | Node.js | 60.812 | 60.812 | — | — | 1/1 |

## 正確性驗證

所有語言的每筆暖身與正式樣本輸出，均符合 Python 參考答案。

| 演算法 | 預期結果 | 工作負載 |
| --- | ---: | --- |
| 遞迴費波那契 | 144 | 使用樸素遞迴，不使用記憶化。 |
| 阿克曼函數 | 61 | 計算 A(3, n)，測試巢狀遞迴呼叫。 |
| 埃拉托斯特尼篩法 | 25 | 使用布林陣列，計算 2 至 n（含）的質數數量。 |
| 快速排序 | 464184 | 以中間元素為樞紐，原地排序固定種子的線性同餘序列；檢查排序順序與加權校驗值。 |
| 矩陣乘法 | 790 | 使用列優先的一維陣列與 i/j/k 三層迴圈，計算結果矩陣所有元素的總和。 |
| 曼德布洛特集合 | 1462 | 在 [-2, 1) × [-1, 1) 上取 n × n 個點，最多迭代 60 次，累計逃逸迭代次數。 |
| N 皇后問題 | 10 | 以回溯法逐一檢查欄與對角線，計算所有解的數量。 |
| 二元樹 | 504 | 建立八棵深度為 n 的完整二元樹，並遞迴計算節點總數。 |
| 譜範數 | 1.6130176190135865 | 對隱式矩陣執行十輪冪次迭代，輸出譜範數平方，避免使用函式庫平方根。 |
| 考拉茲猜想 | 3142 | 累計起始整數 1 至 n 到達 1 的步數，不使用記憶化。 |

## 可重現測試資料

- 原始樣本、輸出、指令、執行順序、環境資訊與執行檔／原始碼雜湊：`C:\OfficialProjects\AquariusLang_PerformanceBenchmark\results\smoke\20261010-012910-915910\results.json`
- 統計摘要與逐筆樣本 CSV：`C:\OfficialProjects\AquariusLang_PerformanceBenchmark\results\smoke\20261010-012910-915910\summary.csv`、`C:\OfficialProjects\AquariusLang_PerformanceBenchmark\results\smoke\20261010-012910-915910\samples.csv`
- `benchmarks.json`：標準／快速檢查的輸入規模與工作負載定義。
- `benchmarks/aquarius/`、`benchmarks/python/`、`benchmarks/node/`：可獨立執行的測試腳本。
- `reference.py`：未納入計時的參考答案；`tests/`：主控程式與參考答案的回歸測試。

本 README 由 `run_benchmarks.py` 產生，下次執行時會覆寫。JSON 保留測量當時的原始與暫存腳本、測試清單、主控程式及參考答案雜湊。指令中的暫存路徑對應當次執行的檔案，測試後會移除。比較不同測試時，請保留原始碼與相對應的報告。
