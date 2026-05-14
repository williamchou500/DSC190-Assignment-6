from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
import re


def try_parse_date(s: str) -> date | None:
    formats = (
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%B %d, %Y",
        "%b %d, %Y",
    )

    for fmt in formats:
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            pass

    return None


def parse(s: str, today: date | None = None) -> date:
    ref = today or date.today()
    raw = s.replace(".", "").strip()

    raw = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", raw)

    parsed = try_parse_date(raw)

    if parsed is not None:
        return parsed

    match = re.search(r"([A-Za-z]+ \d{1,2}, \d{4})", raw)

    embedded_patterns = [
        r"\d{4}-\d{2}-\d{2}",
        r"\d{4}/\d{2}/\d{2}",
        r"[A-Za-z]+ \d{1,2}, \d{4}",
    ]

    embedded_date = None

    for pattern in embedded_patterns:
        match = re.search(pattern, raw)

        if match:
            date_str = match.group(0)

            parsed = try_parse_date(date_str)

            if parsed is not None:
                embedded_date = parsed
                break

    number_words = {
        "a": 1,
        "an": 1,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
    }

    s = s.strip().lower()

    if s == "today":
        return ref
    if s == "tomorrow":
        return ref + timedelta(days=1)
    if s == "yesterday":
        return ref - timedelta(days=1)
    if "day after tomorrow" in s:
        ref = today or date.today()
        return ref + timedelta(days=2)
    if "the day after tomorrow" in s:
        ref = today or date.today()
        return ref + timedelta(days=2)
    if "day before yesterday" in s:
        ref = today or date.today()
        return ref - timedelta(days=2)
    if "the day before yesterday" in s:
        ref = today or date.today()
        return ref - timedelta(days=2)

    base = embedded_date or ref

    tokens = s.replace(",", "").lower().split()

    if "tomorrow" in tokens:
        base = base + timedelta(days=1)

    if "yesterday" in tokens:
        base = base - timedelta(days=1)

    if tokens[0] == "in":
        value = int(tokens[1])
        unit = tokens[2]

        if unit.startswith("day"):
            return base + timedelta(days=value)
        if unit.startswith("week"):
            return base + timedelta(weeks=value)
        if unit.startswith("month"):
            return base + relativedelta(months=value)
        if unit.startswith("year"):
            return base + relativedelta(years=value)
    days = weeks = months = years = 0
    direction = None

    direction = None

    if "ago" in tokens or "before" in tokens:
        direction = "before"
    elif (
        "after" in tokens or ("in" in tokens) or ("from" in tokens and "now" in tokens)
    ):
        direction = "after"

    i = 0
    while i < len(tokens):
        t = tokens[i]

        if t.isdigit() and i + 1 < len(tokens):
            unit = tokens[i + 1]

            if unit.startswith("day"):
                days += int(t)
            elif unit.startswith("week"):
                weeks += int(t)
            elif unit.startswith("month"):
                months += int(t)
            elif unit.startswith("year"):
                years += int(t)

        elif t in number_words and i + 1 < len(tokens):
            unit = tokens[i + 1]

            unit_increase = number_words[t]

            if unit.startswith("day"):
                days += int(unit_increase)
            elif unit.startswith("week"):
                weeks += int(unit_increase)
            elif unit.startswith("month"):
                months += int(unit_increase)
            elif unit.startswith("year"):
                years += int(unit_increase)

        elif t == "next" and i + 1 < len(tokens):
            wd = tokens[i + 1]
            if wd in {
                "monday",
                "tuesday",
                "wednesday",
                "thursday",
                "friday",
                "saturday",
                "sunday",
            }:
                weekday_map = {
                    "monday": 0,
                    "tuesday": 1,
                    "wednesday": 2,
                    "thursday": 3,
                    "friday": 4,
                    "saturday": 5,
                    "sunday": 6,
                }
                target = weekday_map[wd]
                return base + timedelta(days=(7 + target - base.weekday()) % 7)

        elif t == "last" and i + 1 < len(tokens):
            wd = tokens[i + 1]
            if wd in {
                "monday",
                "tuesday",
                "wednesday",
                "thursday",
                "friday",
                "saturday",
                "sunday",
            }:
                weekday_map = {
                    "monday": 0,
                    "tuesday": 1,
                    "wednesday": 2,
                    "thursday": 3,
                    "friday": 4,
                    "saturday": 5,
                    "sunday": 6,
                }
                target = weekday_map[wd]
                return base - timedelta(days=(7 - target + base.weekday()) % 7)

        i += 1

    delta = timedelta(days=days, weeks=weeks)

    if direction == "after":
        return base + delta + relativedelta(months=months, years=years)
    elif direction == "before":
        return base - delta - relativedelta(months=months, years=years)

    valid_patterns = [
        r"\d",
        r"today|tomorrow|yesterday",
        r"ago|before|after|in|from|next|last",
    ]

    if not any(re.search(p, s.lower()) for p in valid_patterns):
        raise ValueError()

    return base
