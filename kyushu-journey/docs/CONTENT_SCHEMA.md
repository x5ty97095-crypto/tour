# Content contract — TRAVEL / EDITION

這份文件描述 `data/trips/*.json` 的真實渲染格式。與 `assets/app.js` 配套。**前端內容資料格式 ≠ Groq 回傳保證，必須執行 Python 檢查與人工查證。**

## 主結構

`slug, title, subtitle, dateRange, duration, description, heroImage, heroImageAlt, imageCredit, updatedAt, lodging, flights, pretrip, days, sources`

- `slug`：`YYYY-region-short-title`，須與檔名相同。例：`2027-kyoto-spring`。
- `title, subtitle, dateRange, duration, description, updatedAt`：非空字串。
- `heroImage`：合法 HTTP(S) 圖片 URL；**未取得合法授權圖片時保持空字串**，前端會降級顯示。
- `heroImageAlt`：圖片替代描述；無圖可為空。
- `imageCredit`：`{"label":"作者／出處","url":"https://..."}` 或 `null`。
- `lodging`：`{"name":{"zh":"...","en":"...","ja":"..."}, "detail":"..."}`。不可公開 Airbnb 住址。
- `flights`：可空陣列；若有航班，物件欄位為 `direction,date,flight,route,time,note,source`。
- `pretrip`：可空陣列，每項為 `level`（high/medium）、`title, text`、選填 `url`。
- `sources`：可空陣列，元素為 `{"name":"資料來源", "url":"https://..."}`；不得由 AI 杜撰。

## 每日 `days[]`

| Key | 說明 |
|---|---|
| `date` | `11.26` 類型的日期字串 |
| `weekday` | `MON` 到 `SUN` |
| `number` | `01`、`02` 等；字串 |
| `heading`, `theme`, `summary` | 當日標題、主題及摘要 |
| `base`, `pace` | 地點與行程強度 |
| `routeText` | 中文動線，例如「博多 → 太宰府 → 天神」 |
| `routeMaps` | 已提供的 Google Maps 導航 URL，未知可為 `""` |
| `highlights` | 至少一個活動物件，依時間排序 |
| `meals` | 餐食候選清單，可為 `[]` |
| `notes` | 當日風險與提醒文字陣列 |

### `highlights[]` 活動

`time, type, title, details` 必填；`tip, map, source` 可為空字串。

```json
{
  "time": "09:00–10:30",
  "type": "feature",
  "title": {"zh": "大濠公園", "en": "Ohori Park", "ja": "大濠公園"},
  "details": "活動描述。未確定之時刻須寫明待確認。",
  "tip": "注意事項",
  "map": "https://www.google.com/maps/search/?api=1&query=Ohori+Park",
  "source": ""
}
```

`type` 必須為 `transport | feature | place | meal | rest | flight`，且時間格式為 `HH:mm–HH:mm`（例如 `09:00–10:30`）。遇到跨日飛行，應在說明與航班欄位另標日期，不可把不同時區的時刻當同一天時間軸排序。

### `meals[]` 餐食

```json
{
  "slot": "午餐 · 太宰府",
  "main": {
    "zh": "餐廳中文名", "en": "Restaurant English name", "ja": "日本語店名",
    "why": "推薦理由", "maps": "", "source": ""
  },
  "alternatives": [
    {"zh":"備案甲", "ja":"備案甲日文", "why":"理由", "maps":""},
    {"zh":"備案乙", "ja":"備案乙日文", "why":"理由", "maps":""}
  ]
}
```

餐食由人工確認，原則上主選一間、兩間備案。團體行程中餐飲受限應明確說明。

## 產生與發布流程

1. 先整理真實資料成 `examples/itinerary-notes.md` 類型的文稿；未完成資料查核不得宣稱已查證。
2. GitHub Codespaces 透過 `python3 tools/generate_trip.py --input ... --slug ... --title ...` 呼叫 Groq，產生 `data/drafts/slug.json`。
3. 人工審查該草稿，修正與來源不一致之處，尤其是營業時間、班次、費用、店家、三語名稱、圖片授權與 URL。
4. `python3 tools/publish_trip.py --slug ... --approve` 驗證並發布；此步驟會加入 `data/trips/slug.json` 並更新 `data/trips/index.json`。
5. `python3 tools/validate_trip.py` 檢查全部正式旅程；在瀏覽器驗收後再提交 Git。

**注意：** 目前工具以 Groq `json_object` 模式生成，再用本機程式檢查資料契約。JSON 格式正確不代表旅行事實已確認。大型多日行程可能因免費額度、速率或輸出 token 限制失敗；建議分批整理與審閱，不要無限重試。Groq API 不會由 GitHub Pages 直接呼叫。
