from datetime import date, timedelta, strptime
from dateutil.relativedelta import relativedelta
import numpy as np

weekdays = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}


def parse(s: str, today: date | None = None) -> date:
    try:
        return strptime(s, "%Y-%m-%d").date()
    except ValueError:
        pass

    if today is None:
        ref_date = date.today()
    else:
        ref_date = today

    if s.lower() == "today":
        return ref_date

    if s.lower() == "tomorrow":
        return ref_date + timedelta(days=1)

    if s.lower() == "yesterday":
        return ref_date - timedelta(days=1)

    days_to_shift = 0
    weeks_to_shift = 0
    months_to_shift = 0
    years_to_shift = 0

    split_str = np.array(s.replace(",", "").lower().split())

    increase_from_ref = False
    decrease_from_ref = False

    for i in range(len(split_str)):
        curr_word = split_str[i]

        if i != len(split_str) - 1:
            next_word = split_str[i + 1]

        if curr_word.isdigit():
            if next_word == "day" or next_word == "days":
                days_to_shift += int(curr_word)

            elif next_word == "week" or next_word == "weeks":
                weeks_to_shift += int(curr_word)

            elif next_word == "month" or next_word == "months":
                months_to_shift += int(curr_word)

            elif next_word == "year" or next_word == "years":
                years_to_shift += int(curr_word)

        if curr_word == "after":
            increase_from_ref = True

            if next_word == "tomorrow":
                ref_date += timedelta(days=1)

        if curr_word == "before":
            decrease_from_ref = True

            if next_word == "tomorrow":
                ref_date += timedelta(days=1)

        if curr_word == "next":
            if next_word in weekdays.keys():
                return ref_date + timedelta(
                    days=7 + weekdays[next_word] - ref_date.weekday()
                )

        if curr_word == "last":
            if next_word in weekdays.keys():
                return ref_date - timedelta(
                    days=7 - weekdays[next_word] + ref_date.weekday()
                )

    if increase_from_ref:
        return (
            ref_date
            + timedelta(days=days_to_shift)
            + timedelta(weeks=weeks_to_shift)
            + relativedelta(months=months_to_shift)
            + relativedelta(years=years_to_shift)
        )

    if decrease_from_ref:
        return (
            ref_date
            - timedelta(days=days_to_shift)
            - timedelta(weeks=weeks_to_shift)
            - relativedelta(months=months_to_shift)
            - relativedelta(years=years_to_shift)
        )

    return ref_date
