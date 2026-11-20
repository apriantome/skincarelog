# === Stage 6: Теги ===
# Project: SkinCareLog
import re
from typing import Dict, List, Optional

Tag = str


class Product:
    def __init__(self, name: str, product_type: str, opened: str, expiry: str):
        self.name = name
        self.product_type = product_type
        self.opened = opened
        self.expiry = expiry
        self.tags: List[str] = []

    def add_tag(self, tag: Tag) -> None:
        tag = self._normalize(tag)
        if tag and tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: Tag) -> bool:
        tag = self._normalize(tag)
        if tag in self.tags:
            self.tags.remove(tag)
            return True
        return False

    def has_tag(self, tag: Tag) -> bool:
        return self._normalize(tag) in self.tags

    def search_tags(self, query: str) -> List[str]:
        query = re.sub(r'\s+', ' ', query.strip()).lower()
        if not query:
            return []
        return [t for t in self.tags if query in t.lower()]

    @staticmethod
    def _normalize(tag: Tag) -> str:
        return re.sub(r'\s+', ' ', tag.strip().lower())

    def __str__(self) -> str:
        return f"{self.name} ({self.product_type}) — теги: {', '.join(self.tags) or 'нет'}"


class ProductStore:
    def __init__(self) -> None:
        self._products: Dict[str, Product] = {}

    def get_product(self, name: str) -> Optional[Product]:
        return self._products.get(self._normalize_key(name))

    def add_product(self, product: Product) -> None:
        self._products[self._normalize_key(product.name)] = product

    def _normalize_key(self, name: str) -> str:
        return re.sub(r'\s+', ' ', name.strip().lower())

    def tag_search(self, query: str) -> List[Product]:
        query = re.sub(r'\s+', ' ', query.strip()).lower()
        if not query:
            return []
        return [p for p in self._products.values() if p.has_tag(query)]

    def __len__(self) -> int:
        return len(self._products)
