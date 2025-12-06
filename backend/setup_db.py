import psycopg2
import os
from config import DB_CONFIG

# Create database
print("Creating database...")
try:
    conn = psycopg2.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'] if DB_CONFIG['password'] else None,
        port=DB_CONFIG['port']
    )
    conn.autocommit = True
    cur = conn.cursor()

    # Check if database exists
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_CONFIG['database'],))
    if not cur.fetchone():
        cur.execute('CREATE DATABASE "%s"' % DB_CONFIG['database'])
        print(f"Database {DB_CONFIG['database']} created!")
    else:
        print(f"Database {DB_CONFIG['database']} already exists!")

    cur.close()
    conn.close()
except Exception as e:
    print(f"Error creating database: {e}")
    exit(1)

# Now connect to DBProject and create tables
print("\nCreating tables...")
try:
    conn = psycopg2.connect(
        host=DB_CONFIG['host'],
        database=DB_CONFIG['database'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'] if DB_CONFIG['password'] else None,
        port=DB_CONFIG['port']
    )
    cur = conn.cursor()

    # Read and execute the schema file
    with open('../ERtoRelational.sql', 'r') as f:
        sql = f.read()
        cur.execute(sql)
        conn.commit()
        print("Tables created from ERtoRelational.sql!")

    # Read and execute the inserts file
    with open('../Inserts.sql', 'r') as f:
        sql = f.read()
        cur.execute(sql)
        conn.commit()
        print("Data inserted from Inserts.sql!")

    cur.close()
    conn.close()
    print("\nDatabase setup complete!")
except Exception as e:
    print(f"Error setting up tables: {e}")
    exit(1)

