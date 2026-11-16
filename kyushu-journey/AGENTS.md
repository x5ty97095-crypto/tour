# AGENTS.md — 旅程視覺敘事系統（Travel Editorial System）

> 版本：1.1｜目的：讓 AI Coding Agent 在**無須重設網頁風格與元件**的情況下，持續為不同旅程新增內容或頁面。
>
> 本專案是一個**既有行程的呈現引擎**，附帶可選的 Groq「文稿 → JSON」轉檔工具。**不是**會自動研究、查證、預訂或產生全新旅行事實的後端。

## 1. Project Mission / 專案目標

- 將**已完成、人工審閱過的旅遊行程**轉換成精緻、易讀、可在手機操作的互動式旅遊手冊。
- 呈現必須同時保留交通、精確時間區間、地點三語名稱、餐飲備選、來源證據與預約提醒。
- **先完成內容，再開始排版**。前端是資料的忠實呈現，不應為視覺效果自行改變既定的路線、時間或費用。
- 最大化重複使用：新增一個旅程原則上只需新增 **一個 JSON 檔**，並更新一份旅程索引；**不要複製 `index.html`**。

## 2. Tech Stack / 技術邊界

- 前端為原生 HTML5、CSS3、Vanilla JavaScript（ES Modules）、JSON；無資料庫、無 Node runtime。可選 Python 3（standard library）＋ Groq API 用於**離線草稿轉檔**；不用 Groq 時網站仍能正常運作。
- 以 GitHub Pages 部署（`index.html` 為預設首頁）；本地測試需 HTTP Server，**不要直接雙擊檔案用 `file://` 開啟**，因為 `fetch()` 需要本地 HTTP。
- 允許外部可嵌入圖片（附來源）、Google Maps URL；不需要 Google Maps API 金鑰。
- 網頁瀏覽、列印與分享完全不需要 Groq API。需要 AI 將已規劃行程轉為 JSON 時，才由 GitHub Codespaces 中的 `tools/generate_trip.py` 呼叫 Groq；用 Codespaces Secrets 注入 `GROQ_API_KEY`，不得寫入 HTML、JS、Git、JSON 或 GitHub Pages 公開檔案。模型不得擅自改寫旅遊事實。

## 3. Fixed Design Tokens / 不可擅改的視覺規範

必須透過 `assets/style.css` 的 `:root` design tokens 實作，禁止在元件中散落任意硬編碼顏色。

| Token | 色碼 | 使用場合 |
|---|---|---|
| `--mauve` | `#A28F9D` | 章節識別、重要日期、互動強調 |
| `--sage` | `#74776B` | 次要資訊、類別與細節 |
| `--taupe` | `#5C574F` | 一般裝飾性標題 |
| `--olive` | `#48483A` | 主要文字、深色大區塊 |
| `--mint` | `#DFF8EB` | 輕微提示與柔和背景色 |

額外允許中性色 `#FCFAF7`、`#FFFFFF`、`#E7E3DE` 以維持層次與對比；**重要警告不能只靠顏色表示，還需文字**。

### 字體

- 主要閱讀字體：開源 **Noto Sans TC**，weight 300–900，使用 Google Fonts CDN；`font-display: swap`，未載入時 fallback 系統繁體中文字體。
- 編輯式主標題：開源 **獅尾四季春 Swei Spring**，優先引用字體專案文件列明的 jsDelivr 網頁字型，不需把字型上傳至 GitHub 倉庫。若下載失敗，回退 Noto Serif TC / 明體系統字。
- 日文地名以 `lang="ja"` 標記，搭配 `Noto Sans JP` fallback，確保日文字形自然。英文使用字體原生英文字形。
- 內文：手機至少 16px，桌機 16–17px，行高 1.7–1.85；次要資料至少 13px；說明與來源不得用 11px 等難讀字級。
- 頁面最大文字寬度約 70–75ch，主內容 1120px 附近；手機使用單欄版面，點擊區至少 44px 高。

### 風格與節奏

- 時尚、簡約、帶有編輯型旅遊雜誌的留白感：層次清楚、低彩度、細分隔線、大數字日期、有限陰影。
- 用字級、留白、時間軸結構與內容密度形成節奏；**不可把每個景點都做成長得完全相同的大卡片**。
- `feature` 行程強化標題與說明，`transport` 為緊湊交通帶，`meal` 使用餐食標籤，`rest` 採柔和區塊，`flight` 為重點交通標籤；所有變化都由既有 type 渲染，不需每次新增 CSS。
- 強調可讀與可掃描：每個活動先顯示時間、繁中名稱，再顯示英文與日文、短摘要、地圖／來源連結；延伸注意事項視情況展開。

