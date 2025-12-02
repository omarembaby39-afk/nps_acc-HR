import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import streamlit as st
from config import APP_TITLE
from db import init_acc_tables
from pages import (
    Accounting_Dashboard,
    Cash_Transactions,
    Project_Summary,
)

def main():
    st.set_page_config(page_title=APP_TITLE, layout="wide")

    init_acc_tables()

    st.sidebar.markdown(
        "<h2 style='color:#007746;'>NPS Accounting</h2>",
        unsafe_allow_html=True,
    )

    page = st.sidebar.radio(
        "",
        ["Dashboard", "Cash In/Out", "Project Summary"]
    )

    if page == "Dashboard":
        Accounting_Dashboard.page_accounting_dashboard()
    elif page == "Cash In/Out":
        Cash_Transactions.page_cash_transactions()
    elif page == "Project Summary":
        Project_Summary.page_project_summary()

if __name__ == "__main__":
    main()

