import { authStore, createAuth } from '$lib/auth_store';

/** @type {import('./$types').LayoutLoad} */
export const load = async ({ fetch }) => {
    authStore.update(state => ({ ...state, isAuthenticating: true }));

    // Create auth instance with SvelteKit's fetch
    const auth = createAuth(fetch);
    
    // Only run on client side
    if (typeof window !== 'undefined') {
        const token = auth.getToken();
        if (token) {
            try {
                console.log('Fetching user...');               
                await auth.fetchUser();
            } catch (error) {
                // Handle error silently - auth store already handles logout
                console.error('Failed to fetch user:', error);
            }
        }
    }
    
    // Return empty object since this is a layout load function
    return {};
};