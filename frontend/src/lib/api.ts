const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = {
    auth: {
        login: async (email: string, password: string) => {
            return await api.post('/auth/login', { email, password });
        },
        register: async (email: string, password: string) => {
            return await api.post('/auth/register', { email, password });
        },
        logout: async () => {
            return await api.post('/auth/logout', {});
        }
    },
    routines: {
        list: async () => {
            return await api.get('/routines');
        },
        create: async (routine: any) => {
            return await api.post('/routines', routine);
        },
        start: async (id: string) => {
            return await api.post(`/routines/${id}/start`, {});
        },
        stop: async (id: string) => {
            return await api.post(`/routines/${id}/stop`, {});
        }
    },
    schedules: {
        list: async () => {
            return await api.get('/schedules');
        },
        create: async (schedule: any) => {
            return await api.post('/schedules', schedule);
        }
    },
    get: async (path: string) => {
        const response = await fetch(`${BASE_URL}${path}`, {
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
    },
    post: async (path: string, data: any) => {
        const response = await fetch(`${BASE_URL}${path}`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
    }
};