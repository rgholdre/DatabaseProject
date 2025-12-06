import React, { useState, useEffect } from 'react';
import { useStudent } from '../context/StudentContext';
import { enrollmentAPI } from '../api';
import './MyEnrollments.css';

function MyEnrollments() {
    const { student } = useStudent();
    const [enrollments, setEnrollments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [message, setMessage] = useState({ text: '', type: '' });

    useEffect(() => {
        if (student) {
            loadEnrollments();
        }
    }, [student]);

    const loadEnrollments = async () => {
        try {
            setLoading(true);
            const data = await enrollmentAPI.getByStudent(student.studentid || student.student_id);
            setEnrollments(data);
        } catch (err) {
            setMessage({ text: 'Failed to load enrollments', type: 'error' });
        } finally {
            setLoading(false);
        }
    };

    const handleDrop = async (courseId, secNo, courseName) => {
        if (window.confirm(`Are you sure you want to drop ${courseName}?`)) {
            try {
                await enrollmentAPI.delete(student.studentid || student.student_id, courseId, secNo);
                setMessage({ text: `Successfully dropped ${courseName}`, type: 'success' });
                loadEnrollments();
                setTimeout(() => setMessage({ text: '', type: '' }), 3000);
            } catch (err) {
                setMessage({ text: 'Failed to drop course', type: 'error' });
            }
        }
    };

    const formatTime = (time) => time ? time.substring(0, 5) : 'TBA';

    const totalCredits = enrollments.reduce((sum, e) => sum + (e.credits || 3), 0);

    return (
        <div className="my-enrollments-page">
            <header className="enrollments-header">
                <div className="header-content">
                    <h1>My Enrollments</h1>
                    <div className="student-info">
                        <span className="student-name">{student?.name}</span>
                        <span className="student-id">ID: {student?.student_id}</span>
                    </div>
                </div>
            </header>

            {message.text && (
                <div className={`message ${message.type}`}>{message.text}</div>
            )}

            <div className="enrollments-content">
                <div className="summary-card">
                    <div className="summary-item">
                        <span className="summary-label">Enrolled Classes</span>
                        <span className="summary-value">{enrollments.length}</span>
                    </div>
                    <div className="summary-item">
                        <span className="summary-label">Total Credits</span>
                        <span className="summary-value">{totalCredits}</span>
                    </div>
                </div>

                {loading ? (
                    <div className="loading">Loading your enrollments...</div>
                ) : enrollments.length === 0 ? (
                    <div className="no-enrollments">
                        <h3>No Classes Enrolled</h3>
                        <p>You haven't enrolled in any classes yet. Go to Class Search to add classes.</p>
                    </div>
                ) : (
                    <div className="enrollments-list">
                        {enrollments.map(e => (
                            <div key={`${e.course_id}-${e.sec_no}`} className="enrollment-card">
                                <div className="course-info">
                                    <div className="course-header">
                                        <span className="course-code">{e.course_code}</span>
                                        <span className="section-badge">Section {e.sec_no}</span>
                                    </div>
                                    <h3 className="course-title">{e.course_title}</h3>
                                    <div className="course-details">
                                        <div className="detail">
                                            <span className="icon">👤</span>
                                            <span>{e.instructor_name}</span>
                                        </div>
                                        <div className="detail">
                                            <span className="icon">📅</span>
                                            <span>{e.days} {formatTime(e.start_time)} - {formatTime(e.end_time)}</span>
                                        </div>
                                        <div className="detail">
                                            <span className="icon">📍</span>
                                            <span>{e.building ? `${e.building} ${e.room_no}` : 'Online'}</span>
                                        </div>
                                    </div>
                                </div>
                                <button 
                                    className="drop-btn"
                                    onClick={() => handleDrop(e.course_id, e.sec_no, e.course_code)}
                                >
                                    Drop Class
                                </button>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}

export default MyEnrollments;

