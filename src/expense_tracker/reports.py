from collections import defaultdict


def total_amount(expenses: list[dict]) -> float:
    return sum(float(e["amount"]) for e in expenses)


def summary_by_category(expenses: list[dict]) -> dict[str, float]:
    sums: dict[str, float] = defaultdict(float)
    for e in expenses:
        category = str(e["category"]).strip().lower()
        sums[category] += float(e["amount"])
    return dict(sums)
