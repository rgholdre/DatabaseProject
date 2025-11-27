// API service for connecting to Flask backend
const API_BASE_URL = 'http://localhost:5000/api';

// Generic fetch wrapper
async function fetchAPI(endpoint, options = {}) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        headers: {
            'Content-Type': 'application/json',
        },
        ...options,
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'API request failed');
    }
    
    return response.json();
}

// Course API
export const courseAPI = {
    getAll: () => fetchAPI('/courses'),
    getById: (id) => fetchAPI(`/courses/${id}`),
    search: (query, term, year) => {
        const params = new URLSearchParams();
        if (query) params.append('q', query);
        if (term) params.append('term', term);
        if (year) params.append('year', year);
        return fetchAPI(`/search/courses?${params.toString()}`);
    },
};

// Student API
export const studentAPI = {
    getAll: () => fetchAPI('/students'),
    getById: (id) => fetchAPI(`/students/${id}`),
    create: (data) => fetchAPI('/students', {
        method: 'POST',
        body: JSON.stringify(data),
    }),
};

// Instructor API
export const instructorAPI = {
    getAll: () => fetchAPI('/instructors'),
};

// Section API
export const sectionAPI = {
    getAll: () => fetchAPI('/sections'),
    getById: (courseId, secNo) => fetchAPI(`/sections/${courseId}/${secNo}`),
};

// Enrollment API
export const enrollmentAPI = {
    getAll: () => fetchAPI('/enrollments'),
    getByStudent: (studentId) => fetchAPI(`/enrollments/student/${studentId}`),
    create: (data) => fetchAPI('/enrollments', {
        method: 'POST',
        body: JSON.stringify(data),
    }),
    delete: (studentId, courseId, secNo) => fetchAPI(
        `/enrollments/${studentId}/${courseId}/${secNo}`,
        { method: 'DELETE' }
    ),
};

