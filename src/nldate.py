from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta


def parse(s: str, today: date | None = None) -> date:
    ref = today or date.today()
    raw = (
        s.lower()
        .replace("st", "")
        .replace("nd", "")
        .replace("rd", "")
        .replace("th", "")
        .replace(".", "")
        .strip()
    )

    try:
        return datetime.strptime(raw, "%Y-%m-%d").date()
    except ValueError:
        pass

    try:
        return datetime.strptime(s.strip(), "%Y/%m/%d").date()
    except ValueError:
        pass

    try:
        return datetime.strptime(raw, "%B %d, %Y").date()
    except ValueError:
        pass

    try:
        return datetime.strptime(raw, "%b %d, %Y").date()
    except ValueError:
        pass

    s = s.strip().lower()

    # ----------------------------
    # 2. simple cases
    # ----------------------------
    if s == "today":
        return ref
    if s == "tomorrow":
        return ref + timedelta(days=1)
    if s == "yesterday":
        return ref - timedelta(days=1)

    # ----------------------------
    # 3. base shift handling
    # ----------------------------
    base = ref

    if "tomorrow" in s.split():
        base = ref + timedelta(days=1)
    elif "yesterday" in s.split():
        base = ref - timedelta(days=1)

    # ----------------------------
    # 4. token parsing
    # ----------------------------
    tokens = s.replace(",", "").lower().split()

    # ----------------------------
    # handle "in X days" pattern
    # ----------------------------
    if tokens[0] == "in":
        value = int(tokens[1])
        unit = tokens[2]

        if unit.startswith("day"):
            return ref + timedelta(days=value)
        if unit.startswith("week"):
            return ref + timedelta(weeks=value)
        if unit.startswith("month"):
            return ref + relativedelta(months=value)
        if unit.startswith("year"):
            return ref + relativedelta(years=value)

    days = weeks = months = years = 0
    direction = None

    direction = None

    if "ago" in tokens or "before" in tokens:
        direction = "before"
    elif "after" in tokens or ("in" in tokens):
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

    # ----------------------------
    # 5. apply accumulated shift
    # ----------------------------
    delta = timedelta(days=days, weeks=weeks)

    if direction == "after":
        return base + delta + relativedelta(months=months, years=years)
    elif direction == "before":
        return base - delta - relativedelta(months=months, years=years)

    return base
