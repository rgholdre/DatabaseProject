# required: psycopg2, Flask, React

import psycopg2 # pip install psycopg2-binary

# SQL query text:
create_student_table = """
CREATE TABLE IF NOT EXISTS students (
    StudentId INT PRIMARY KEY,
    Name VARCHAR(50),
    Email VARCHAR(100),
    Major VARCHAR(50),
    ClassYear VARCHAR(50)
);
"""

create_instructor_table = """
CREATE TABLE IF NOT EXISTS instructor (
    InstructorId INT PRIMARY KEY,
    Name VARCHAR(50),
    Email VARCHAR(100)
);
"""

create_course_table = """
CREATE TABLE IF NOT EXISTS course (
    CourseId INT PRIMARY KEY,
    Title VARCHAR(50),
    Credits INT,
    Level VARCHAR(50),
    Code VARCHAR(50)
);
"""

# currently doesn't follow partial keys; treats sec_no as primary
create_section_table = """
CREATE TABLE IF NOT EXISTS section (
    Sec_no INT PRIMARY KEY,
    Term VARCHAR(50),
    Year INT,
    Session CHAR(1),
    Modality VARCHAR(50),
    Capacity INT
)
"""

create_room_table = """
CREATE TABLE IF NOT EXISTS room (
    RoomId INT PRIMARY KEY,
    Capacity INT, 
    Building VARCHAR(50),
    Room_no INT
)
"""

create_timeSlot_table = """
CREATE TABLE IF NOT EXISTS timeSlot (
    SlotId INT PRIMARY KEY,
    Start_time TIME,
    End_time TIME,
    Days VARCHAR(50)
)
"""

# Relationship tables
create_offered_as_table = """"""

create_teaches_table = """"""
create_enrolled_table = """"""
create_scheduled_at_table = """"""
create_located_at_table = """"""



drop_student_table = "DROP TABLE IF EXISTS students;"
drop_instructor_table = "DROP TABLE IF EXISTS instructor;"
drop_course_table = "DROP TABLE IF EXISTS course;"
drop_section_table = "DROP TABLE IF EXISTS section;"
drop_room_table = "DROP TABLE IF EXISTS room;"
drop_timeSlot_table = "DROP TABLE IF EXISTS timeSlot;"

def runQuery(query):
# Database/user/password/port must be set individually between group
# --> Change to config files for easier swapping between group-members
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="DBProject",
            user="postgres",
            password="Kalefire16",
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