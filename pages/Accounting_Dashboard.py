import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from datetime import date
from acc_logic import (
    get_monthly_cash_summary,
    get_monthly_salary_total
)

st.markdown("""
<style>
.metric-container {
    background-color: #e6f4ea;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #bcd9c8;
}
h2, h3, h4 { color: #007746 !important; }
</style>
""", unsafe_allow_html=True)

def page_accounting_dashboard():
    st.header("📊 NPS Accounting Dashboard")

    today = date.today()
    col1, col2 = st.columns(2)
    year = col1.number_input("Year", value=today.year, step=1)
    month = col2.number_input("Month", value=today.month, min_value=1, max_value=12)

    month_str = f"{int(year)}-{int(month):02d}"

    total_in, total_out, balance = get_monthly_cash_summary(int(year), int(month))
    total_salary = get_monthly_salary_total(month_str)

    c1, c2, c3, c4 = st.columns(4)
    items = [
        (c1, "Total Income", total_in),
        (c2, "Total Outcome", total_out),
        (c3, "Balance", balance),
        (c4, "Total Salaries", total_salary)
    ]

    for col, title, value in items:
        with col:
            st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
            st.metric(title, f"{value:,.2f}")
            st.markdown("</div>", unsafe_allow_html=True)
