# === Stage 3: Хранилище в памяти ===
# Project: SkinCareLog
from datetime import date


class SkinProduct:
    def __init__(self, name, product_type, opened_on, expiry):
        self.id = None
        self.name = name
        self.product_type = product_type
        self.opened_on = opened_on
        self.expiry = expiry

    def __repr__(self):
        return (f"SkinProduct(id={self.id}, name={self.name!r}, "
                f"type={self.product_type!r}, opened_on={self.opened_on}, "
                f"expiry={self.expiry})")


class SkinProductStore:
    def __init__(self):
        self._products = {}

    def add(self, name, product_type, opened_on, expiry):
        product = SkinProduct(name, product_type, opened_on, expiry)
        product.id = self._next_id()
        self._products[product.id] = product
        return product

    def get(self, product_id):
        return self._products.get(product_id)

    def list_all(self):
        return list(self._products.values())

    def _next_id(self):
        return len(self._products) + 1


if __name__ == "__main__":
    store = SkinProductStore()

    product_a = store.add("CeraVe", "cleanser", date(2025, 1, 5), date(2026, 1, 5))
    print(product_a)

    product_b = store.add("La Roche", "toner", date(2025, 2, 1), date(2026, 2, 1))
    print(product_b)

    print("get 1:", store.get(1))
    print("get 99:", store.get(99))

    print("list:")
    for product in store.list_all():
        print(" ", product)
