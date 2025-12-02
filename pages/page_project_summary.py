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
    st.markdown(
        "<h2 style='color:#007746; font-weight:700;'>📦 Project Summary</h2>",
        unsafe_allow_html=True,
    )

    today = date.today()
    col1, col2 = st.columns(2)
    year = col1.number_input("Year", value=today.year, step=1)
    month = col2.number_input("Month", value=today.month, min_value=1, max_value=12)

    month_str = f"{int(year)}-{int(month):02d}"

    income, expense = fetch_project_financials(int(year), int(month))
    salary_data = get_project_salary_breakdown(month_str)
    salary_dict = {row["project_code"]: row["total_salary"] for row in salary_data}

    project_codes = sorted(set(list(income.keys()) +
                               list(expense.keys()) +
                               list(salary_dict.keys())))

    table = []
    for p in project_codes:
        inc = income.get(p, 0)
        out = expense.get(p, 0)
        sal = salary_dict.get(p, 0)
        profit = inc - (out + sal)
        table.append([p, inc, out, sal, profit])

    st.markdown(
        "<h4 style='color:#007746; font-weight:600;'>💼 Monthly Project Profit / Loss</h4>",
        unsafe_allow_html=True,
    )

    st.table(
        {
            "Project Code": [r[0] for r in table],
            "Income": [f"{r[1]:,.2f}" for r in table],
            "Expense": [f"{r[2]:,.2f}" for r in table],
            "Salaries": [f"{r[3]:,.2f}" for r in table],
            "Profit": [f"{r[4]:,.2f}" for r in table]
        }
    )

