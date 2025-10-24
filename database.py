# required: psycopg2, Flask, React

import psycopg2 # pip install psycopg2-binary
import csv

# SQL query text:

# Create tables query text
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
    Sec_no INT,
    CourseId INT,
    Term VARCHAR(50),
    Year INT,
    Session CHAR(1),
    Modality VARCHAR(50),
    Capacity INT,
    PRIMARY KEY (Sec_no, CourseId),
    FOREIGN KEY (CourseId) REFERENCES course(CourseId) ON DELETE CASCADE
);
"""

create_room_table = """
CREATE TABLE IF NOT EXISTS room (
    RoomId INT PRIMARY KEY,
    Capacity INT, 
    Building VARCHAR(50),
    Room_no INT
);
"""

create_timeSlot_table = """
CREATE TABLE IF NOT EXISTS timeSlot (
    SlotId INT PRIMARY KEY,
    Start_time TIME,
    End_time TIME,
    Days VARCHAR(50)
);
"""

# Relationship tables
create_offered_as_table = """
CREATE TABLE IF NOT EXISTS offered_as(
    Sec_no INT,
    CourseId INT,
    Term VARCHAR(50),
    Year INT,
    Session CHAR(1),
    Modality VARCHAR(50),
    Capacity INT,
    PRIMARY KEY (Sec_no, CourseId),
    FOREIGN KEY (Sec_no) REFERENCES course ON DELETE CASCADE
);
"""
create_enrolled_table = """
CREATE TABLE IF NOT EXISTS enrolled(
    Sec_no INT,
    CourseId INT,
    StudentId INT,
    PRIMARY KEY (Sec_no, CourseId, StudentId),
    FOREIGN KEY (StudentId) REFERENCES students,
    FOREIGN KEY (Sec_no, CourseId) REFERENCES section   
);
"""
create_scheduled_at_table = """
CREATE TABLE IF NOT EXISTS scheduled_at(
    Sec_no INT,
    CourseId INT,
    SlotId INT,
    PRIMARY KEY (Sec_no, CourseId),
    FOREIGN KEY (SlotId) REFERENCES timeSlot,
    FOREIGN KEY (Sec_no, CourseId) REFERENCES section
);
"""
create_located_at_table = """
CREATE TABLE IF NOT EXISTS located_at(
    Sec_no INT,
    CourseId INT,
    RoomId INT,
    PRIMARY KEY (Sec_no, CourseId),
    FOREIGN KEY (RoomId) REFERENCES room,
    FOREIGN KEY (Sec_no, CourseId) REFERENCES section
);
"""
create_teaches_table = """
CREATE TABLE IF NOT EXISTS teaches(
    Sec_no INT,
    CourseId INT,
    InstructorId INT,
    PRIMARY KEY (Sec_no, CourseId),
    FOREIGN KEY (InstructorId) REFERENCES instructor,
    FOREIGN KEY (Sec_no, CourseId) REFERENCES section ON DELETE CASCADE
);
"""

# Drop table queries for testing
drop_student_table = "DROP TABLE IF EXISTS students CASCADE;"
drop_instructor_table = "DROP TABLE IF EXISTS instructor CASCADE;"
drop_course_table = "DROP TABLE IF EXISTS course CASCADE;"
drop_section_table = "DROP TABLE IF EXISTS section CASCADE;"
drop_room_table = "DROP TABLE IF EXISTS room CASCADE;"
drop_timeSlot_table = "DROP TABLE IF EXISTS timeSlot CASCADE;"
drop_offered_as_table = "DROP TABLE IF EXISTS offered_as CASCADE;"
drop_teaches_table = "DROP TABLE IF EXISTS teaches CASCADE;"
drop_enrolled_table = "DROP TABLE IF EXISTS enrolled CASCADE;"
drop_located_at_table = "DROP TABLE IF EXISTS located_at CASCADE;"
drop_scheduled_at_table = "DROP TABLE IF EXISTS scheduled_at CASCADE;"

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
        print(f"Query {query} successfully run")

    except psycopg2.Error as e:
        print(f"Error with connection: {e}")

    finally:
        cursor.close()
        connection.close()
        print("Database connection closed.")


def createTables():
    runQuery(create_course_table)
    runQuery(create_section_table)
    runQuery(create_instructor_table)
    runQuery(create_student_table)
    runQuery(create_timeSlot_table)
    runQuery(create_room_table)

def createRelations():
    runQuery(create_scheduled_at_table)
    runQuery(create_located_at_table)
    runQuery(create_teaches_table)
    runQuery(create_enrolled_table)
    runQuery(create_offered_as_table)

def insertData():
    runQuery("INSERT INTO students(StudentId,Name,Email,Major,ClassYear) VALUES(1,'John','john@asu.edu','Computer_Science','Junior');")
    runQuery("INSERT INTO instructor(InstructorId,Name,Email) VALUES(1,'Dr.Smith','smith@asu.edu');")
    runQuery("INSERT INTO course(CourseId,Title,Credits,Level,Code) VALUES(1,'Databases',3,'4XX','CSE412');")

    #Insert csv into Section
    with open('csv/sections.csv','r') as f:
        read = csv.DictReader(f)
        for row in read:
            runQuery(f"INSERT INTO section(Sec_no,CourseId,Term,Year,Session,Modality,Capacity) VALUES({row['Sec_no']},{row['CourseId']},{row['Term']},{row['Year']},{row['Session']},{row['Modality']},{row['Capacity']});")

    #Insert csv into student
    with open('csv/students.csv','r') as f:
        read = csv.DictReader(f)
        for row in read:
            runQuery(f"INSERT INTO students(StudentId,Name,Email,Major,ClassYear) VALUES({row['StudentId']},{row['Name']},{row['Email']},{row['Major']},{row['ClassYear']});")
            #Test for inserting into enrolled (relation table based on student information)
            runQuery(f"INSERT INTO enrolled(Sec_no,CourseId,StudentId) VALUES({row['Sec_no1']},{row['CourseId']},{row['StudentId']});")

    runQuery("INSERT INTO room(RoomId,Capacity,Building,Room_no) VALUES(12,130,'Wexler',101);")
    runQuery("INSERT INTO timeSlot(SlotId,Start_time,End_time,Days) VALUES(1,'3:00:00','4:00:00',13)")

def closeTables():
    runQuery(drop_course_table)
    runQuery(drop_instructor_table)
    runQuery(drop_room_table)
    runQuery(drop_section_table)
    runQuery(drop_student_table)
    runQuery(drop_timeSlot_table)
    runQuery(drop_offered_as_table)
    runQuery(drop_teaches_table)
    runQuery(drop_enrolled_table)
    runQuery(drop_located_at_table)
    runQuery(drop_scheduled_at_table)

# create/close tables
createTables()
createRelations()
insertData()
#closeTables()