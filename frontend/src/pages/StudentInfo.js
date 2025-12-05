import React, { useState, useEffect } from 'react';
import { useStudent } from '../context/StudentContext';
import { enrollmentAPI } from '../api';
import './StudentInfo.css';

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
            const data = await enrollmentAPI.getByStudent(student.student_id);
            setEnrollments(data);
        } catch (err) {
            setMessage({ text: 'Failed to load enrollments', type: 'error' });
        } finally {
            setLoading(false);
        }
    };

    const formatTime = (time) => time ? time.substring(0, 5) : 'TBA';

    const totalCredits = enrollments.reduce((sum, e) => sum + (e.credits || 3), 0);

    return (
        <div className="my-enrollments-page">
            <header className="enrollments-header">
                <div className="header-content">
                    <h1>My ASU</h1>
                    <div className="student-info">
                        <span className="student-name">{student?.name}</span>
                        <span className="student-id">Student ID: {student?.student_id}</span>
                    </div>
                </div>
            </header>

            {message.text && (
                <div className={`message ${message.type}`}>{message.text}</div>
            )}


            <div className="student-content">
                <div className="summary-card">
                    <div className="summary-item">
                        <span className="summary-label-student">Student Email</span>
                        <span className="summary-value-student">{student?.email}</span>
                        <span className="summary-label-student">Student Major</span>
                        <span className="summary-value-student">{student?.major}</span>
                        <span className="summary-label-student">Class Year</span>
                        <span className="summary-value-student">{student?.class_year}</span>
                    </div>
                </div>
                
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

            </div>


            </div>
        </div>
    );
}

export default MyEnrollments;

