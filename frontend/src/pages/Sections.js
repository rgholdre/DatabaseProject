import React, { useState, useEffect } from 'react';
import { sectionAPI } from '../api';
import './Sections.css';

function Sections() {
    const [sections, setSections] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [filter, setFilter] = useState({ term: '', modality: '' });

    useEffect(() => {
        loadSections();
    }, []);

    const loadSections = async () => {
        try {
            setLoading(true);
            const data = await sectionAPI.getAll();
            setSections(data);
            setError(null);
        } catch (err) {
            setError('Failed to load sections. Make sure the backend is running.');
        } finally {
            setLoading(false);
        }
    };

    const filteredSections = sections.filter(section => {
        if (filter.term && section.term !== filter.term) return false;
        if (filter.modality && section.modality !== filter.modality) return false;
        return true;
    });

    const formatTime = (time) => {
        if (!time) return 'TBA';
        return time.substring(0, 5);
    };

    if (loading) return <div className="loading">Loading sections...</div>;

    return (
        <div className="sections-page">
            <h1>Available Sections</h1>

            <div className="filters">
                <select 
                    value={filter.term} 
                    onChange={(e) => setFilter({...filter, term: e.target.value})}
                    className="filter-select"
                >
                    <option value="">All Terms</option>
                    <option value="Fall">Fall</option>
                    <option value="Spring">Spring</option>
                    <option value="Summer">Summer</option>
                </select>

                <select 
                    value={filter.modality} 
                    onChange={(e) => setFilter({...filter, modality: e.target.value})}
                    className="filter-select"
                >
                    <option value="">All Modalities</option>
                    <option value="in_person">In Person</option>
                    <option value="online">Online</option>
                    <option value="hybrid">Hybrid</option>
                </select>
            </div>

            {error && <div className="error-message">{error}</div>}

            <div className="sections-table-container">
                <table className="sections-table">
                    <thead>
                        <tr>
                            <th>Course</th>
                            <th>Section</th>
                            <th>Instructor</th>
                            <th>Schedule</th>
                            <th>Location</th>
                            <th>Modality</th>
                            <th>Term</th>
                            <th>Capacity</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredSections.map(section => (
                            <tr key={`${section.course_id}-${section.sec_no}`}>
                                <td>
                                    <strong>{section.course_code}</strong>
                                    <br />
                                    <small>{section.course_title}</small>
                                </td>
                                <td>{section.sec_no}</td>
                                <td>{section.instructor_name}</td>
                                <td>
                                    {section.days} {formatTime(section.start_time)}-{formatTime(section.end_time)}
                                </td>
                                <td>
                                    {section.building ? `${section.building} ${section.room_no}` : 'Online'}
                                </td>
                                <td>
                                    <span className={`modality-badge ${section.modality}`}>
                                        {section.modality.replace('_', ' ')}
                                    </span>
                                </td>
                                <td>{section.term} {section.year}</td>
                                <td>{section.capacity}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {filteredSections.length === 0 && !error && (
                <div className="no-results">No sections match your filters.</div>
            )}
        </div>
    );
}

export default Sections;

