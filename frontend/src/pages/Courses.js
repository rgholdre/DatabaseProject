import React, { useState, useEffect } from 'react';
import { courseAPI } from '../api';
import './Courses.css';

function Courses() {
    const [courses, setCourses] = useState([]);
    const [searchQuery, setSearchQuery] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        loadCourses();
    }, []);

    const loadCourses = async () => {
        try {
            setLoading(true);
            const data = await courseAPI.getAll();
            setCourses(data);
            setError(null);
        } catch (err) {
            setError('Failed to load courses. Make sure the backend is running.');
        } finally {
            setLoading(false);
        }
    };

    const handleSearch = async (e) => {
        e.preventDefault();
        try {
            setLoading(true);
            const data = await courseAPI.search(searchQuery);
            setCourses(data);
            setError(null);
        } catch (err) {
            setError('Search failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <div className="loading">Loading courses...</div>;

    return (
        <div className="courses-page">
            <h1>Course Catalog</h1>
            
            <form onSubmit={handleSearch} className="search-form">
                <input
                    type="text"
                    placeholder="Search courses by title or code..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="search-input"
                />
                <button type="submit" className="search-btn">Search</button>
                <button type="button" className="reset-btn" onClick={() => {
                    setSearchQuery('');
                    loadCourses();
                }}>Reset</button>
            </form>

            {error && <div className="error-message">{error}</div>}

            <div className="courses-grid">
                {courses.map(course => (
                    <div key={course.course_id} className="course-card">
                        <div className="course-code">{course.code}</div>
                        <h3 className="course-title">{course.title}</h3>
                        <div className="course-details">
                            <span className="course-level">Level: {course.level}</span>
                            <span className="course-credits">{course.credits} Credits</span>
                        </div>
                        {course.section_count !== undefined && (
                            <div className="section-count">
                                {course.section_count} section(s) available
                            </div>
                        )}
                    </div>
                ))}
            </div>

            {courses.length === 0 && !error && (
                <div className="no-results">No courses found.</div>
            )}
        </div>
    );
}

export default Courses;

