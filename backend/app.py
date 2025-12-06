# Flask Backend API for University Course Management System
from flask import Flask, jsonify, request
from flask.json.provider import DefaultJSONProvider
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import date, time, datetime
from config import DB_CONFIG

# Custom JSON provider to handle datetime objects
class CustomJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        if isinstance(obj, time):
            return obj.strftime('%H:%M:%S')
        return super().default(obj)

app = Flask(__name__)
app.json_provider_class = CustomJSONProvider
app.json = CustomJSONProvider(app)
CORS(app)  # Enable CORS for React frontend

def get_db_connection():
    """Create and return a database connection."""
    conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
    return conn

# ==================== COURSE ROUTES ====================
@app.route('/api/courses', methods=['GET'])
def get_courses():
    """Get all courses."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM course ORDER BY courseid')
        courses = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(courses)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/courses/<int:courseid>', methods=['GET'])
def get_course(courseid):
    """Get a specific course by ID."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM course WHERE courseid = %s', (courseid,))
        course = cur.fetchone()
        cur.close()
        conn.close()
        if course:
            return jsonify(course)
        return jsonify({'error': 'Course not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== STUDENT ROUTES ====================
@app.route('/api/students', methods=['GET'])
def get_students():
    """Get all students."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM students ORDER BY studentid')
        students = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(students)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/students/<int:studentid>', methods=['GET'])
def get_student(studentid):
    """Get a specific student by ID."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM students WHERE studentid = %s', (studentid,))
        student = cur.fetchone()
        cur.close()
        conn.close()
        if student:
            return jsonify(student)
        return jsonify({'error': 'Student not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/students', methods=['POST'])
def create_student():
    """Create a new student."""
    try:
        data = request.get_json()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            '''INSERT INTO students (studentid, name, email, major, classyear) 
               VALUES (%s, %s, %s, %s, %s) RETURNING *''',
            (data['studentid'], data['name'], data['email'], 
             data.get('major'), data.get('classyear'))
        )
        student = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(student), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/students', methods=['POST'])
def update_student(studentid):
    """Update a student."""
    try:
        data = request.get_json()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            '''UPDATE students SET studentid = %s, name = %s,
                    email = %s, major = %s, classyear = %s) WHERE name = %s''',
            (data['studentid'], data['name'], data['email'], 
             data.get('major'), data.get('classyear'), data['name'])
        )
        student = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(student), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== INSTRUCTOR ROUTES ====================
@app.route('/api/instructors', methods=['GET'])
def get_instructors():
    """Get all instructors."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM instructor ORDER BY instructorid')
        instructors = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(instructors)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/instructors/<int:instructorid>', methods=['GET'])
def get_instructor(instructorid):
    """Get a specific instructor by ID."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM instructor WHERE instructorid = %s', (instructorid,))
        instructor = cur.fetchone()
        cur.close()
        conn.close()
        if instructor:
            return jsonify(instructor)
        return jsonify({'error': 'Instructor not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== SECTION ROUTES ====================
@app.route('/api/sections', methods=['GET'])
def get_sections():
    """Get all sections with course and instructor details."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            SELECT s.sec_no, s.courseid as course_id, s.term, s.year, s.session, s.modality, s.capacity,
                   c.title as course_title, c.code as course_code,
                   i.name as instructor_name, t.days, t.start_time, t.end_time,
                   r.room_no, r.building
            FROM section s
            JOIN course c ON s.courseid = c.courseid
            JOIN teaches te ON s.sec_no = te.sec_no AND s.courseid = te.courseid
            JOIN instructor i ON te.instructorid = i.instructorid
            JOIN scheduled_at sa ON s.sec_no = sa.sec_no AND s.courseid = sa.courseid
            JOIN timeslot t ON sa.slotid = t.slotid
            LEFT JOIN located_at la ON s.sec_no = la.sec_no AND s.courseid = la.courseid
            LEFT JOIN room r ON la.roomid = r.roomid
            ORDER BY c.code, s.sec_no
        ''')
        sections = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(sections)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sections/<int:courseid>/<int:sec_no>', methods=['GET'])
def get_section(courseid, sec_no):
    """Get a specific section."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            SELECT s.*, c.title as course_title, c.code as course_code,
                   i.name as instructor_name, t.days, t.start_time, t.end_time,
                   r.room_no, r.building,
                   s.capacity - COALESCE(COUNT(e.studentid), 0) as seats_available
            FROM section s
            JOIN course c ON s.courseid = c.courseid
            JOIN teaches te ON s.sec_no = te.sec_no AND s.courseid = te.courseid
            JOIN instructor i ON te.instructorid = i.instructorid
            JOIN scheduled_at sa ON s.sec_no = sa.sec_no AND s.courseid = sa.courseid
            JOIN timeslot t ON sa.slotid = t.slotid
            LEFT JOIN located_at la ON s.sec_no = la.sec_no AND s.courseid = la.courseid
            LEFT JOIN room r ON la.roomid = r.roomid
            LEFT JOIN enrolled e ON s.courseid = e.courseid AND s.sec_no = e.sec_no
            WHERE s.courseid = %s AND s.sec_no = %s
            GROUP BY s.courseid, s.sec_no, c.title, c.code, i.name,
                     t.days, t.start_time, t.end_time, r.room_no, r.building
        ''', (courseid, sec_no))
        section = cur.fetchone()
        cur.close()
        conn.close()
        if section:
            return jsonify(section)
        return jsonify({'error': 'Section not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== ENROLLMENT ROUTES ====================
@app.route('/api/enrollments', methods=['GET'])
def get_enrollments():
    """Get all enrollments with details."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            SELECT e.*, st.name as student_name, c.title as course_title,
                   c.code as course_code, se.term, se.year
            FROM enrolled e
            JOIN students st ON e.studentid = st.studentid
            JOIN section se ON e.courseid = se.courseid AND e.sec_no = se.sec_no
            JOIN course c ON se.courseid = c.courseid
            ORDER BY st.name, c.code
        ''')
        enrollments = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(enrollments)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/enrollments/student/<int:studentid>', methods=['GET'])
def get_student_enrollments(studentid):
    """Get all enrollments for a specific student."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            SELECT e.studentid as student_id, e.courseid as course_id, e.sec_no,
                   c.title as course_title, c.code as course_code,
                   se.term, se.year, se.modality, i.name as instructor_name, i.email as instructor_email,
                   t.days, t.start_time, t.end_time, r.room_no, r.building
            FROM enrolled e
            JOIN section se ON e.courseid = se.courseid AND e.sec_no = se.sec_no
            JOIN course c ON se.courseid = c.courseid
            JOIN teaches te ON se.sec_no = te.sec_no AND se.courseid = te.courseid
            JOIN instructor i ON te.instructorid = i.instructorid
            JOIN scheduled_at sa ON se.sec_no = sa.sec_no AND se.courseid = sa.courseid
            JOIN timeslot t ON sa.slotid = t.slotid
            LEFT JOIN located_at la ON se.sec_no = la.sec_no AND se.courseid = la.courseid
            LEFT JOIN room r ON la.roomid = r.roomid
            WHERE e.studentid = %s
            ORDER BY c.code
        ''', (studentid,))
        enrollments = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(enrollments)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/enrollments', methods=['POST'])
def create_enrollment():
    """Enroll a student in a section."""
    try:
        data = request.get_json()
        conn = get_db_connection()
        cur = conn.cursor()

        # Support both naming conventions from frontend
        studentid = data.get('studentid') or data.get('student_id')
        courseid = data.get('courseid') or data.get('course_id')
        sec_no = data.get('sec_no')

        # Check if section has available seats - COALESCE(COUNT(e.studentid), 0) as seats
        cur.execute('''
            SELECT s.capacity as seats
            FROM section s
            LEFT JOIN enrolled e ON s.courseid = e.courseid AND s.sec_no = e.sec_no
            WHERE s.courseid = %s AND s.sec_no = %s
            GROUP BY s.capacity
        ''', (courseid, sec_no))
        result = cur.fetchone()

        if not result or result['seats'] <= 0:
            return jsonify({'error': 'No seats available'}), 400

        cur.execute(
            '''INSERT INTO enrolled (studentid, courseid, sec_no)
               VALUES (%s, %s, %s) RETURNING *''',
            (studentid, courseid, sec_no)
        )

        enrollment = cur.fetchone()
        conn.commit()

        capacity = int(result['seats']) - 1

        cur.execute(
            '''UPDATE section SET capacity = %s WHERE sec_no = %s''',
            (capacity , sec_no)
        )
        conn.commit()

        cur.close()
        conn.close()
        return jsonify(enrollment), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/enrollments/<int:studentid>/<int:courseid>/<int:sec_no>', methods=['DELETE'])
def delete_enrollment(studentid, courseid, sec_no):
    """Remove a student from a section."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            '''DELETE FROM enrolled
               WHERE studentid = %s AND courseid = %s AND sec_no = %s
               RETURNING *''',
            (studentid, courseid, sec_no)
        )
        deleted = cur.fetchone()

        cur.execute('''
            SELECT s.capacity as seats
            FROM section s
            LEFT JOIN enrolled e ON s.courseid = e.courseid AND s.sec_no = e.sec_no
            WHERE s.courseid = %s AND s.sec_no = %s
            GROUP BY s.capacity
        ''', (courseid, sec_no))
        result = cur.fetchone()
        capacity = int(result['seats']) + 1

        conn.commit()

        cur.execute(
            '''UPDATE section SET capacity = %s WHERE sec_no = %s''',
            (capacity, sec_no)
      )
        conn.commit()
        cur.close()
        conn.close()
        if deleted:
            return jsonify({'message': 'Enrollment deleted successfully'})
        return jsonify({'error': 'Enrollment not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== SEARCH ROUTES ====================
@app.route('/api/search/courses', methods=['GET'])
def search_courses():
    """Search courses by title, code, or level."""
    try:
        query = request.args.get('q', '')
        term = request.args.get('term', '')
        year = request.args.get('year', '')

        conn = get_db_connection()
        cur = conn.cursor()

        sql = '''
            SELECT DISTINCT c.*,
                   (SELECT COUNT(*) FROM section s WHERE s.courseid = c.courseid) as section_count
            FROM course c
            LEFT JOIN section s ON c.courseid = s.courseid
            WHERE (c.title ILIKE %s OR c.code ILIKE %s)
        '''
        params = [f'%{query}%', f'%{query}%']

        if term:
            sql += ' AND s.term = %s'
            params.append(term)
        if year:
            sql += ' AND s.year = %s'
            params.append(int(year))

        sql += ' ORDER BY c.code'

        cur.execute(sql, params)
        courses = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(courses)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

