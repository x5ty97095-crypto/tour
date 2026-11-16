#!/usr/bin/env python3
"""Publish a manually reviewed draft and register it in the site index."""
import argparse
import json
from pathlib import Path
from trip_validation import SLUG_RE, validate_trip

ROOT = Path(__file__).resolve().parents[1]


def main():
    p = argparse.ArgumentParser(description="核對後發布行程草稿，更新旅程索引")
    p.add_argument("--slug", required=True)
    p.add_argument("--approve", action="store_true", help="已人工確認資料真實性和授權，可正式發布")
    args = p.parse_args()
    if not SLUG_RE.fullmatch(args.slug): p.error("slug 不符合 YYYY-region-name 格式")
    draft = ROOT / "data" / "drafts" / f"{args.slug}.json"
    target = ROOT / "data" / "trips" / f"{args.slug}.json"
    index_path = ROOT / "data" / "trips" / "index.json"
    if not draft.is_file(): p.error(f"找不到草稿：{draft}")
    if target.exists(): p.error(f"正式旅程已存在，為避免覆寫已中止：{target}")
    try:
        trip = json.loads(draft.read_text(encoding="utf-8"))
        index = json.loads(index_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as err:
        p.error(f"資料讀取失敗：{err}")
    errors, warnings = validate_trip(trip)
    if trip.get("slug") != args.slug: errors.append("slug 與檔案名稱不同")
    for e in errors: print("[錯誤]", e)
    for w in warnings: print("[提醒]", w)
    if errors: p.error("請先修正格式錯誤")
    if not args.approve:
        print("格式驗證通過；仍需人工確認航班、交通、時程、票價、來源及圖片授權。")
        print(f"確認後執行：python3 tools/publish_trip.py --slug {args.slug} --approve")
        return
    if not isinstance(index.get("trips"), list): p.error("index.json 缺少 trips 陣列")
    if any(x.get("slug") == args.slug for x in index["trips"]): p.error("索引中已有相同 slug")
    index["trips"].append({"slug": args.slug, "title": trip["title"],
                           "date": trip["dateRange"], "region": trip["lodging"]["name"]["zh"]})
    # Retain the previous defaultTrip: publishing a trip does not silently change the homepage.
    target.write_text(json.dumps(trip, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"已發布：{target.relative_to(ROOT)}，索引已更新。請再於瀏覽器核對後提交 Git。")


if __name__ == "__main__": main()
