// src/lib/api.ts
const BASE_URL = 'http://localhost:8000/api/v1'; // Add this line

interface LoginResponse {
    access_token: string;
    token_type: string;
    user: {
        id: number;
        email: string;
        is_active: boolean;
    };
}

export const api = {
    auth: {
        login: async (email: string, password: string): Promise<LoginResponse> => {
            const formData = new FormData();
            formData.append('username', email);
            formData.append('password', password);
            
            const response = await fetch(`${BASE_URL}/auth/login`, {
                method: 'POST',
                body: formData,
                credentials: 'include'
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Login failed');
            }
            
            return await response.json();
        },
        
        register: async (email: string, password: string) => {
            const response = await fetch(`${BASE_URL}/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Registration failed');
            }
            
            return response.json();
        }
    }
};