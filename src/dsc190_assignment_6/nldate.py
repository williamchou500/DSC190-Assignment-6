from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta


def parse(s: str, today: date | None = None) -> date:
    if today is None:
        ref = date.today()
    else:
        ref = today

    raw = s.strip().lower()

    # ----------------------------
    # 1. ISO date support
    # ----------------------------
    try:
        return datetime.strptime(raw, "%Y-%m-%d").date()
    except ValueError:
        pass

    # ----------------------------
    # 2. simple cases
    # ----------------------------
    if raw == "today":
        return ref
    if raw == "tomorrow":
        return ref + timedelta(days=1)
    if raw == "yesterday":
        return ref - timedelta(days=1)

    # ----------------------------
    # 3. tokenization
    # ----------------------------
    tokens = raw.replace(",", "").split()

    direction = None  # "after" or "before"

    days = weeks = months = years = 0

    i = 0
    while i < len(tokens):
        t = tokens[i]

        if t in ("after", "before"):
            direction = t

        elif t.isdigit():
            if i + 1 < len(tokens):
                unit = tokens[i + 1]

                if unit.startswith("day"):
                    days += int(t)
                elif unit.startswith("week"):
                    weeks += int(t)
                elif unit.startswith("month"):
                    months += int(t)
                elif unit.startswith("year"):
                    years += int(t)

        elif t == "tomorrow":
            ref = ref + timedelta(days=1)
        elif t == "yesterday":
            ref = ref - timedelta(days=1)

        i += 1

    # ----------------------------
    # 4. apply shifts
    # ----------------------------
    delta = timedelta(days=days, weeks=weeks)

    if direction == "after":
        return ref + delta + relativedelta(months=months, years=years)
    elif direction == "before":
        return ref - delta - relativedelta(months=months, years=years)

    return ref
