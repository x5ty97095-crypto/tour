"""Validation shared by the optional Groq import flow and the publishing tool.

Uses Python's standard library; does not make network calls.
"""
from __future__ import annotations

import re
from urllib.parse import urlparse

SLUG_RE = re.compile(r"^[0-9]{4}-[a-z0-9]+(?:-[a-z0-9]+)*$")
TIME_RE = re.compile(r"^([01]\d|2[0-3]):[0-5]\d[–-]([01]\d|2[0-3]):[0-5]\d$")
ALLOWED_TYPES = {"transport", "feature", "place", "meal", "rest", "flight"}


def valid_url(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    p = urlparse(value)
    return p.scheme in {"http", "https"} and bool(p.netloc)


def validate_trip(trip: object) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(trip, dict):
        return ["旅程最外層必須是 JSON 物件"], warnings

    def reqstr(obj: object, key: str, path: str, required: bool = True) -> str:
        value = obj.get(key) if isinstance(obj, dict) else None
        if required and (not isinstance(value, str) or not value.strip()):
            errors.append(f"{path}.{key} 必須是非空文字")
            return ""
        if value is not None and not isinstance(value, str):
            errors.append(f"{path}.{key} 必須是文字")
            return ""
        return value or ""

    slug = reqstr(trip, "slug", "trip")
    if slug and not SLUG_RE.fullmatch(slug):
        errors.append("trip.slug 應為 YYYY-region-short-title，例如 2027-kyoto-spring")
    for k in ("title", "subtitle", "dateRange", "duration", "description", "updatedAt"):
        reqstr(trip, k, "trip")
    for k in ("heroImage", "heroImageAlt"):
        reqstr(trip, k, "trip", required=False)
    if trip.get("heroImage") and not valid_url(trip["heroImage"]):
        errors.append("trip.heroImage 必須是 http(s) 圖片網址，或保留空白")
    credit = trip.get("imageCredit")
    if credit is not None:
        if not isinstance(credit, dict):
            errors.append("trip.imageCredit 必須是物件或 null")
        else:
            reqstr(credit, "label", "trip.imageCredit")
            u = reqstr(credit, "url", "trip.imageCredit")
            if u and not valid_url(u): errors.append("trip.imageCredit.url 格式錯誤")
    lodging = trip.get("lodging")
    if not isinstance(lodging, dict):
        errors.append("trip.lodging 必須是物件")
    else:
        name = lodging.get("name")
        if not isinstance(name, dict):
            errors.append("trip.lodging.name 必須有 zh/en/ja 三語")
        else:
            for lang in ("zh", "en", "ja"): reqstr(name, lang, "trip.lodging.name")
        reqstr(lodging, "detail", "trip.lodging", required=False)

    for field in ("flights", "pretrip", "sources"):
        if not isinstance(trip.get(field), list): errors.append(f"trip.{field} 必須是陣列（無資料時用 []）")
    for si, s in enumerate(trip.get("sources", []) if isinstance(trip.get("sources"), list) else []):
        reqstr(s, "name", f"sources[{si}]")
        u = reqstr(s, "url", f"sources[{si}]")
        if u and not valid_url(u): errors.append(f"sources[{si}].url 不合法")

    days = trip.get("days")
    if not isinstance(days, list) or not days:
        errors.append("trip.days 必須至少包含一天")
        return errors, warnings
    if len(days) > 14: errors.append("trip.days 最多支援 14 天")
    for di, day in enumerate(days):
        path = f"days[{di}]"
        for key in ("date", "weekday", "number", "heading", "theme", "summary", "base", "pace", "routeText"):
            reqstr(day, key, path)
        route_url = reqstr(day, "routeMaps", path, required=False)
        if route_url and not valid_url(route_url): errors.append(f"{path}.routeMaps 不合法")
        if not isinstance(day, dict): continue
        highlights = day.get("highlights")
        if not isinstance(highlights, list) or not highlights:
            errors.append(f"{path}.highlights 必須包含至少一個事件")
            highlights = []
        for hi, h in enumerate(highlights):
            hp = f"{path}.highlights[{hi}]"
            tm = reqstr(h, "time", hp)
            if tm and not TIME_RE.fullmatch(tm): errors.append(f"{hp}.time 必須是 HH:mm–HH:mm，例如 09:00–10:30")
            typ = reqstr(h, "type", hp)
            if typ and typ not in ALLOWED_TYPES: errors.append(f"{hp}.type 不支援：{typ}")
            title = h.get("title") if isinstance(h, dict) else None
            if not isinstance(title, dict):
                errors.append(f"{hp}.title 必須包含 zh/en/ja")
            else:
                for lang in ("zh", "en", "ja"): reqstr(title, lang, f"{hp}.title")
            reqstr(h, "details", hp)
            for k in ("map", "source"):
                u = reqstr(h, k, hp, required=False)
                if u and not valid_url(u): errors.append(f"{hp}.{k} 必須是 http(s) 網址")
            if isinstance(h, dict) and h.get("type") in {"transport", "flight", "feature"} and not h.get("source"):
                warnings.append(f"{hp} 未附來源網址，若涉及營業時間／交通班次請人工確認")
        meals = day.get("meals", [])
        if not isinstance(meals, list):
            errors.append(f"{path}.meals 必須是陣列")
            meals = []
        for mi, meal in enumerate(meals):
            mp = f"{path}.meals[{mi}]"
            reqstr(meal, "slot", mp)
            main = meal.get("main") if isinstance(meal, dict) else None
            if not isinstance(main, dict):
                errors.append(f"{mp}.main 必須是物件")
            else:
                for k in ("zh", "ja", "why"): reqstr(main, k, f"{mp}.main")
                u = reqstr(main, "maps", f"{mp}.main", required=False)
                if u and not valid_url(u): errors.append(f"{mp}.main.maps 不合法")
            alts = meal.get("alternatives") if isinstance(meal, dict) else None
            if not isinstance(alts, list):
                errors.append(f"{mp}.alternatives 必須是陣列")
                continue
            if len(alts) < 2: warnings.append(f"{mp} 目前不足兩間餐飲備選")
            for ai, alt in enumerate(alts):
                ap = f"{mp}.alternatives[{ai}]"
                for k in ("zh", "ja", "why"): reqstr(alt, k, ap)
                u = reqstr(alt, "maps", ap, required=False)
                if u and not valid_url(u): errors.append(f"{ap}.maps 不合法")
        if not isinstance(day.get("notes"), list): errors.append(f"{path}.notes 必須是陣列")
    return errors, warnings
