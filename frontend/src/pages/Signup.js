import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useStudent } from '../context/StudentContext';
import { studentAPI } from '../api';
import './Signup.css';

function Signup() {
    const [formData, setFormData] = useState({
        name: '',
        studentId: '',
        email: '',
        major: '',
        classYear: ''
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const { login } = useStudent();
    const navigate = useNavigate();

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        // Validation
        if (!formData.name || !formData.studentId || !formData.email || !formData.major || !formData.classYear) {
            setError('All fields are required');
            setLoading(false);
            return;
        }

        if (!formData.email.includes('@')) {
            setError('Please enter a valid email address');
            setLoading(false);
            return;
        }

        try {
            // Create new student with studentid (using the student's input as ID)
            const newStudent = await studentAPI.create({
                studentid: parseInt(formData.studentId),
                name: formData.name,
                email: formData.email,
                major: formData.major,
                classyear: formData.classYear
            });
            
            // Log the student in
            login(newStudent);
            navigate('/classes');
        } catch (err) {
            setError(err.message || 'Failed to create account. Student ID may already exist.');
        } finally {
            setLoading(false);
        }
    };

    const handleBackToLogin = () => {
        navigate('/login');
    };

    return (
        <div className="signup-page">
            <div className="signup-container">
                <div className="signup-header">
                    <h1>🎓 Create Your Account</h1>
                    <p>University Course Management System</p>
                </div>

                <form onSubmit={handleSubmit} className="signup-form">
                    <h2>Student Sign Up</h2>

                    <div className="form-group">
                        <label htmlFor="name">Full Name</label>
                        <input
                            type="text"
                            id="name"
                            name="name"
                            value={formData.name}
                            onChange={handleInputChange}
                            placeholder="Enter your full name"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="studentId">Student ID</label>
                        <input
                            type="number"
                            id="studentId"
                            name="studentId"
                            value={formData.studentId}
                            onChange={handleInputChange}
                            placeholder="Enter your Student ID"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="email">Email Address</label>
                        <input
                            type="email"
                            id="email"
                            name="email"
                            value={formData.email}
                            onChange={handleInputChange}
                            placeholder="Enter your email"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="major">Major</label>
                        <input
                            type="text"
                            id="major"
                            name="major"
                            value={formData.major}
                            onChange={handleInputChange}
                            placeholder="Enter your major"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="classYear">Class Year</label>
                        <select
                            id="classYear"
                            name="classYear"
                            value={formData.classYear}
                            onChange={handleInputChange}
                            required
                        >
                            <option value="">Select your class year</option>
                            <option value="Freshman">Freshman</option>
                            <option value="Sophomore">Sophomore</option>
                            <option value="Junior">Junior</option>
                            <option value="Senior">Senior</option>
                        </select>
                    </div>

                    {error && <div className="error-message">{error}</div>}

                    <button type="submit" disabled={loading}>
                        {loading ? 'Creating Account...' : 'Sign Up'}
                    </button>
                </form>

                <div className="login-link">
                    <p>Already have an account? <button onClick={handleBackToLogin} className="link-button">Login here</button></p>
                </div>
            </div>
        </div>
    );
}

export default Signup;
