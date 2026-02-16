import json
from pathlib import Path

DEFAULT_PATH = Path("data/expenses.json")


def load_expenses(path: Path = DEFAULT_PATH) -> list[dict]:
    """Carrega despesas do JSON. Se não existir ainda, retorna lista vazia."""
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_expenses(expenses: list[dict], path: Path = DEFAULT_PATH) -> None:
    """Salva despesas no JSON (bonitinho com indent)."""
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as f:
        json.dump(expenses, f, ensure_ascii=False, indent=2)
