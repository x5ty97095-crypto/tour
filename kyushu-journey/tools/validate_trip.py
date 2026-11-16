#!/usr/bin/env python3
"""Validate one or all published itineraries. Run from repository root."""
import argparse
import json
from pathlib import Path
from trip_validation import validate_trip

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description="驗證旅程 JSON 是否符合既有網頁資料契約")
    parser.add_argument("paths", nargs="*", help="JSON paths (default: data/trips/*.json excluding index.json)")
    args = parser.parse_args()
    files = [Path(p) for p in args.paths] if args.paths else sorted((ROOT / "data" / "trips").glob("*.json"))
    files = [p for p in files if p.name != "index.json"]
    if not files:
        parser.error("沒有找到行程 JSON")
    failed = False
    for f in files:
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
            errors, warnings = validate_trip(d)
            if isinstance(d, dict) and d.get("slug") != f.stem: errors.append("slug 與檔案名稱不一致")
        except (OSError, json.JSONDecodeError) as e:
            errors, warnings = [str(e)], []
        print(f"\n{'FAIL' if errors else 'PASS'} {f}")
        for error in errors: print("  錯誤：", error)
        for warning in warnings: print("  提醒：", warning)
        failed |= bool(errors)
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__": main()
