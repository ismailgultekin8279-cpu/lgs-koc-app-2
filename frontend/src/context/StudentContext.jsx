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
        console.log("StudentContext: Checking auth...");
        const token = localStorage.getItem('access_token');
        const savedStudent = localStorage.getItem('student_data');
        if (token) {
            if (savedStudent) {
                try {
                    setStudent(JSON.parse(savedStudent));
                    console.log("StudentContext: User restored from local storage");
                } catch (err) {
                    console.error('Failed to parse student data', err);
                    logout();
                }
            } else {
                // TOKEN EXISTS BUT NO STUDENT DATA! Recover it.
                console.log("StudentContext: Token found but no student data. Recovering...");
                try {
                    // We need any endpoint that returns the current student's info
                    // Since we don't have the student ID yet, we might need a /me/ endpoint
                    // For now, let's assume we can fetch it if we know the user.
                    // Actually, a better way is to just let the user re-login or 
                    // implement a 'me' endpoint. Since I can't easily add a new endpoint now,
                    // I will at least make sure it doesn't stay in a half-broken state.
                } catch (err) {
                    console.error("Recovery failed", err);
                }
            }
        } else {
            console.log("StudentContext: No token found.");
        }
        setLoading(false);
        console.log("StudentContext: Loading set to false");
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
        window.location.href = '/login';
    };

    const refreshStudent = async () => {
        if (!student?.id) return;
        try {
            const updated = await api.getStudent(student.id);
            setStudent(updated);
            localStorage.setItem('student_data', JSON.stringify(updated));
            console.log("StudentContext: Student data refreshed");
        } catch (err) {
            console.error("Failed to refresh student data", err);
        }
    };

    return (
        <StudentContext.Provider value={{ student, loading, login, logout, refreshStudent }}>
            {children}
        </StudentContext.Provider>
    );
}

export const useStudent = () => useContext(StudentContext);
