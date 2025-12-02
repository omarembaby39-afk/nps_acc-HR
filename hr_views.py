from db import get_conn

def fetch_employees_for_accounting():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees_for_accounting ORDER BY emp_code;")
    rows = cur.fetchall()
    conn.close()
    return rows

def fetch_projects_for_accounting():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM projects_for_accounting ORDER BY project_code;")
    rows = cur.fetchall()
    conn.close()
    return rows

def fetch_payroll_for_month(month_str: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM payroll_for_accounting
        WHERE month = %s
        ORDER BY worker_code;
    """, (month_str,))
    rows = cur.fetchall()
    conn.close()
    return rows

