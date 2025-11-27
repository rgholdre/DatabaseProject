import React, { useState, useEffect } from 'react';
import { useStudent } from '../context/StudentContext';
import { sectionAPI, enrollmentAPI } from '../api';
import './ClassSearch.css';

function ClassSearch() {
    const { student } = useStudent();
    const [sections, setSections] = useState([]);
    const [filteredSections, setFilteredSections] = useState([]);
    const [loading, setLoading] = useState(true);
    const [message, setMessage] = useState({ text: '', type: '' });
    
    // Filter states
    const [filters, setFilters] = useState({
        term: '',
        subject: '',
        number: '',
        keyword: ''
    });
    
    // Available filter options
    const [terms, setTerms] = useState([]);
    const [subjects, setSubjects] = useState([]);

    useEffect(() => {
        loadSections();
    }, []);

    const loadSections = async () => {
        try {
            setLoading(true);
            const data = await sectionAPI.getAll();
            setSections(data);
            setFilteredSections(data);
            
            // Extract unique terms and subjects
            const uniqueTerms = [...new Set(data.map(s => `${s.term} ${s.year}`))];
            const uniqueSubjects = [...new Set(data.map(s => s.course_code.match(/^[A-Z]+/)?.[0] || ''))];
            setTerms(uniqueTerms);
            setSubjects(uniqueSubjects.filter(Boolean).sort());
        } catch (err) {
            setMessage({ text: 'Failed to load classes', type: 'error' });
        } finally {
            setLoading(false);
        }
    };

    const handleSearch = () => {
        let results = [...sections];
        
        if (filters.term) {
            results = results.filter(s => `${s.term} ${s.year}` === filters.term);
        }
        if (filters.subject) {
            results = results.filter(s => s.course_code.startsWith(filters.subject));
        }
        if (filters.number) {
            results = results.filter(s => s.course_code.includes(filters.number));
        }
        if (filters.keyword) {
            const kw = filters.keyword.toLowerCase();
            results = results.filter(s => 
                s.course_title.toLowerCase().includes(kw) || 
                s.course_code.toLowerCase().includes(kw)
            );
        }
        setFilteredSections(results);
    };

    const handleEnroll = async (section) => {
        try {
            await enrollmentAPI.create({
                student_id: student.student_id,
                course_id: section.course_id,
                sec_no: section.sec_no
            });
            setMessage({ text: `Enrolled in ${section.course_code} Section ${section.sec_no}!`, type: 'success' });
            setTimeout(() => setMessage({ text: '', type: '' }), 3000);
        } catch (err) {
            setMessage({ text: 'Failed to enroll: ' + (err.message || 'Already enrolled or class full'), type: 'error' });
        }
    };

    const formatTime = (time) => time ? time.substring(0, 5) : 'TBA';

    return (
        <div className="class-search-page">
            {/* Header */}
            <header className="search-header">
                <div className="header-content">
                    <h1>Class Search</h1>
                </div>
            </header>

            {/* Search Filters */}
            <div className="search-filters">
                <div className="filters-container">
                    <div className="filter-group">
                        <label>Term</label>
                        <select value={filters.term} onChange={e => setFilters({...filters, term: e.target.value})}>
                            <option value="">All Terms</option>
                            {terms.map(t => <option key={t} value={t}>{t}</option>)}
                        </select>
                    </div>
                    <div className="filter-group">
                        <label>Subject</label>
                        <select value={filters.subject} onChange={e => setFilters({...filters, subject: e.target.value})}>
                            <option value="">Subject</option>
                            {subjects.map(s => <option key={s} value={s}>{s}</option>)}
                        </select>
                    </div>
                    <div className="filter-group">
                        <label>Number</label>
                        <input type="text" placeholder="Number" value={filters.number} 
                            onChange={e => setFilters({...filters, number: e.target.value})} />
                    </div>
                    <div className="filter-group keyword">
                        <label>Keyword search</label>
                        <input type="text" placeholder="Enter keywords" value={filters.keyword}
                            onChange={e => setFilters({...filters, keyword: e.target.value})} />
                    </div>
                    <button className="search-btn" onClick={handleSearch}>🔍 Search Classes</button>
                </div>
            </div>

            {/* Messages */}
            {message.text && (
                <div className={`message ${message.type}`}>{message.text}</div>
            )}

            {/* Results */}
            <div className="results-section">
                {loading ? (
                    <div className="loading">Loading classes...</div>
                ) : filteredSections.length === 0 ? (
                    <div className="no-results">No classes found. Try adjusting your filters.</div>
                ) : (
                    <div className="results-table">
                        <table>
                            <thead>
                                <tr>
                                    <th>Course</th>
                                    <th>Title</th>
                                    <th>Section</th>
                                    <th>Instructor</th>
                                    <th>Days/Time</th>
                                    <th>Location</th>
                                    <th>Seats</th>
                                    <th>Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                {filteredSections.map(sec => (
                                    <tr key={`${sec.course_id}-${sec.sec_no}`}>
                                        <td className="course-code">{sec.course_code}</td>
                                        <td>{sec.course_title}</td>
                                        <td>{sec.sec_no}</td>
                                        <td>{sec.instructor_name}</td>
                                        <td>{sec.days} {formatTime(sec.start_time)}-{formatTime(sec.end_time)}</td>
                                        <td>{sec.modality === 'online' ? 'Online' : `${sec.building || ''} ${sec.room_no || ''}`}</td>
                                        <td>{sec.capacity}</td>
                                        <td>
                                            <button className="enroll-btn" onClick={() => handleEnroll(sec)}>
                                                + Add
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </div>
    );
}

export default ClassSearch;

