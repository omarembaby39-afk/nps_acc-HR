import streamlit as st
from datetime import date
from db import get_conn
from acc_logic import get_project_salary_breakdown

def fetch_project_financials(year, month):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT project_code, COALESCE(SUM(amount),0) AS income
        FROM acc_cash_transactions
        WHERE tran_type='IN'
        AND EXTRACT(YEAR FROM tran_date)=%s
        AND EXTRACT(MONTH FROM tran_date)=%s
        GROUP BY project_code;
    """, (year, month))
    income = {r["project_code"]: r["income"] for r in cur.fetchall()}

    cur.execute("""
        SELECT project_code, COALESCE(SUM(amount),0) AS expense
        FROM acc_cash_transactions
        WHERE tran_type='OUT'
        AND EXTRACT(YEAR FROM tran_date)=%s
        AND EXTRACT(MONTH FROM tran_date)=%s
        GROUP BY project_code;
    """, (year, month))
    expense = {r["project_code"]: r["expense"] for r in cur.fetchall()}

    conn.close()
    return income, expense


def page_project_summary():
    st.header("📦 Project Summary")

    today = date.today()
    col1, col2 = st.columns(2)
    year = col1.number_input("Year", value=today.year, step=1)
    month = col2.number_input("Month", value=today.month, min_value=1, max_value=12)

    month_str = f"{int(year)}-{int(month):02d}"

    income, expense = fetch_project_financials(int(year), int(month))
    salary_data = get_project_salary_breakdown(month_str)
    salary_dict = {r["project_code"]: r["total_salary"] for r in salary_data}

    codes = sorted(set(list(income.keys()) + list(expense.keys()) + list(salary_dict.keys())))

    table = []
    for p in codes:
        inc = income.get(p, 0)
        out = expense.get(p, 0)
        sal = salary_dict.get(p, 0)
        prof = inc - (out + sal)
        table.append([p, inc, out, sal, prof])

    st.table({
        "Project": [r[0] for r in table],
        "Income": [f"{r[1]:,.2f}" for r in table],
        "Expense": [f"{r[2]:,.2f}" for r in table],
        "Salaries": [f"{r[3]:,.2f}" for r in table],
        "Profit": [f"{r[4]:,.2f}" for r in table],
    })
