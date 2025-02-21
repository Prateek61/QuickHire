import { writable } from 'svelte/store';
import { goto } from '$app/navigation';
import { PUBLIC_API_URL } from '$env/static/public';

// Auth store for managing user state
export const authStore = writable({
    user: null,
    token: null,
    isAuthenticated: false
});

// Local storage handling
function getStoredToken() {
    if (typeof window !== 'undefined') {
        return localStorage.getItem('session');
    }
    return null;
}

function setStoredToken(token) {
    if (typeof window !== 'undefined') {
        localStorage.setItem('session', token);
    }
}

function clearStoredToken() {
    if (typeof window !== 'undefined') {
        localStorage.removeItem('session');
    }
}

// Auth utilities
export const auth = {
    async login(username, password) {
        try {
            const response = await fetch(`${PUBLIC_API_URL}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
                credentials: 'include' // Important for cookie handling
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Login failed');
            }

            const data = await response.json();
            setStoredToken(data.access_token);
            await this.fetchUser();

            return { success: true };
        } catch (error) {
            return { 
                success: false, 
                error: error.message 
            };
        }
    },

    async register(userData) {
        try {
            const response = await fetch(`${PUBLIC_API_URL}/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData),
                credentials: 'include' // Important for cookie handling
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Registration failed');
            }

            const data = await response.json();
            setStoredToken(data.access_token);
            await this.fetchUser();

            return { success: true };
        } catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    },

    async fetchUser() {
        try {
            const token = getStoredToken();
            if (!token) throw new Error('No token found');

            const response = await fetch(`${PUBLIC_API_URL}/auth/me`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                credentials: 'include'
            });

            if (!response.ok) {
                throw new Error('Failed to fetch user');
            }

            const user = await response.json();
            authStore.update(state => ({ 
                ...state, 
                user, 
                token,
                isAuthenticated: true 
            }));
            
            return user;
        } catch (error) {
            this.logout();
            throw error;
        }
    },

    getToken() {
        return getStoredToken();
    },

    async logout() {
        // Clear the cookie on server
        await fetch(`${PUBLIC_API_URL}/auth/logout`, {
            method: 'POST',
            credentials: 'include'
        });

        // Clear local storage and state
        clearStoredToken();
        authStore.set({
            user: null,
            token: null,
            isAuthenticated: false
        });

        // Redirect to login
        goto('/auth/login');
    },

    isLoggedIn() {
        return !!this.getToken();
    }
};

// Initialize auth state if token exists
if (typeof window !== 'undefined') {
    const token = getStoredToken();
    if (token) {
        auth.fetchUser().catch(() => {
            auth.logout();
        });
    }
}