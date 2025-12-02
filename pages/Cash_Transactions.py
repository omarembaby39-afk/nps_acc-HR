import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from datetime import date
from acc_logic import add_cash_transaction
from db import get_conn

def fetch_cash():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM acc_cash_transactions ORDER BY tran_date DESC, id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def page_cash_transactions():
    st.header("💰 Cash In / Out")

    with st.form("cash_form"):
        col1, col2 = st.columns(2)
        d = col1.date_input("Date", value=date.today())
        t = col2.selectbox("Type", ["IN", "OUT"])
        pc = st.text_input("Project Code")
        cat = st.text_input("Category")
        desc = st.text_area("Description")
        amt = st.number_input("Amount", min_value=0.0, step=1.0)

        if st.form_submit_button("Save"):
            add_cash_transaction(d, t, amt, cat, desc, pc)
            st.success("Saved")

    st.subheader("🧾 All Transactions")
    st.dataframe(fetch_cash())
