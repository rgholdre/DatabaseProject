# Flask Backend API for University Course Management System
from flask import Flask, jsonify, request
from flask.json.provider import DefaultJSONProvider
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import date, time, datetime

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

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "database": "DBProject",
    "user": "postgres",
    "password": "sohumgodsfury0703",
    "port": "5432"
}

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
        cur.execute('SELECT * FROM course ORDER BY course_id')
        courses = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(courses)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    """Get a specific course by ID."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM course WHERE course_id = %s', (course_id,))
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
        cur.execute('SELECT * FROM student ORDER BY student_id')
        students = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(students)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    """Get a specific student by ID."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM student WHERE student_id = %s', (student_id,))
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
            '''INSERT INTO student (student_id, name, email, major, class_year) 
               VALUES (%s, %s, %s, %s, %s) RETURNING *''',
            (data['student_id'], data['name'], data['email'], 
             data.get('major'), data.get('class_year'))
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
        cur.execute('SELECT * FROM instructor ORDER BY instructor_id')
        instructors = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(instructors)
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
            SELECT s.*, c.title as course_title, c.code as course_code,
                   i.name as instructor_name, t.days, t.start_time, t.end_time,
                   r.room_no, r.building
            FROM section s
            JOIN course c ON s.course_id = c.course_id
            JOIN instructor i ON s.instructor_id = i.instructor_id
            JOIN timeslot t ON s.slot_id = t.slot_id
            LEFT JOIN room r ON s.room_id = r.room_id
            ORDER BY c.code, s.sec_no
        ''')
        sections = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(sections)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sections/<int:course_id>/<int:sec_no>', methods=['GET'])
def get_section(course_id, sec_no):
    """Get a specific section."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            SELECT s.*, c.title as course_title, c.code as course_code,
                   i.name as instructor_name, t.days, t.start_time, t.end_time,
                   r.room_no, r.building,
                   s.capacity - COALESCE(COUNT(e.student_id), 0) as seats_available
            FROM section s
            JOIN course c ON s.course_id = c.course_id
            JOIN instructor i ON s.instructor_id = i.instructor_id
            JOIN timeslot t ON s.slot_id = t.slot_id
            LEFT JOIN room r ON s.room_id = r.room_id
            LEFT JOIN enrolled e ON s.course_id = e.course_id AND s.sec_no = e.sec_no
            WHERE s.course_id = %s AND s.sec_no = %s
            GROUP BY s.course_id, s.sec_no, c.title, c.code, i.name,
                     t.days, t.start_time, t.end_time, r.room_no, r.building
        ''', (course_id, sec_no))
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
            JOIN student st ON e.student_id = st.student_id
            JOIN section se ON e.course_id = se.course_id AND e.sec_no = se.sec_no
            JOIN course c ON se.course_id = c.course_id
            ORDER BY st.name, c.code
        ''')
        enrollments = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(enrollments)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/enrollments/student/<int:student_id>', methods=['GET'])
def get_student_enrollments(student_id):
    """Get all enrollments for a specific student."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            SELECT e.*, c.title as course_title, c.code as course_code,
                   se.term, se.year, se.modality, i.name as instructor_name,
                   t.days, t.start_time, t.end_time, r.room_no, r.building
            FROM enrolled e
            JOIN section se ON e.course_id = se.course_id AND e.sec_no = se.sec_no
            JOIN course c ON se.course_id = c.course_id
            JOIN instructor i ON se.instructor_id = i.instructor_id
            JOIN timeslot t ON se.slot_id = t.slot_id
            LEFT JOIN room r ON se.room_id = r.room_id
            WHERE e.student_id = %s
            ORDER BY c.code
        ''', (student_id,))
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

        # Check if section has available seats
        cur.execute('''
            SELECT s.capacity - COALESCE(COUNT(e.student_id), 0) as seats
            FROM section s
            LEFT JOIN enrolled e ON s.course_id = e.course_id AND s.sec_no = e.sec_no
            WHERE s.course_id = %s AND s.sec_no = %s
            GROUP BY s.capacity
        ''', (data['course_id'], data['sec_no']))
        result = cur.fetchone()

        if not result or result['seats'] <= 0:
            return jsonify({'error': 'No seats available'}), 400

        cur.execute(
            '''INSERT INTO enrolled (student_id, course_id, sec_no)
               VALUES (%s, %s, %s) RETURNING *''',
            (data['student_id'], data['course_id'], data['sec_no'])
        )
        enrollment = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(enrollment), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/enrollments/<int:student_id>/<int:course_id>/<int:sec_no>', methods=['DELETE'])
def delete_enrollment(student_id, course_id, sec_no):
    """Remove a student from a section."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            '''DELETE FROM enrolled
               WHERE student_id = %s AND course_id = %s AND sec_no = %s
               RETURNING *''',
            (student_id, course_id, sec_no)
        )
        deleted = cur.fetchone()
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
                   (SELECT COUNT(*) FROM section s WHERE s.course_id = c.course_id) as section_count
            FROM course c
            LEFT JOIN section s ON c.course_id = s.course_id
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

