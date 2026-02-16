import streamlit as st

from src.expense_tracker.expense import Expense
from src.expense_tracker.storage import load_expenses, save_expenses
from src.expense_tracker.reports import summary_by_category, total_amount


def next_id(expenses: list[dict]) -> int:
    if not expenses:
        return 1
    return max(e["id"] for e in expenses) + 1


st.set_page_config(page_title="Expense Tracker", page_icon="💸", layout="wide")

st.title("💸 Expense Tracker (Streamlit)")
st.caption("Registre despesas e veja resumo por categoria. Dados salvos em data/expenses.json")

# Carrega dados
expenses = load_expenses()

# ---------- SIDEBAR (Adicionar) ----------
st.sidebar.header("➕ Adicionar despesa")

amount = st.sidebar.number_input("Valor", min_value=0.0, step=0.01, format="%.2f")
description = st.sidebar.text_input("Descrição", placeholder="ex: Mercado")
category = st.sidebar.text_input("Categoria", placeholder="ex: alimentacao")

if st.sidebar.button("Adicionar", use_container_width=True):
    if not description.strip() or not category.strip():
        st.sidebar.error("Descrição e categoria são obrigatórias.")
    else:
        exp = Expense.new(
            expense_id=next_id(expenses),
            amount=float(amount),
            description=description.strip(),
            category=category.strip(),
        )
        expenses.append(exp.to_dict())
        save_expenses(expenses)
        st.sidebar.success(f"Adicionado: #{exp.id} {exp.description} (${exp.amount:.2f})")
        st.rerun()

# ---------- Layout principal ----------
col1, col2 = st.columns([1, 2], gap="large")

# ===== RESUMO =====
with col1:
    st.subheader("📊 Resumo")

    if expenses:
        summary = summary_by_category(expenses)
        total = total_amount(expenses)

        rows = [{"Categoria": k, "Total": v} for k, v in summary.items()]
        st.dataframe(rows, use_container_width=True, hide_index=True)

        st.metric("Total geral", f"${total:.2f}")
    else:
        st.info("Sem despesas ainda.")

# ===== TABELA DE DESPESAS =====
with col2:
    st.subheader("🧾 Despesas")

    if not expenses:
        st.info("Nenhuma despesa cadastrada.")
    else:
        expenses_sorted = sorted(expenses, key=lambda e: e["id"], reverse=True)
        st.dataframe(expenses_sorted, use_container_width=True, hide_index=True)

        st.divider()
        st.subheader("🗑️ Remover despesa")

        remove_id = st.number_input("ID para remover", min_value=1, step=1)

        if st.button("Remover", type="primary"):
            before = len(expenses)
            updated = [e for e in expenses if e["id"] != int(remove_id)]

            if len(updated) == before:
                st.error("ID não encontrado.")
            else:
                save_expenses(updated)
                st.success(f"Removido ID {int(remove_id)}")
                st.rerun()
