import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useStudent } from '../context/StudentContext';
import { studentAPI } from '../api';
import './Login.css';

function Login() {
    const [studentId, setStudentId] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const { login } = useStudent();
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            const student = await studentAPI.getById(studentId);
            if (student) {
                login(student);
                navigate('/classes');
            } else {
                setError('Student not found. Please check your ID.');
            }
        } catch (err) {
            setError('Student not found. Please check your ID.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-page">
            <div className="login-container">
                <div className="login-header">
                    <h1>🎓 Course Registration</h1>
                    <p>University Course Management System</p>
                </div>
                
                <form onSubmit={handleLogin} className="login-form">
                    <h2>Student Login</h2>
                    
                    <div className="form-group">
                        <label htmlFor="studentId">Student ID</label>
                        <input
                            type="text"
                            id="studentId"
                            value={studentId}
                            onChange={(e) => setStudentId(e.target.value)}
                            placeholder="Enter your Student ID"
                            required
                        />
                    </div>

                    {error && <div className="error-message">{error}</div>}

                    <button type="submit" disabled={loading}>
                        {loading ? 'Logging in...' : 'Login'}
                    </button>
                </form>

                <div className="demo-info">
                    <p><strong>Demo Student IDs:</strong></p>
                    <p>Try: 1, 2, 3, 4, or 5</p>
                </div>
            </div>
        </div>
    );
}

export default Login;

