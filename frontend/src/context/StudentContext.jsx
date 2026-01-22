import { createContext, useContext, useState, useEffect } from 'react';
import { api } from '../services/api';

const StudentContext = createContext();

export function StudentProvider({ children }) {
    const [student, setStudent] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        checkAuth();
    }, []);

    const checkAuth = async () => {
        const token = localStorage.getItem('access_token');
        const savedStudent = localStorage.getItem('student_data');

        if (token && savedStudent) {
            try {
                setStudent(JSON.parse(savedStudent));
            } catch (err) {
                console.error('Failed to parse student data', err);
                logout();
            }
        }
        setLoading(false);
    };

    const login = (authData) => {
        // authData = { access, refresh, student }
        if (authData.access) localStorage.setItem('access_token', authData.access);
        if (authData.refresh) localStorage.setItem('refresh_token', authData.refresh);
        if (authData.student) {
            localStorage.setItem('student_data', JSON.stringify(authData.student));
            setStudent(authData.student);
        }
    };

    const logout = () => {
        setStudent(null);
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('student_data');
        localStorage.removeItem('student_id'); // Clear legacy
    };

    return (
        <StudentContext.Provider value={{ student, loading, login, logout }}>
            {children}
        </StudentContext.Provider>
    );
}

export const useStudent = () => useContext(StudentContext);
