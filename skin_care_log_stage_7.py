# === Stage 7: Группировка ===
# Project: SkinCareLog
from collections import defaultdict


def group_by_type(supplies):
    grouped = defaultdict(list)
    for supply in supplies:
        grouped[supply["type"]].append(supply)
    return grouped


def count_by_type(supplies):
    counts = defaultdict(int)
    for supply in supplies:
        counts[supply["type"]] += 1
    return dict(sorted(counts.items()))


def summarize_types(supplies):
    groups = group_by_type(supplies)
    summary = {}
    for type_name, items in groups.items():
        summary[type_name] = {
            "count": len(items),
            "items": [item["name"] for item in items],
        }
    return summary


if __name__ == "__main__":
    sample = [
        {"name": "Увлажняющий крем", "type": "Уход", "opened": "2025-01-01", "expiry": "2026-01-01"},
        {"name": "Сыворотка с витамином С", "type": "Сыворотка", "opened": "2025-02-15", "expiry": "2025-08-15"},
        {"name": "Увлажняющий лосьон", "type": "Уход", "opened": "2025-03-10", "expiry": "2026-03-10"},
        {"name": "Тоник", "type": "Тоник", "opened": "2025-04-01", "expiry": "2025-10-01"},
        {"name": "Пенка для умывания", "type": "Уход", "opened": "2025-05-20", "expiry": "2026-05-20"},
    ]

    result = summarize_types(sample)
    for type_name, data in result.items():
        print(f"{type_name}: {data['count']} шт — {', '.join(data['items'])}")
