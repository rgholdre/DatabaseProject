import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

function Home() {
    return (
        <div className="home">
            <div className="hero">
                <h1>Welcome to the University Course Management System</h1>
                <p>Search for courses, view sections, and manage your enrollments</p>
            </div>
            
            <div className="features">
                <div className="feature-card">
                    <div className="feature-icon">📚</div>
                    <h3>Browse Courses</h3>
                    <p>Explore our catalog of available courses across all departments</p>
                    <Link to="/courses" className="feature-link">View Courses →</Link>
                </div>
                
                <div className="feature-card">
                    <div className="feature-icon">📅</div>
                    <h3>View Sections</h3>
                    <p>Check available sections, schedules, and instructors</p>
                    <Link to="/sections" className="feature-link">View Sections →</Link>
                </div>
                
                <div className="feature-card">
                    <div className="feature-icon">👥</div>
                    <h3>Student Portal</h3>
                    <p>Manage student information and view enrollments</p>
                    <Link to="/students" className="feature-link">Student Portal →</Link>
                </div>
                
                <div className="feature-card">
                    <div className="feature-icon">✏️</div>
                    <h3>Enrollments</h3>
                    <p>Enroll in courses and manage your schedule</p>
                    <Link to="/enrollments" className="feature-link">Manage Enrollments →</Link>
                </div>
            </div>
        </div>
    );
}

export default Home;

