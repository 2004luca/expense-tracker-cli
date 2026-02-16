# 💸 Expense Tracker
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://expense-tracker-cli.streamlit.app/)

🌍 **Versão online:**  
https://expense-tracker-cli.streamlit.app/

Um projeto em Python para registrar despesas e visualizar resumo por categoria.

O sistema possui duas interfaces:

- 🖥️ CLI (terminal)
- 📊 Web App com Streamlit

---

## 🚀 Funcionalidades

- Adicionar despesa
- Listar despesas
- Remover despesa
- Resumo por categoria
- Total geral
- Persistência em JSON (`data/expenses.json`)

---

## 📦 Instalação

Clone o repositório:

```bash
git clone https://github.com/2004luca/expense-tracker-cli.git
cd expense-tracker-cli
```

Crie e ative o ambiente virtual (Windows PowerShell):

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## 🖥️ Rodar versão CLI

```bash
python -m src.expense_tracker.main add 50 Mercado alimentacao
python -m src.expense_tracker.main list
python -m src.expense_tracker.main summary
```

---

## 📊 Rodar versão Web (Streamlit)

```bash
streamlit run streamlit_app.py
```

Acesse no navegador:

```
http://localhost:8501
```

---

## 🧠 Tecnologias utilizadas

- Python
- Streamlit
- JSON (persistência local)
- Arquitetura modular
- Git & GitHub

---

## 📂 Estrutura do projeto

```
expense-tracker-cli/
│
├── src/expense_tracker/
│   ├── main.py
│   ├── expense.py
│   ├── storage.py
│   └── reports.py
│
├── streamlit_app.py
├── requirements.txt
└── README.md
```

---

