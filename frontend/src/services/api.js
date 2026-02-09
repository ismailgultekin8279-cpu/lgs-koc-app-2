// Use env var for production, fallback to relative path for dev proxy
const BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

const getHeaders = () => {
    const headers = { 'Content-Type': 'application/json' };
    const token = localStorage.getItem('access_token');
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    return headers;
};

export const api = {
    // Auth
    register: async (data) => {
        const res = await fetch(`${BASE_URL}/students/auth/register/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        if (!res.ok) {
            const err = await res.json();
            throw new Error(JSON.stringify(err));
        }
        return res.json();
    },

    login: async (username, password) => {
        const res = await fetch(`${BASE_URL}/students/auth/login/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password }),
        });
        if (!res.ok) throw new Error('Giriş başarısız');
        return res.json();
    },

    // Students
    getStudent: async (id) => {
        const res = await fetch(`${BASE_URL}/students/${id}/`, { headers: getHeaders() });
        if (!res.ok) throw new Error('Failed to fetch student');
        return res.json();
    },

    updateStudent: async (id, data) => {
        const res = await fetch(`${BASE_URL}/students/${id}/`, {
            method: 'PATCH',
            headers: getHeaders(),
            body: JSON.stringify(data),
        });
        if (!res.ok) throw new Error('Failed to update student');
        return res.json();
    },

    // Exams
    saveExamResult: async (data) => {
        const res = await fetch(`${BASE_URL}/students/exam-results/`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify(data),
        });
        if (!res.ok) throw new Error('Failed to save exam result');
        return res.json();
    },

    getLatestExam: async (studentId) => {
        // Fetch exam results, sorted by date descending (we might need to ensure backend supports ordering)
        // For now, let's assuming GET /students/exam-results/?student_id=X&ordering=-exam_date returns list
        // Or we can filter client side if needed, but backend filter is better.
        // Let's rely on standard list endpoint for now.
        const res = await fetch(`${BASE_URL}/students/exam-results/?student_id=${studentId}&ordering=-exam_date`, {
            headers: getHeaders(),
        });
        if (!res.ok) throw new Error('Failed to fetch exams');
        return res.json();
    },

    // Tasks
    getStudentTasks: async (studentId, date) => {
        let url = `${BASE_URL}/students/tasks/?student=${studentId}`;
        if (date) url += `&date=${date}`;

        const res = await fetch(url, { headers: getHeaders() });
        if (!res.ok) throw new Error('Failed to fetch tasks');
        return res.json();
    },

    toggleTaskStatus: async (taskId) => {
        const res = await fetch(`${BASE_URL}/students/tasks/${taskId}/toggle_status/`, {
            method: 'POST',
            headers: getHeaders(),
        });
        if (!res.ok) throw new Error('Failed to update task');
        return res.json();
    },

    // Coaching
    generatePlan: async (studentId) => {
        const res = await fetch(`${BASE_URL}/coaching/coach/${studentId}/generate_plan/`, {
            method: 'POST',
            headers: getHeaders(),
        });
        if (!res.ok) throw new Error('Failed to generate plan');
        return res.json();
    },

    getCoachStatus: async (studentId) => {
        const res = await fetch(`${BASE_URL}/coaching/coach/${studentId}/status/`, {
            headers: getHeaders(),
        });
        if (!res.ok) throw new Error('Failed to get coach status');
        return res.json();
    },

    // Curriculum
    getCurriculum: async (subject = 'matematik') => {
        const res = await fetch(`${BASE_URL}/coaching/curriculum/?view=tree&subject=${subject}`, {
            headers: getHeaders(),
        });
        if (!res.ok) throw new Error('Failed to fetch curriculum');
        return res.json();
    },

    // Admin / CRUD
    getTopics: async () => {
        const res = await fetch(`${BASE_URL}/coaching/curriculum/`, {
            headers: getHeaders(),
        });
        return res.json();
    },

    createTopic: async (data) => {
        const res = await fetch(`${BASE_URL}/coaching/curriculum/`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify(data),
        });
        if (!res.ok) throw new Error('Failed to create topic');
        return res.json();
    },

    deleteTopic: async (id) => {
        const res = await fetch(`${BASE_URL}/coaching/curriculum/${id}/`, {
            method: 'DELETE',
            headers: getHeaders(),
        });
        if (!res.ok) throw new Error('Failed to delete topic');
        return true;
    },

    toggleTopic: async (topicId) => {
        const res = await fetch(`${BASE_URL}/coaching/curriculum/${topicId}/toggle/`, {
            method: 'POST',
            headers: getHeaders(),
        });
        if (!res.ok) throw new Error('Failed to update topic');
        return res.json();
    }
};
