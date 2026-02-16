from dataclasses import dataclass, asdict
from datetime import date


@dataclass
class Expense:
    id: int
    amount: float
    description: str
    category: str
    date: str  # formato: YYYY-MM-DD

    @staticmethod
    def new(expense_id: int, amount: float, description: str, category: str) -> "Expense":
        return Expense(
            id=expense_id,
            amount=amount,
            description=description,
            category=category,
            date=date.today().isoformat(),
        )

    def to_dict(self) -> dict:
        return asdict(self)
