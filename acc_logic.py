from datetime import date
from db import get_conn

def add_cash_transaction(tran_date: date, tran_type: str, amount: float,
                         category: str = None, description: str = None,
                         project_code: str = None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO acc_cash_transactions (
            tran_date, tran_type, amount, category, description, project_code
        ) VALUES (%s, %s, %s, %s, %s, %s)
    """, (tran_date, tran_type, amount, category, description, project_code))
    conn.commit()
    conn.close()


def get_monthly_cash_summary(year: int, month: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            COALESCE(SUM(CASE WHEN tran_type = 'IN' THEN amount ELSE 0 END),0) AS total_in,
            COALESCE(SUM(CASE WHEN tran_type = 'OUT' THEN amount ELSE 0 END),0) AS total_out
        FROM acc_cash_transactions
        WHERE EXTRACT(YEAR FROM tran_date)=%s
        AND EXTRACT(MONTH FROM tran_date)=%s;
    """, (year, month))
    
    row = cur.fetchone()
    conn.close()
    return row["total_in"], row["total_out"], row["total_in"] - row["total_out"]


def get_monthly_salary_total(month_str: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT COALESCE(SUM(net_pay),0) AS total_salary
        FROM payroll_for_accounting
        WHERE month=%s;
    """, (month_str,))
    row = cur.fetchone()
    conn.close()
    return row["total_salary"]


def get_project_salary_breakdown(month_str: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            e.project_code,
            COALESCE(SUM(p.net_pay),0) AS total_salary
        FROM payroll_for_accounting p
        JOIN employees_for_accounting e
            ON e.emp_code = p.worker_code
        WHERE p.month=%s
        GROUP BY e.project_code
        ORDER BY e.project_code;
    """, (month_str,))
    rows = cur.fetchall()
    conn.close()
    return rows

