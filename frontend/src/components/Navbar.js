import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useStudent } from '../context/StudentContext';
import './Navbar.css';

function Navbar() {
    const location = useLocation();
    const navigate = useNavigate();
    const { student, logout } = useStudent();

    const handleLogout = () => {
        logout();
        navigate('/');
    };

    return (
        <nav className="navbar">
            <div className="navbar-brand">
                <Link to="/classes">
                    <span className="asu-logo">ASU</span>
                    <span className="brand-text">Class Search</span>
                </Link>
            </div>
            <ul className="navbar-menu">
                <li className={location.pathname === '/classes' ? 'active' : ''}>
                    <Link to="/classes">Class Search</Link>
                </li>
                <li className={location.pathname === '/my-enrollments' ? 'active' : ''}>
                    <Link to="/my-enrollments">My Enrollments</Link>
                </li>
                <li className={location.pathname === '/profile' ? 'active' : ''}>
                    <Link to="/profile">Profile</Link>
                </li>
            </ul>
            <div className="navbar-user">
                {student && (
                    <>
                        <span className="student-name">👤 {student.name}</span>
                        <button className="logout-btn" onClick={handleLogout}>Logout</button>
                    </>
                )}
            </div>
        </nav>
    );
}

export default Navbar;


