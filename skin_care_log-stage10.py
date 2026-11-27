# === Stage 10: Слияние записей ===
# Project: SkinCareLog
import random
from datetime import date


def _parse_date(value):
    if value is None or value == "":
        return None
    try:
        return date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


def _merge_scalar(current, incoming, field, strategy):
    if current is None:
        return incoming
    if incoming is None:
        return current
    if strategy == "winner":
        return _pick_winner(current, incoming)
    return incoming


def _pick_winner(a, b):
    if isinstance(a, date) and isinstance(b, date):
        return a if a <= b else b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a if a >= b else b
    if a == b:
        return a
    return random.choice([a, b])


def merge_skincare_record(current, incoming, fields):
    if current is None:
        return dict(incoming)
    if incoming is None:
        return dict(current)

    merged = dict(current)
    for field in fields:
        merged[field] = _merge_scalar(
            current.get(field),
            incoming.get(field),
            field,
            "winner",
        )
    return merged


def merge_skincare_records(current, incoming, fields):
    if current is None:
        return dict(incoming)
    if incoming is None:
        return dict(current)
    merged = dict(current)
    for field in fields:
        merged[field] = _pick_winner(current.get(field), incoming.get(field))
    return merged
