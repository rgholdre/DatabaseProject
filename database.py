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
    PRIMARY KEY (Sec_no, CourseId)
);
"""
create_enrolled_table = """
CREATE TABLE IF NOT EXISTS enrolled(
    Sec_no INT,
    CourseId INT,
    StudentId INT,
    PRIMARY KEY (Sec_no, CourseId, StudentId),
    FOREIGN KEY (StudentId) REFERENCES students(StudentId),
    FOREIGN KEY (Sec_no, CourseId) REFERENCES section(Sec_no, CourseId)
);
"""
create_scheduled_at_table = """
CREATE TABLE IF NOT EXISTS scheduled_at(
    Sec_no INT,
    CourseId INT,
    SlotId INT,
    PRIMARY KEY (Sec_no, CourseId),
    FOREIGN KEY (SlotId) REFERENCES timeSlot(SlotId),
    FOREIGN KEY (Sec_no, CourseId) REFERENCES section(Sec_no, CourseId)
);
"""
create_located_at_table = """
CREATE TABLE IF NOT EXISTS located_at(
    Sec_no INT,
    CourseId INT,
    RoomId INT,
    PRIMARY KEY (Sec_no, CourseId),
    FOREIGN KEY (RoomId) REFERENCES room(RoomId),
    FOREIGN KEY (Sec_no, CourseId) REFERENCES section(Sec_no, CourseId)
);
"""
create_teaches_table = """
CREATE TABLE IF NOT EXISTS teaches(
    Sec_no INT,
    CourseId INT,
    InstructorId INT,
    PRIMARY KEY (Sec_no, CourseId),
    FOREIGN KEY (InstructorId) REFERENCES instructor(InstructorId),
    FOREIGN KEY (Sec_no, CourseId) REFERENCES section(Sec_no, CourseId) ON DELETE CASCADE
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
    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="DBProject",
            port="5432"
        )
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
    except psycopg2.Error as e:
        print(f"Error with connection / query: {e}\nQuery: {query}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

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
    # Use a dedicated connection here for parameterized inserts and per-row handling
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(host="localhost", database="DBProject", port="5432")
        cur = conn.cursor()

        cur.execute("INSERT INTO students(StudentId,Name,Email,Major,ClassYear) VALUES(%s,%s,%s,%s,%s) ON CONFLICT (StudentId) DO NOTHING;",
                    (1, 'John', 'john@asu.edu', 'Computer_Science', 'Junior'))
        cur.execute("INSERT INTO instructor(InstructorId,Name,Email) VALUES(%s,%s,%s) ON CONFLICT (InstructorId) DO NOTHING;",
                    (1, 'Dr.Smith', 'smith@asu.edu'))
        cur.execute("INSERT INTO course(CourseId,Title,Credits,Level,Code) VALUES(%s,%s,%s,%s,%s) ON CONFLICT (CourseId) DO NOTHING;",
                    (1, 'Databases', 3, '4XX', 'CSE412'))

        # Insert csv into Section
        with open('csv/sections.csv','r', newline='', encoding='utf-8') as f:
            # Try both comma and tab delimiters if necessary
            dialect = csv.Sniffer().sniff(f.read(2048))
            f.seek(0)
            reader = csv.DictReader(f, dialect=dialect)
            for row in reader:
                # strip possible surrounding quotes from values
                def clean(v):
                    if v is None:
                        return None
                    s = v.strip()
                    if s.startswith("'") and s.endswith("'"):
                        s = s[1:-1]
                    return s
                try:
                    Sec_no = int(clean(row.get('Sec_no') or row.get('Sec_no\t') or row.get('Sec_no ')))
                    CourseId = int(clean(row.get('CourseId')))
                    Term = clean(row.get('Term'))
                    Year = int(clean(row.get('Year')))
                    Session = clean(row.get('Session'))
                    Modality = clean(row.get('Modality'))
                    Capacity = int(clean(row.get('Capacity')))
                    cur.execute(
                        "INSERT INTO section (Sec_no, CourseId, Term, Year, Session, Modality, Capacity) VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (Sec_no, CourseId) DO NOTHING;",
                        (Sec_no, CourseId, Term, Year, Session, Modality, Capacity)
                    )
                except Exception as e:
                    print("Skipping section row due to error:", e, row)

        # Insert csv into students and enrollments
        with open('csv/students.csv','r', newline='', encoding='utf-8') as f:
            dialect = csv.Sniffer().sniff(f.read(2048))
            f.seek(0)
            reader = csv.DictReader(f, dialect=dialect)
            for row in reader:
                def clean(v):
                    if v is None:
                        return None
                    s = v.strip()
                    if s.startswith("'") and s.endswith("'"):
                        s = s[1:-1]
                    return s
                try:
                    StudentId = int(clean(row.get('StudentId')))
                    Name = clean(row.get('Name'))
                    Email = clean(row.get('Email'))
                    Major = clean(row.get('Major'))
                    ClassYear = clean(row.get('ClassYear'))
                    Sec_no1 = int(clean(row.get('Sec_no1'))) if row.get('Sec_no1') else None
                    CourseId = int(clean(row.get('CourseId'))) if row.get('CourseId') else None

                    cur.execute(
                        "INSERT INTO students (StudentId, Name, Email, Major, ClassYear) VALUES (%s,%s,%s,%s,%s) ON CONFLICT (StudentId) DO NOTHING;",
                        (StudentId, Name, Email, Major, ClassYear)
                    )
                    if Sec_no1 is not None and CourseId is not None:
                        try:
                            cur.execute(
                                "INSERT INTO enrolled (Sec_no, CourseId, StudentId) VALUES (%s,%s,%s) ON CONFLICT (Sec_no, CourseId, StudentId) DO NOTHING;",
                                (Sec_no1, CourseId, StudentId)
                            )
                        except Exception as e:
                            print("Skipping enroll insert due to error:", e, row)
                except Exception as e:
                    print("Skipping student row due to error:", e, row)

        cur.execute("INSERT INTO room(RoomId,Capacity,Building,Room_no) VALUES(%s,%s,%s,%s) ON CONFLICT (RoomId) DO NOTHING;", (12,130,'Wexler',101))
        cur.execute("INSERT INTO timeSlot(SlotId,Start_time,End_time,Days) VALUES(%s,%s,%s,%s) ON CONFLICT (SlotId) DO NOTHING;", (1,'03:00:00','04:00:00','Mon/Wed'))

        conn.commit()
    except psycopg2.Error as e:
        print("Error inserting data:", e)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

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

def exportData():
    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="DBProject",
            port="5432"
        )
        cursor = connection.cursor()

        exports = {
            'students_updated.csv': "SELECT * FROM students;",
            'enrolled_updated.csv': "SELECT * FROM enrolled;",
            'section_updated.csv': "SELECT * FROM section;",
            'course_updated.csv': "SELECT * FROM course;",
            'instructor_updated.csv': "SELECT * FROM instructor;",
            'room_updated.csv': "SELECT * FROM room;",
            'timeslot_updated.csv': "SELECT * FROM timeSlot;"
        }

        for filename, query in exports.items():
            cursor.execute(query)
            rows = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]
            outpath = f"csv/{filename}"
            with open(outpath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(colnames)
                writer.writerows(rows)
            print(f"Exported {len(rows)} rows to {outpath}")

    except psycopg2.Error as e:
        print("Error exporting data:", e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# create/close tables
createTables()
createRelations()
insertData()
exportData()
#closeTables()
