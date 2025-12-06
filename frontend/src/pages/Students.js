import React, { useState, useEffect } from 'react';
import { studentAPI, enrollmentAPI } from '../api';
import './Students.css';

function Students() {
    const [students, setStudents] = useState([]);
    const [selectedStudent, setSelectedStudent] = useState(null);
    const [enrollments, setEnrollments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [showAddForm, setShowAddForm] = useState(false);
    const [newStudent, setNewStudent] = useState({
        student_id: '', name: '', email: '', major: '', class_year: ''
    });

    useEffect(() => {
        loadStudents();
    }, []);

    const loadStudents = async () => {
        try {
            setLoading(true);
            const data = await studentAPI.getAll();
            setStudents(data);
            setError(null);
        } catch (err) {
            setError('Failed to load students. Make sure the backend is running.');
        } finally {
            setLoading(false);
        }
    };

    const viewEnrollments = async (student) => {
        try {
            setSelectedStudent(student);
            const data = await enrollmentAPI.getByStudent(student.student_id);
            setEnrollments(data);
        } catch (err) {
            setError('Failed to load enrollments.');
        }
    };

    const handleAddStudent = async (e) => {
        e.preventDefault();
        try {
            await studentAPI.create({
                ...newStudent,
                student_id: parseInt(newStudent.student_id)
            });
            setShowAddForm(false);
            setNewStudent({ student_id: '', name: '', email: '', major: '', class_year: '' });
            loadStudents();
        } catch (err) {
            setError('Failed to add student: ' + err.message);
        }
    };

    const formatTime = (time) => {
        if (!time) return 'TBA';
        return time.substring(0, 5);
    };

    if (loading) return <div className="loading">Loading students...</div>;

    return (
        <div className="students-page">
            <div className="page-header">
                <h1>Student Portal</h1>
                <button 
                    className="add-btn"
                    onClick={() => setShowAddForm(!showAddForm)}
                >
                    {showAddForm ? 'Cancel' : '+ Add Student'}
                </button>
            </div>

            {error && <div className="error-message">{error}</div>}

            {showAddForm && (
                <form onSubmit={handleAddStudent} className="add-form">
                    <h3>Add New Student</h3>
                    <div className="form-grid">
                        <input type="number" placeholder="Student ID" required
                            value={newStudent.student_id}
                            onChange={e => setNewStudent({...newStudent, student_id: e.target.value})}
                        />
                        <input type="text" placeholder="Full Name" required
                            value={newStudent.name}
                            onChange={e => setNewStudent({...newStudent, name: e.target.value})}
                        />
                        <input type="email" placeholder="Email" required
                            value={newStudent.email}
                            onChange={e => setNewStudent({...newStudent, email: e.target.value})}
                        />
                        <input type="text" placeholder="Major"
                            value={newStudent.major}
                            onChange={e => setNewStudent({...newStudent, major: e.target.value})}
                        />
                        <select value={newStudent.class_year}
                            onChange={e => setNewStudent({...newStudent, class_year: e.target.value})}
                        >
                            <option value="">Select Year</option>
                            <option value="Freshman">Freshman</option>
                            <option value="Sophomore">Sophomore</option>
                            <option value="Junior">Junior</option>
                            <option value="Senior">Senior</option>
                        </select>
                        <button type="submit" className="submit-btn">Add Student</button>
                    </div>
                </form>
            )}

            <div className="students-container">
                <div className="students-list">
                    <h2>Students</h2>
                    {students.map(student => (
                        <div 
                            key={student.student_id} 
                            className={`student-card ${selectedStudent?.student_id === student.student_id ? 'selected' : ''}`}
                            onClick={() => viewEnrollments(student)}
                        >
                            <div className="student-name">{student.name}</div>
                            <div className="student-info">
                                <span>{student.major || 'Undeclared'}</span>
                                <span>{student.class_year}</span>
                            </div>
                            <div className="student-email">{student.email}</div>
                        </div>
                    ))}
                </div>

                {selectedStudent && (
                    <div className="enrollments-panel">
                        <h2>{selectedStudent.name}'s Enrollments</h2>
                        {enrollments.length === 0 ? (
                            <p className="no-enrollments">No enrollments found.</p>
                        ) : (
                            <div className="enrollment-list">
                                {enrollments.map(e => (
                                    <div key={`${e.course_id}-${e.sec_no}`} className="enrollment-card">
                                        <div className="enrollment-course">
                                            <strong>{e.course_code}</strong> - {e.course_title}
                                        </div>
                                        <div className="enrollment-details">
                                            <span>Section {e.sec_no}</span>
                                            <span>{e.instructor_name}</span>
                                            <span>{e.days} {formatTime(e.start_time)}-{formatTime(e.end_time)}</span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
}

export default Students;

