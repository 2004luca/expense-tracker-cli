import streamlit as st
from datetime import date

from src.expense_tracker.reports import summary_by_category, total_amount
from src.expense_tracker.database import (
    init_db,
    get_or_create_user,
    add_expense_db,
    list_expenses_db,
    remove_expense_db,
)

# Configuração da página
st.set_page_config(page_title="Expense Tracker", page_icon="💸", layout="wide")

# Inicializa banco
init_db()

st.title("💸 Expense Tracker (SQLite)")
st.caption("Cada usuário possui suas próprias despesas.")

# ---------- SIDEBAR (Usuário) ----------
st.sidebar.header("👤 Usuário")
username = st.sidebar.text_input("Digite seu nome de usuário")

if not username:
    st.warning("Digite um nome de usuário para começar.")
    st.stop()

user_id = get_or_create_user(username)

# Carrega despesas do banco
expenses = list_expenses_db(user_id)

# ---------- SIDEBAR (Adicionar) ----------
st.sidebar.header("➕ Adicionar despesa")

amount = st.sidebar.number_input("Valor", min_value=0.0, step=0.01, format="%.2f")
description = st.sidebar.text_input("Descrição", placeholder="ex: Mercado")
category = st.sidebar.text_input("Categoria", placeholder="ex: alimentacao")

if st.sidebar.button("Adicionar", use_container_width=True):
    if not description.strip() or not category.strip():
        st.sidebar.error("Descrição e categoria são obrigatórias.")
    else:
        add_expense_db(
            user_id=user_id,
            amount=float(amount),
            description=description.strip(),
            category=category.strip(),
            date_str=date.today().isoformat(),
        )
        st.sidebar.success("Despesa adicionada.")
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
        st.dataframe(expenses, use_container_width=True, hide_index=True)

        st.divider()


        st.subheader("🗑️ Remover despesa")

# Criar lista formatada para o selectbox
        options = [
            f"{e['id']} - {e['description']} (${e['amount']:.2f})"
            for e in expenses
        ]

        if options:
            selected = st.selectbox("Selecione a despesa", options)

            if st.button("Remover", type="primary"):
        # Extrai o ID da string (antes do primeiro espaço)
                expense_id = int(selected.split(" - ")[0])

                removed = remove_expense_db(user_id, expense_id)

                if removed:
                    st.success("Despesa removida.")
                else:
                    st.error("Erro ao remover.")

                st.rerun()
        else:
            st.info("Nenhuma despesa para remover.")
