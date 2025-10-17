# required: psycopg2, tkinter

import psycopg2 # pip install psycopg2-binary

# SQL query text:
create_test_table = """
CREATE TABLE IF NOT EXISTS students (
    StudentId INT PRIMARY KEY,
    Name VARCHAR(50),
    Email VARCHAR(100),
    Major VARCHAR(50),
    ClassYear INT
);
"""

drop_test_table = "DROP TABLE IF EXISTS students;"

def runQuery(query):
# Database/user/password/port must be set individually between group
# --> Change to config files for easier swapping between group-members
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="DBProject",
            user="",
            password="",
            port="5432"
        )
        cursor = connection.cursor()
        print("Database connection started.")
        
        #Run query
        cursor.execute(query)
        connection.commit()
        print("Query successfully run")

    except psycopg2.Error as e:
        print(f"Error with connection: {e}")

    finally:
        cursor.close()
        connection.close()
        print("Database connection closed.")