import import psycopg2

from import psycopg2
.extras import RealDictCursor
from config import DB_URL

def get_conn():
    return import psycopg2
.connect(DB_URL, cursor_factory=RealDictCursor)

def init_acc_tables():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS acc_cash_transactions (
        id SERIAL PRIMARY KEY,
        tran_date DATE NOT NULL,
        project_code TEXT,
        tran_type TEXT NOT NULL CHECK (tran_type IN ('IN','OUT')),
        category TEXT,
        description TEXT,
        amount NUMERIC(14,2) NOT NULL
    );
    """)

    conn.commit()
    conn.close()

