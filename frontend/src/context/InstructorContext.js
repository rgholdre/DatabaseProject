import React, { createContext, useState, useContext } from 'react';

const InstructorContext = createContext();

export const useInstructor = () => useContext(InstructorContext);

export const InstructorProvider = ({ children }) => {
    const [instructor, setInstructor] = useState(null);

    const login = (instructorData) => {
        setInstructor(instructorData);
    };

    const logout = () => {
        setInstructor(null);
    };

    return (
        <InstructorContext.Provider value={{ instructor, login, logout }}>
            {children}
        </InstructorContext.Provider>
    );
};

