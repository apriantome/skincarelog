# === Stage 4: Редактирование записей ===
# Project: SkinCareLog
ALLOWED_EDIT_FIELDS = {"name", "type", "opened_at", "expiry"}


def normalize_field(value):
    if value is None:
        return None
    if isinstance(value, str):
        return value.strip()
    return value


def sanitize_edit(data):
    cleaned = {}
    for key, value in data.items():
        if key not in ALLOWED_EDIT_FIELDS:
            raise ValueError(f"Поле '{key}' нельзя изменить")
        cleaned[key] = normalize_field(value)
    return cleaned


def validate_edit(entity, data):
    sanitized = sanitize_edit(data)
    if not sanitized:
        raise ValueError("Нечего менять")
    if "opened_at" in sanitized and sanitized["opened_at"] > entity.expiry:
        raise ValueError("Дата открытия позже срока годности")
    if "expiry" in sanitized and sanitized["expiry"] is not None:
        if sanitized["opened_at"] is not None and sanitized["opened_at"] > sanitized["expiry"]:
            raise ValueError("Средство уже просрочено при открытии")
    return sanitized


def edit_entity(entity, data):
    sanitized = validate_edit(entity, data)
    for key, value in sanitized.items():
        setattr(entity, key, value)
    return entity


def edit_entity_by_id(entities, entity_id, data):
    for entity in entities:
        if entity.id == entity_id:
            return edit_entity(entity, data)
    raise KeyError(f"Средство с id={entity_id} не найдено")


class SkinCareProduct:
    def __init__(self, product_id, name, type, opened_at, expiry):
        self.id = product_id
        self.name = name
        self.type = type
        self.opened_at = opened_at
        self.expiry = expiry

    def __repr__(self):
        return f"SkinCareProduct(id={self.id}, name={self.name!r}, type={self.type!r})"


if __name__ == "__main__":
    sample = SkinCareProduct(1, "Увлажняющий крем", "Увлажнение", "2024-01-01", "2026-01-01")
    print("До:", sample.name)
    edited = edit_entity_by_id([sample], 1, {"name": "Крем для лица", "opened_at": "2024-06-01"})
    print("После:", edited.name, "| Открыто:", edited.opened_at)

    try:
        edit_entity_by_id([sample], 1, {"type": "Пилинг"})
    except ValueError as error:
        print("Ошибка:", error)

    try:
        edit_entity_by_id([sample], 999, {"name": "Не существует"})
    except KeyError as error:
        print("Ошибка:", error)
