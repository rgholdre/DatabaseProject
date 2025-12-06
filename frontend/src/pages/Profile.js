import React, { useState } from 'react';
import { useStudent } from '../context/StudentContext';
import './Profile.css';

function Profile() {
    const { student } = useStudent();
    const [isEditing, setIsEditing] = useState(false);
    const [editData, setEditData] = useState(student || {});

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setEditData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSaveChanges = () => {
        // In a real application, this would save to the backend
        // For now, we'll just close the edit mode
        setIsEditing(false);
    };

    const handleCancel = () => {
        setEditData(student);
        setIsEditing(false);
    };

    return (
        <div className="profile-page">
            <div className="profile-container">
                <div className="profile-header">
                    <h1>👤 My Profile</h1>
                    <p>Your account information</p>
                </div>

                {!isEditing ? (
                    <div className="profile-content">
                        <div className="profile-card">
                            <div className="profile-section">
                                <div className="profile-item">
                                    <div className="profile-label">Full Name</div>
                                    <div className="profile-value">{student?.name || 'N/A'}</div>
                                </div>

                                <div className="profile-item">
                                    <div className="profile-label">Student ID</div>
                                    <div className="profile-value">{student?.studentid || student?.student_id || 'N/A'}</div>
                                </div>

                                <div className="profile-item">
                                    <div className="profile-label">Email Address</div>
                                    <div className="profile-value">{student?.email || 'N/A'}</div>
                                </div>

                                <div className="profile-item">
                                    <div className="profile-label">Major</div>
                                    <div className="profile-value">{student?.major || 'N/A'}</div>
                                </div>

                                <div className="profile-item">
                                    <div className="profile-label">Class Year</div>
                                    <div className="profile-value">{student?.classyear || student?.class_year || 'N/A'}</div>
                                </div>
                            </div>
                        </div>

                        <div className="profile-actions">
                            <button 
                                className="edit-btn"
                                onClick={() => setIsEditing(true)}
                            >
                                ✏️ Edit Profile
                            </button>
                        </div>
                    </div>
                ) : (
                    <div className="profile-content">
                        <div className="profile-card edit-mode">
                            <div className="profile-section">
                                <div className="form-group">
                                    <label htmlFor="name">Full Name</label>
                                    <input
                                        type="text"
                                        id="name"
                                        name="name"
                                        value={editData?.name || ''}
                                        onChange={handleInputChange}
                                    />
                                </div>

                                <div className="form-group">
                                    <label htmlFor="studentid">Student ID</label>
                                    <input
                                        type="text"
                                        id="studentid"
                                        name="studentid"
                                        value={editData?.studentid || editData?.student_id || ''}
                                        disabled
                                        title="Student ID cannot be changed"
                                    />
                                </div>

                                <div className="form-group">
                                    <label htmlFor="email">Email Address</label>
                                    <input
                                        type="email"
                                        id="email"
                                        name="email"
                                        value={editData?.email || ''}
                                        onChange={handleInputChange}
                                    />
                                </div>

                                <div className="form-group">
                                    <label htmlFor="major">Major</label>
                                    <input
                                        type="text"
                                        id="major"
                                        name="major"
                                        value={editData?.major || ''}
                                        onChange={handleInputChange}
                                    />
                                </div>

                                <div className="form-group">
                                    <label htmlFor="classyear">Class Year</label>
                                    <select
                                        id="classyear"
                                        name="classyear"
                                        value={editData?.classyear || editData?.class_year || ''}
                                        onChange={handleInputChange}
                                    >
                                        <option value="">Select class year</option>
                                        <option value="Freshman">Freshman</option>
                                        <option value="Sophomore">Sophomore</option>
                                        <option value="Junior">Junior</option>
                                        <option value="Senior">Senior</option>
                                    </select>
                                </div>
                            </div>
                        </div>

                        <div className="profile-actions edit-actions">
                            <button 
                                className="save-btn"
                                onClick={handleSaveChanges}
                            >
                                ✓ Save Changes
                            </button>
                            <button 
                                className="cancel-btn"
                                onClick={handleCancel}
                            >
                                ✕ Cancel
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

export default Profile;
