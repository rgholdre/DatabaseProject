import psycopg2

# Create database
print("Creating database...")
conn = psycopg2.connect(
    host='localhost',
    database='postgres',
    user='postgres',
    password='sohumgodsfury0703',
    port='5432'
)
conn.autocommit = True
cur = conn.cursor()

# Check if database exists
cur.execute("SELECT 1 FROM pg_database WHERE datname = 'DBProject'")
if not cur.fetchone():
    cur.execute('CREATE DATABASE "DBProject"')
    print("Database DBProject created!")
else:
    print("Database DBProject already exists!")

cur.close()
conn.close()

# Now connect to DBProject and create tables
print("\nCreating tables...")
conn = psycopg2.connect(
    host='localhost',
    database='DBProject',
    user='postgres',
    password='sohumgodsfury0703',
    port='5432'
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

