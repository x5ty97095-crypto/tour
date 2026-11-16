# TRAVEL / EDITION — 行家級旅遊行程視覺手冊

以「先確認內容，再排版」為原則的旅遊手冊網站。第一篇為 **2026/11/26–11/29 九州四天三夜**：福岡、大濠公園、太宰府、由布院・別府（一日團）、門司港與小倉。

專案主題不再是即時 AI 旅遊規劃器，而是**可重複使用的旅遊行程呈現規則系統**：透過 `AGENTS.md` 規範結構、內容格式、字體、色彩、圖片與測試方式。新增新旅程只需要新增 JSON，無須重做前端。

## 技術

HTML5 + CSS3 + Vanilla JavaScript + JSON；無額外套件、無 API Key、無資料庫。Google Maps 直接使用不需金鑰的 URL。可直接部署至 GitHub Pages。

## 本地啟動

在專案根目錄執行：

```bash
python3 -m http.server 8000
```

在瀏覽器開啟 `http://localhost:8000/`。切勿直接雙擊 `index.html`：因使用 `fetch()` 載入 JSON，`file://` 可能受到同源限制。

## 目錄

- `AGENTS.md`：AI Coding Agent 必須閱讀的規範（重點交付）。
- `docs/CONTENT_SCHEMA.md`：旅程 JSON 契約。
- `data/trips/index.json`：旅程註冊清單。
- `data/trips/2026-kyushu-autumn.json`：完整四天行程。
- `index.html`：所有旅程共用的網頁模板。
- `assets/app.js`：讀取 JSON、每日切換、餐食備選、地圖及分享、列印。
- `assets/style.css`：五色設計系統、繁中開源字體、桌機與手機版型。

## 如何新增旅程？

先閱讀 `AGENTS.md`，並：

1. 把審核完成的新旅程寫為 `data/trips/YYYY-region-title.json`。
2. 在 `data/trips/index.json` 加上新旅程的 `slug`、`title`、`date` 與 `region`。
3. 開啟 `/?trip=YOUR-SLUG` 檢查四天（或其他天數）全部顯示。
4. 測試手機版面、Google Maps 連結、航班跨日、餐食與 PDF 列印。

這套流程可套用京都、東京、北海道等新頁面，**不必要求 AI 再自行設計排版**。

## GitHub Pages 部署

1. 建立公開 GitHub Repository 並將此資料夾全部 push 至 `main`。
2. Repository → Settings → Pages → Build and deployment → Source 選擇 **Deploy from a branch**。
3. Branch 選 **main**、Folder 選 **/(root)**，儲存並等待部署。
4. 到 `https://<username>.github.io/<repository>/` 瀏覽。此專案全用**相對路徑**，支援 project-site 子路徑。

```bash
git init
git add .
git commit -m "feat: launch reusable travel editorial website"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

> 此封裝不包含 GitHub 帳號憑證，不能代替你建立公開儲存庫。推送前請自行確認 repository 名稱與帳號。

## 資料邊界

- 旅程依 2026/11/16 查到的公開官方、平台資料製作，**不代表機票、住宿、一日團已有訂位**。
- 交通窗口以可行動線估算，**不是特定車次保證**，實際請查當日公告。
- 一日團 11/28 空位未完成實際預訂確認；時段依上架範例。
- 航班、門票與平台商品可能調整，出發前仍需確認。
- 圖片使用 Unsplash License 的授權作品（來源於旅程 JSON）。字型使用 SIL OFL 1.1 開源字體。網站不另上傳字型檔。

## 作業繳交用簡介（可直接改寫）

專案以一份九州四天三夜旅行行程為範例，打造可重複使用的旅遊內容展示網站。`AGENTS.md` 定義了視覺色彩、三語地名、時間軸、交通／餐飲／警示元件、檔案命名與資料驗證流程。以後新增旅程只須新增結構化 JSON 並更新索引，AI 就能沿用相同的排版規則，不必重新開發網頁。
