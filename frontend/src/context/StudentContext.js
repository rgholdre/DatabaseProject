import React, { createContext, useState, useContext } from 'react';

const StudentContext = createContext();

export const useStudent = () => useContext(StudentContext);

export const StudentProvider = ({ children }) => {
    const [student, setStudent] = useState(null);

    const login = (studentData) => {
        setStudent(studentData);
    };

    const logout = () => {
        setStudent(null);
    };

    return (
        <StudentContext.Provider value={{ student, login, logout }}>
            {children}
        </StudentContext.Provider>
    );
};

