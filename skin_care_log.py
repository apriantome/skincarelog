# === Stage 1: Каркас модуля ===
# Project: SkinCareLog
from dataclasses import dataclass, field
from datetime import date


@dataclass
class SkincareProduct:
    """Средство для ухода за кожей."""

    name: str
    type: str
    opened_at: date
    expiry: date
    notes: str = field(default="")


def make_demo_products() -> list[SkincareProduct]:
    """Создаёт демонстрационные записи о средствах."""

    return [
        SkincareProduct(
            name="Сыворотка с ниацинамидом",
            type="serum",
            opened_at=date(2025, 1, 10),
            expiry=date(2026, 1, 10),
            notes="Утро, после тоника",
        ),
        SkincareProduct(
            name="Увлажняющий крем",
            type="cream",
            opened_at=date(2024, 11, 5),
            expiry=date(2025, 11, 5),
            notes="Вечер, финальный шаг",
        ),
        SkincareProduct(
            name="Очищающий гель",
            type="cleanser",
            opened_at=date(2025, 2, 1),
            expiry=date(2026, 2, 1),
            notes="Утро и вечер",
        ),
    ]


def main() -> None:
    products = make_demo_products()

    print("SkinCareLog — дневник ухода за кожей")
    print("=" * 40)

    for product in products:
        days_left = (product.expiry - product.opened_at).days
        status = "в норме" if days_left >= 0 else "просрочено!"
        print(f"• {product.name} ({product.type})")
        print(f"  открыто: {product.opened_at}  срок: {product.expiry}  {status}")
        print(f"  примечание: {product.notes}\n")


if __name__ == "__main__":
    main()
