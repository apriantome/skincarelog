# === Stage 8: Быстрые фильтры ===
# Project: SkinCareLog
from datetime import date, timedelta


def _today():
    return date.today()


def _start_of_week(today):
    Monday = timedelta(days=0)
    days_since_monday = (today.weekday() - Monday.days) % 7
    return today - timedelta(days=days_since_monday)


def _is_expired(opened, expiry):
    if expiry is None:
        return False
    return expiry < today()


def filter_by_opened(records, predicate):
    return [record for record in records if predicate(record)]


def get_expired_records(records):
    return filter_by_opened(
        records,
        lambda record: _is_expired(record["opened"], record["expiry"]),
    )


def get_this_week_records(records):
    week_start = _start_of_week(_today())
    week_end = week_start + timedelta(days=6)
    return filter_by_opened(
        records,
        lambda record: week_start <= record["opened"] <= week_end,
    )


def get_today_records(records):
    return filter_by_opened(records, lambda record: record["opened"] == _today())


def apply_fast_filters(records, filters):
    result = records
    for name in filters:
        if name == "today":
            result = get_today_records(result)
        elif name == "this_week":
            result = get_this_week_records(result)
        elif name == "expired":
            result = get_expired_records(result)
    return result
