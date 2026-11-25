# === Stage 9: Поиск дубликатов ===
# Project: SkinCareLog
import re
from datetime import date


def normalize_name(name: str) -> str:
    text = name.strip().lower()
    text = re.sub(r'[\s\-_]+', ' ', text)
    text = re.sub(r'[(\u0400-\u04FF)]', '', text)
    return text.strip()


def normalize_type(product_type: str) -> str:
    mapping = {
        'cleanser': 'очищение',
        'serum': 'сыворотка',
        'moisturizer': 'увлажнение',
        'sunscreen': 'spf',
        'exfoliant': 'пилинг',
        'toner': 'тоник',
        'mask': 'маска',
    }
    return mapping.get(product_type.strip().lower(), str(product_type).strip().lower())


def parse_open_date(open_date: str) -> date:
    for fmt in ('%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y', '%m/%d/%Y', '%m-%d-%Y'):
        try:
            return date.fromisoformat(open_date.replace('.', '-').replace('/', '-'))
        except ValueError:
            continue
    raise ValueError(f'Неверный формат даты открытия: {open_date!r}')


def parse_expiry_date(expiry_date: str) -> date | None:
    if not expiry_date or expiry_date.strip().lower() in ('', 'nan', 'none', 'н/д'):
        return None
    try:
        return parse_open_date(expiry_date)
    except ValueError:
        return None


def normalize_open_date(open_date: str) -> str:
    parsed = parse_open_date(open_date)
    return parsed.isoformat()


def normalize_expiry_date(expiry_date: str) -> str:
    parsed = parse_expiry_date(expiry_date)
    return parsed.isoformat() if parsed else ''


def normalize_field(value: str, field: str) -> str:
    if value is None:
        return ''
    value = str(value).strip()
    if field == 'name':
        return normalize_name(value)
    if field == 'type':
        return normalize_type(value)
    if field == 'open_date':
        return normalize_open_date(value)
    if field == 'expiry_date':
        return normalize_expiry_date(value)
    return value


def product_signature(product: dict) -> tuple:
    return tuple(
        normalize_field(product.get(field), field)
        for field in ('name', 'type', 'open_date', 'expiry_date')
    )


def find_duplicate_products(products: list) -> list:
    groups: dict[tuple, list] = {}
    for product in products:
        signature = product_signature(product)
        if signature:
            groups.setdefault(signature, []).append(id(product))
    return [products[i] for i, sig in groups.items() if len(groups[sig]) > 1]
