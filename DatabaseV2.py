# database.py
# Requires: psycopg2 (pip install psycopg2-binary)

import psycopg2

DB_CONFIG = {
    "host": "/tmp",
    "database": "DBProject",
    "user": "HP",      
    "password": "",    
    "port": "5432"
}

def run_sql_file(filename):
    """Execute an entire .sql file (schema or data) against the database."""
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        with conn, conn.cursor() as cur:
            with open(filename, "r") as f:
                sql = f.read()
            cur.execute(sql)
            print(f"✅ Successfully ran {filename}")
    except psycopg2.Error as e:
        print(f"❌ Error while executing {filename}: {e}")
    finally:
        conn.close()

def main():
    # 1️⃣ Build schema (tables, constraints, views, etc.)
    run_sql_file("ERtoRelational.sql")

    # 2️⃣ Populate tables with your INSERT statements
    run_sql_file("Inserts.sql")

if __name__ == "__main__":
    main()
