# === Stage 2: Проверка полей ===
# Project: SkinCareLog
import datetime

VALID_TYPES = {
    "cleanser": "Очищающее средство",
    "toner": "Тоник",
    "serum": "Сыворотка",
    "moisturizer": "Увлажняющий крем",
    "sunscreen": "Солнцезащитный крем",
    "mask": "Маска",
    "eye_care": "Уход за глазами",
}


def normalize_input(text):
    return text.strip().lower()


def normalize_type(user_type):
    normalized = normalize_input(user_type)
    if normalized in VALID_TYPES:
        return normalized
    raise ValueError(
        "Неверный тип средства. Доступные типы: "
        + ", ".join(VALID_TYPES.keys())
    )


def normalize_date(value):
    if not value:
        raise ValueError("Дата не может быть пустой.")
    try:
        return datetime.date.fromisoformat(value.strip())
    except ValueError:
        raise ValueError(
            "Дата должна быть в формате ГГГГ-ММ-ДД, например 2024-03-15."
        )


def normalize_name(name):
    if not name or not name.strip():
        raise ValueError("Название средства не может быть пустым.")
    return name.strip()


def validate_product(name, product_type, open_date, expiry_date):
    errors = []

    clean_name = normalize_name(name)
    if not clean_name:
        errors.append("Название средства не может быть пустым.")

    type_key = normalize_type(product_type)

    try:
        open_day = normalize_date(open_date)
    except ValueError as exc:
        errors.append(str(exc))

    try:
        expiry_day = normalize_date(expiry_date)
    except ValueError as exc:
        errors.append(str(exc))

    if open_day and expiry_day and open_day > expiry_day:
        errors.append(
            "Дата окончания годности не может быть раньше даты открытия."
        )

    if errors:
        return None, errors

    return {
        "name": clean_name,
        "type": type_key,
        "type_label": VALID_TYPES[type_key],
        "open_date": open_day,
        "expiry_date": expiry_day,
    }, []
