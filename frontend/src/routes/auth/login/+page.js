import { redirect } from '@sveltejs/kit';
import { auth } from '$lib/auth_store';

export const load = async () => {
    // Check if user is already logged in
    if (auth.isLoggedIn()) {
        throw redirect(302, '/');
    }

    return {
        // Return an action that can be used in the page component
        loginAction: async ({ email, password }) => {
            return auth.login(email, password);
        }
    };
};