## 4. Information Architecture / 網站架構

```text
/
├── index.html                   # 單一可重複使用的旅行手冊模板
├── assets/
│   ├── style.css                # 所有 design tokens 與響應式樣式
│   └── app.js                   # JSON 載入、日別切換、時間軸與互動
├── data/
│   └── trips/
│       ├── index.json           # 全站旅程清單、預設旅程 slug
│       └── 2026-kyushu-autumn.json  # 第一篇正式旅程
│   └── drafts/                  # Groq 產生的未審草稿（不提交 Git）
├── tools/
│   ├── generate_trip.py         # 使用 Groq 產生 JSON 草稿
│   ├── validate_trip.py         # JSON 契約檢查
│   ├── publish_trip.py          # 審閱後正式發布＋更新索引
│   └── trip_validation.py       # 共用檢查邏輯
├── docs/
│   └── CONTENT_SCHEMA.md       # 資料欄位定義與範本
├── examples/
│   └── itinerary-notes.md      # 供轉檔使用的文稿格式
├── AGENTS.md                    # AI 開發規範
└── README.md                    # 給人看的使用與部署指引
```

`index.html?trip=2026-kyushu-autumn` 指定旅程；不帶參數時讀取 `index.json` 的 `defaultTrip`。新增旅程時不製作 `trip2.html`，也不要在 `app.js` 寫死新內容。

## 5. Content Contract / 新增內容的資料契約

- 將新旅程儲存為 `data/trips/YYYY-region-short-title.json`，`slug` 必須與檔名相同；小寫英數和 `-`，例 `2026-fukuoka-demo.json`。
- 更新 `data/trips/index.json` 的 `trips` 陣列，確保旅程切換器可找到它。
- JSON 必須符合 `docs/CONTENT_SCHEMA.md` 指定欄位、資料型態與命名。
- 所有景點顯示三語：`title.zh`（**繁體中文**主標）、`title.en`（英文）、`title.ja`（日文）；若原本資料只有一種語言，標記 `待補譯`，不可憑空自創正式官方譯名。
- 所有時間必須採 `HH:mm–HH:mm`，**不得混淆台灣與日本時區**；跨日航班日期需另註明。
- 每個排入行程的主要午、晚餐原則上含 `main` + `alternatives`（約兩個），每項有名稱、推薦理由、Google Maps URL。若餐點由旅行團控制，清楚說明不可自由選擇餐廳的限制。
- 網址必須真實可開啟；交通資料、票價、展覽、導覽團須保留 `source` 或列入 `sources`。不確定項目標註推估／待查，**禁止把推測寫成確定班次或已預訂**。
- 引用照片需提供 `heroImage`（HTTP(S) 直接圖片網址）、`heroImageAlt`、`imageCredit` 名稱與來源網址；需有可重複使用的授權（例如 Unsplash License 或相容 CC 授權）。不可直接盜連未知著作權素材。
- 住宿不可曝露個人地址，最多寫到住宿區域及交通樞紐。

## 6. Layout-First? No — Content-First Workflow / 每次新增旅程的固定流程

**必須依下列順序執行；不允許跳過內容核驗而直接做卡片。**

1. 閱讀本文件及 `docs/CONTENT_SCHEMA.md`。
2. 接收一份**已完成**、可人工核對的行程文稿；若時間／地點／交通明顯衝突，先提出待補清單，不得默默修改。
3. 把文稿轉成旅程 JSON；可手動整理，或按第 8 節用 Groq 工具產生**未發布草稿**。保留所有餐廳備選、來源、風險提示與三語地名。
4. 使用現有型別 `feature | place | transport | meal | rest | flight` 決定各節點的**視覺權重**；可以柔性調整 `feature` 比例，但絕不可變更時間或地點。
5. 人工查證內容與格式後，將 JSON 發布至 `data/trips/` 並在 `data/trips/index.json` 加入 slug；可透過 `tools/publish_trip.py` 執行。
6. 在本地 HTTP Server 開啟網頁，逐日核對文字、網址、Google Maps 導航、來源、日期與餐食項目。
7. 於 375px、768px、1440px 三種寬度檢查排版；長日文名稱不可溢出、重要連結可操作、圖片有 fallback。
8. 以瀏覽器列印→另存 PDF，確認**四天全部印出**、連結文字清楚、內容不被卡片截斷。
9. 更新 `README.md` 的新增旅程示例，檢查 console / JSON 解析錯誤後提交 Git。
10. GitHub Pages 部署後，檢查公開網站是否能載入 JSON、字體、圖片及深連結。

