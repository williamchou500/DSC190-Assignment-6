import nldate
from datetime import date, timedelta


def test_date():
    assert nldate.parse("2025-12-04") == date(2025, 12, 4)


def test_date_slash():
    assert nldate.parse("2025/12/04") == date(2025, 12, 4)


def test_date_string():
    assert nldate.parse("December 1, 2025") == date(2025, 12, 1)


def test_date_string_st():
    assert nldate.parse("December 1st, 2025") == date(2025, 12, 1)


def test_date_string_nd():
    assert nldate.parse("December 2nd, 2025") == date(2025, 12, 2)


def test_date_string_short():
    assert nldate.parse("Dec 2nd, 2025") == date(2025, 12, 2)


def test_date_string_period():
    assert nldate.parse("Dec. 2nd, 2025") == date(2025, 12, 2)


def test_date_string_in_5_days():
    assert nldate.parse("in 5 days") == date(2026, 5, 18)


def test_today():
    assert nldate.parse("Today") == date.today()


def test_tomorrow():
    assert nldate.parse("Tomorrow") == date.today() + timedelta(days=1)


def test_days_before():
    assert nldate.parse("2 days before tomorrow", date(2026, 5, 13)) == date(
        2026, 5, 12
    )


def test_days_after():
    assert nldate.parse("5 days after today", date(2026, 5, 13)) == date(2026, 5, 18)


def test_weeks_before():
    assert nldate.parse("2 weeks before today", date(2026, 5, 13)) == date(2026, 4, 29)


def test_weeks_after():
    assert nldate.parse("1 week after tomorrow", date(2026, 5, 13)) == date(2026, 5, 21)


def test_months_before():
    assert nldate.parse("1 month before today", date(2026, 5, 13)) == date(2026, 4, 13)


def test_months_after():
    assert nldate.parse("1 month after tomorrow", date(2026, 5, 13)) == date(
        2026, 6, 14
    )


def test_years_before():
    assert nldate.parse("3 years before today", date(2026, 5, 13)) == date(2023, 5, 13)


def test_years_after():
    assert nldate.parse("10 years before tomorrow", date(2026, 5, 13)) == date(
        2016, 5, 14
    )


def test_all_before():
    assert nldate.parse(
        "2 years, 1 week, 3 months, and 5 days before today", date(2026, 5, 13)
    ) == date(2024, 2, 1)


def test_all_after():
    assert nldate.parse(
        "2 years, 1 week, 3 months, and 5 days after tomorrow", date(2026, 5, 13)
    ) == date(2028, 8, 26)
