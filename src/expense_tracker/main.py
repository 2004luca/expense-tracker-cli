import argparse

from src.expense_tracker.expense import Expense
from src.expense_tracker.storage import load_expenses, save_expenses
from src.expense_tracker.reports import summary_by_category, total_amount


def next_id(expenses: list[dict]) -> int:
    if not expenses:
        return 1
    return max(e["id"] for e in expenses) + 1


def cmd_add(args):
    expenses = load_expenses()

    expense = Expense.new(
        expense_id=next_id(expenses),
        amount=args.amount,
        description=args.description,
        category=args.category,
    )

    expenses.append(expense.to_dict())
    save_expenses(expenses)

    print(f"✅ Added: {expense.description} - ${expense.amount:.2f}")


def cmd_list(args):
    expenses = load_expenses()

    if not expenses:
        print("No expenses yet.")
        return

    for e in expenses:
        print(
            f"[{e['id']}] {e['date']} | {e['category']} | "
            f"{e['description']} | ${e['amount']:.2f}"
        )


def cmd_summary(args):
    expenses = load_expenses()

    if not expenses:
        print("No expenses yet.")
        return

    summary = summary_by_category(expenses)
    total = total_amount(expenses)

    print("📊 Summary by category:\n")

    for category, amount in summary.items():
        print(f"{category}: ${amount:.2f}")

    print(f"\nTotal: ${total:.2f}")

def cmd_remove(args):
    expenses = load_expenses()
    before = len(expenses)

    expenses = [e for e in expenses if e["id"] != args.id]

    if len(expenses) == before:
        print("❌ Expense not found.")
        return

    save_expenses(expenses)
    print(f"🗑️ Removed expense id={args.id}")

def build_parser():
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    subparsers = parser.add_subparsers(dest="command")

    # ADD
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("amount", type=float)
    add_parser.add_argument("description")
    add_parser.add_argument("category")
    add_parser.set_defaults(func=cmd_add)

    # LIST
    list_parser = subparsers.add_parser("list")
    list_parser.set_defaults(func=cmd_list)

    # SUMMARY
    summary_parser = subparsers.add_parser("summary")
    summary_parser.set_defaults(func=cmd_summary)



    # REMOVE
    remove_parser = subparsers.add_parser("remove")
    remove_parser.add_argument("id", type=int)
    remove_parser.set_defaults(func=cmd_remove)
    
    return parser




def main():
    parser = build_parser()
    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()