**最低驗收標準**：不用改 `index.html`、`assets/app.js`、`assets/style.css`，僅增加 JSON 並更新索引，就能呈現新旅程。

## 7. Editing Rules / AI 修改既有內容的限制

- 未經明確要求，不修改歷史資料的日期、航班、路線、營業時間或餐廳名稱。
- 只改文案／順序時，保持 `slug` 穩定，以免舊分享網址失效。
- 修改 CSS 需優先使用 tokens，不覆蓋公共結構；確認前一個旅程也正常顯示。
- 不得為新旅程增加第三方追蹤碼、API Key、會員登入、資料庫或其他與本次作業無關的功能。
- 不得因「AI 排版建議」隱藏警告、來源、特別交通條件、價格限制。
- JSON 載入失敗要顯示可理解的錯誤，不得呈現空白頁。
- 使用者可按日切換、開啟 Google Maps、開合餐廳備選、列印或分享網址；互動必須真實有效，避免裝飾性死按鈕。

## 8. Optional Groq Draft Agent / 可選 AI 行程 JSON 產生工具

**用途與權限邊界**：這是把「人工已完成、能核對的行程文稿」轉成 JSON 的**轉檔 Agent**，不是自動旅遊研究或資料驗證服務。不可依賴 Groq 杜撰商家、發車班次、票價、圖片、來源 URL，也不可將 AI 回覆當成官方查證。

### 每次新增新旅程的固定指令

1. 在 GitHub Codespaces 準備 `examples/` 或自己建立的 Markdown 文稿，**先將航班、日期、來源、餐食等資料整理清楚**。
2. GitHub 帳號中的 **Codespaces Secrets** 儲存 `GROQ_API_KEY`，允許目前 Repository 使用；若已開啟 Codespace 可能需要重新啟動才能讀到新值。**切勿在對話、Commit、GitHub Pages 或前端檔案中留下私鑰**。
3. 於 repo 根目錄執行：

```bash
python3 tools/generate_trip.py --input examples/itinerary-notes.md --slug 2026-fukuoka-demo --title "福岡一日散策示範"
```

4. 工具只會建立 `data/drafts/2026-fukuoka-demo.json`；**不要跳過人工核對**。有錯誤先編輯草稿，沒有來源的資訊須補查或標記待確認。
5. 人工確認後執行：

```bash
python3 tools/publish_trip.py --slug 2026-fukuoka-demo --approve
python3 tools/validate_trip.py
```

6. `publish_trip.py` 自動建立正式的 `data/trips/2026-fukuoka-demo.json` 並更新 `data/trips/index.json`。在 `http://localhost:8000/?trip=2026-fukuoka-demo` 逐日檢查，確認無誤後才 Git commit、push。

### 不可違反的規則

- 只能使用 `GROQ_API_KEY` 環境變數呼叫 Groq；不准要求把 API Key 寫在網頁或上傳到 Repository。
- Groq API 預設只在 Codespaces **手動觸發**，網頁訪客不會呼叫 Groq；嚴禁在 `assets/app.js` 直接帶金鑰請求 API。
- `generate_trip.py` 使用 Groq JSON Object Mode 產生 JSON，再用 Python 驗證本專案資料契約。**格式驗證不等於事實查證**，任何日期、餐廳、費用、班次或圖片授權仍需人工確認。
- 不可使用沒有原始來源的外部網址作為「查證結果」。Google Maps 搜尋網址只代表導航入口，不代表地址、營業資訊已查證。
- 大型行程可能超出模型單次輸出額度或免費限制；失敗要保留原文、提示分批處理，不得反覆無限重試。
- 無需修改 `index.html`、`assets/app.js`、`assets/style.css` 就能新增一筆內容，這是首要驗收標準。
- `data/drafts/` 不納入 Git，避免未確認的草稿被 GitHub Pages 公開；只提交經審核並發布的正式 JSON。

## 9. Definition of Done / 交付標準

- 首頁可讀、四天內容完整、色系與字體一致，版面在手機可用。
- 有來源、有三語地名、有日期、可操作的地圖連結與餐食備選。
- 可透過新 JSON 建立第二個旅程，不須重複 HTML。
- `AGENTS.md`、`README.md` 與公開 GitHub Pages 網址均可交付。
