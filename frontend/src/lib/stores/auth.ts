// src/lib/stores/auth.ts
import { writable } from 'svelte/store';

interface User {
    id: number;
    email: string;
    is_active: boolean;
}

function createAuthStore() {
    const { subscribe, set } = writable<User | null>(null);
    const { subscribe: subscribeAuth, set: setAuth } = writable(false);

    return {
        subscribe,
        subscribeAuth,
        setUser: (user: User | null) => {
            set(user);
            setAuth(!!user);
        },
        logout: () => {
            set(null);
            setAuth(false);
        }
    };
}

export const auth = createAuthStore();
export const user = { subscribe: auth.subscribe }; // Add this line
export const isAuthenticated = { subscribe: auth.subscribeAuth };