import { redirect } from '@sveltejs/kit';
import { auth } from '$lib/auth_store';

export const load = async () => {
    // Check authentication on the client side
    if (!auth.isLoggedIn()) {
        throw redirect(302, '/auth/login');
    }
};