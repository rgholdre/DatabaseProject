import React, { useState, useEffect } from 'react';
import { enrollmentAPI, studentAPI, sectionAPI } from '../api';
import './Enrollments.css';

function Enrollments() {
    const [enrollments, setEnrollments] = useState([]);
    const [students, setStudents] = useState([]);
    const [sections, setSections] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [showEnrollForm, setShowEnrollForm] = useState(false);
    const [newEnrollment, setNewEnrollment] = useState({
        student_id: '', course_id: '', sec_no: ''
    });

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            setLoading(true);
            const [enrollData, studentData, sectionData] = await Promise.all([
                enrollmentAPI.getAll(),
                studentAPI.getAll(),
                sectionAPI.getAll()
            ]);
            setEnrollments(enrollData);
            setStudents(studentData);
            setSections(sectionData);
            setError(null);
        } catch (err) {
            setError('Failed to load data. Make sure the backend is running.');
        } finally {
            setLoading(false);
        }
    };

    const handleEnroll = async (e) => {
        e.preventDefault();
        try {
            const [courseId, secNo] = newEnrollment.section.split('-');
            await enrollmentAPI.create({
                student_id: parseInt(newEnrollment.student_id),
                course_id: parseInt(courseId),
                sec_no: parseInt(secNo)
            });
            setShowEnrollForm(false);
            setNewEnrollment({ student_id: '', section: '' });
            loadData();
        } catch (err) {
            setError('Failed to enroll: ' + err.message);
        }
    };

    const handleUnenroll = async (studentId, courseId, secNo) => {
        if (window.confirm('Are you sure you want to drop this course?')) {
            try {
                await enrollmentAPI.delete(studentId, courseId, secNo);
                loadData();
            } catch (err) {
                setError('Failed to unenroll: ' + err.message);
            }
        }
    };

    if (loading) return <div className="loading">Loading enrollments...</div>;

    return (
        <div className="enrollments-page">
            <div className="page-header">
                <h1>Enrollment Management</h1>
                <button 
                    className="enroll-btn"
                    onClick={() => setShowEnrollForm(!showEnrollForm)}
                >
                    {showEnrollForm ? 'Cancel' : '+ New Enrollment'}
                </button>
            </div>

            {error && <div className="error-message">{error}</div>}

            {showEnrollForm && (
                <form onSubmit={handleEnroll} className="enroll-form">
                    <h3>Enroll Student in Course</h3>
                    <div className="form-row">
                        <select 
                            required
                            value={newEnrollment.student_id}
                            onChange={e => setNewEnrollment({...newEnrollment, student_id: e.target.value})}
                        >
                            <option value="">Select Student</option>
                            {students.map(s => (
                                <option key={s.student_id} value={s.student_id}>
                                    {s.name} ({s.student_id})
                                </option>
                            ))}
                        </select>
                        <select 
                            required
                            value={newEnrollment.section}
                            onChange={e => setNewEnrollment({...newEnrollment, section: e.target.value})}
                        >
                            <option value="">Select Section</option>
                            {sections.map(sec => (
                                <option 
                                    key={`${sec.course_id}-${sec.sec_no}`} 
                                    value={`${sec.course_id}-${sec.sec_no}`}
                                >
                                    {sec.course_code} - Section {sec.sec_no} ({sec.term} {sec.year})
                                </option>
                            ))}
                        </select>
                        <button type="submit" className="submit-btn">Enroll</button>
                    </div>
                </form>
            )}

            <div className="enrollments-table-container">
                <table className="enrollments-table">
                    <thead>
                        <tr>
                            <th>Student</th>
                            <th>Course</th>
                            <th>Section</th>
                            <th>Term</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {enrollments.map(e => (
                            <tr key={`${e.student_id}-${e.course_id}-${e.sec_no}`}>
                                <td>{e.student_name}</td>
                                <td>
                                    <strong>{e.course_code}</strong>
                                    <br />
                                    <small>{e.course_title}</small>
                                </td>
                                <td>{e.sec_no}</td>
                                <td>{e.term} {e.year}</td>
                                <td>
                                    <button 
                                        className="drop-btn"
                                        onClick={() => handleUnenroll(e.student_id, e.course_id, e.sec_no)}
                                    >
                                        Drop
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {enrollments.length === 0 && !error && (
                <div className="no-results">No enrollments found.</div>
            )}
        </div>
    );
}

export default Enrollments;

