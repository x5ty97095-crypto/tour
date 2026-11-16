# CONTENT_SCHEMA.md — 旅程資料結構

單一旅程範例：`data/trips/2026-kyushu-autumn.json`。本專案用 JSON 當內容資料庫，不建立資料庫伺服器。

## 頂層欄位

| 欄位 | 型別 | 必填 | 用途 |
|---|---|---|---|
| `slug` | string | ✓ | 小寫連字號識別碼，與檔名一致 |
| `title`, `subtitle`, `description` | string | ✓ | 主標、副標、概述 |
| `dateRange`, `duration`, `updatedAt` | string | ✓ | 日期、天數、最後查證日期 |
| `heroImage`, `heroImageAlt` | string | ✓ | HTTPS 直接圖片及替代文字 |
| `imageCredit` | {label,url} | ✓ | 著作權／來源標註 |
| `lodging` | {name,detail} | ✓ | 三語住宿區域與未知項目註明 |
| `flights` | array | 可選 | 已公布航班時刻，非訂位證明 |
| `pretrip` | array | ✓ | 事前注意事項；`level` 為 high 或 medium |
| `days` | array | ✓ | 1–14 天，每一天有 timeline、meals、notes |
| `sources` | array | ✓ | 查證資料來源清單 |

## 日程 `days[]`

每一天必須有 `date`, `weekday`, `number`, `heading`, `theme`, `summary`, `base`, `pace`, `routeText`, `highlights[]`, `meals[]`, `notes[]`。`routeMaps` 為選填的 Google Maps 路線網址。若 Google Maps 的特定交通模式、轉乘或多點路線無法準確呈現，請改成單段地圖連結，不要偽稱為可直接照走的完整路線。

## 行程節點 `highlights[]`

- `time`：`HH:mm–HH:mm`（例 `09:30–10:10`）；跨日航班另在 `details` 註明日期。
- `type`：`feature`, `place`, `transport`, `meal`, `rest`, `flight` 六種之一。
- `title`：`{ "zh": "繁體中文", "en": "English", "ja": "日本語" }`。
- `details`：必填，講清楚停留／交通與可執行細節。
- `tip`：選填，交通轉乘、風險或預約提醒。
- `map`、`source`：選填 HTTPS URL。若有精確票價及營業時間，應附 `source`。

## 餐食 `meals[]`

每項使用 `slot`, `main`, `alternatives`。`main` 使用 `zh`, `en`, `ja`, `why`, `maps`，`source` 可選。備選使用 `zh`, `ja`, `why`, `maps`。如果因團體行程或未知集合點無法推薦確切餐廳，請明確標示彈性限制，不要編造店鋪。

## 來源 `sources[]`

每項為 `{ "name": "來源名稱", "url": "https://..." }`。至少應涵蓋航班／交通、重點場館、特殊票務和一日團。如官方資料與第三方網站衝突，以官方資料為主並保留待查註記。

## 新增示例

1. 新增 `data/trips/2027-kyoto-spring.json`，最少複製既有旅程的**資料結構**，不得複製既有日期或店家當成新資料。
2. 編輯 `data/trips/index.json`：`trips` 加入 `{ "slug": "2027-kyoto-spring", "title": "京都・春日散策", "date": "2027.04.xx–xx", "region": "日本・關西" }`。
3. 開啟 `index.html?trip=2027-kyoto-spring` 驗證；前端模板與 CSS 不需修改。
