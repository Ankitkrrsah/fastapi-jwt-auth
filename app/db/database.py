import psycopg2
from app.config.config import settings

def get_db():
    conn = psycopg2.connect(settings.DATABASE_URL)
    cur = conn.cursor()
    try:
        yield cur, conn
    finally:
        cur.close()
        conn.close()
