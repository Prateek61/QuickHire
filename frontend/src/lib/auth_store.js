import { writable } from 'svelte/store';
import { goto } from '$app/navigation';
import { PUBLIC_API_URL } from '$lib/constants';

// Auth store for managing user state
export const authStore = writable({
    user: null,
    token: null,
    isAuthenticated: false,
    isAuthenticating: false
})

// Local storage handling
function getStoredToken() {
    if (typeof window !== 'undefined')
    {
        return localStorage.getItem('session');
    }

    return null;
}

function setStoredToken(token) {
    if (typeof window !== 'undefined')
    {
        localStorage.setItem('session', token);
    }
}

function clearStoredToken() {
    if (typeof window !== 'undefined')
    {
        localStorage.removeItem('session');
    }
}

// Create auth utilities with optional fetch parameter
export function createAuth(customFetch = fetch) {
    return {
        async login(username, password) {
            try {
                const response = await customFetch(`${PUBLIC_API_URL}/auth/login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({username, password}),
                    credentials: 'include'
                });
        
                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.detail || 'Login failed')
                }

                const data = await response.json();
                setStoredToken(data.access_token);

                await this.fetchUser(customFetch);

                return { success: true };
            } catch (error) {
                return { success: false, error: error.message };
            }
        },

        async register(userData) {
            try {
                const response = await customFetch(`${PUBLIC_API_URL}/auth/register`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(userData),
                    credentials: 'include'
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.detail || 'Registration failed');
                }

                const data = await response.json();
                setStoredToken(data.token);
                await this.fetchUser(customFetch);

                return { success: true };
            } catch (error) {
                return { success: false, error: error.message };
            }
        },

        async fetchUser(fetchFn = customFetch) {
            authStore.update(state => ({ ...state, isAuthenticating: true }));

            try {
                const token = this.getToken();
                if (!token) throw new Error('No token available');

                const response = await fetchFn(`${PUBLIC_API_URL}/auth/me`, {
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
                
                authStore.update(state => ({ ...state, isAuthenticating: false }));
                return user;
            } catch (error) {
                authStore.update(state => ({ ...state, isAuthenticating: false }));
                this.logout();
                throw error;
            }
        },

        getToken() {
            return getStoredToken();
        },

        async logout() {
            // clearStoredToken();

            // authStore.update(state => ({
            //     ...state,
            //     user: null,
            //     token: null,
            //     isAuthenticated: false
            // }));

            // goto('/');
            console.log("logout called")
        },

        isLoggedIn() {
            return !!this.getToken();
        },

        isAuthenticated() {
            while (authStore.get().isAuthenticating) {
                // Wait for authentication to finish
            }

            return authStore.get().isAuthenticated;
        }
    };
}

// Default instance using window.fetch
export const auth = createAuth();

// Initialize auth state if token exists and in browser
if (typeof window !== 'undefined') {
    const token = getStoredToken();
    if (token) {
        auth.fetchUser().catch(() => {
            auth.logout();
        });
    }
}