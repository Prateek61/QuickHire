import { redirect } from '@sveltejs/kit';
import { auth, authStore } from '$lib/auth_store';

export const ssr = false;

export const load = async() => {
    // Check if user is not logged in
    if (!auth.isLoggedIn())
    {
        throw redirect(302, '/login');
    }
}