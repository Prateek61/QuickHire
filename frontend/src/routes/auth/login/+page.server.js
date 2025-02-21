import { fail, redirect } from '@sveltejs/kit';
import { auth } from '$lib/auth';

/** @type {import('./$types').PageServerLoad} */
export function load({ locals }) {
    if (locals.user) {
        throw redirect(303, '/');
    }
}

/** @type {import('./$types').Actions} */
export const actions = {
    default: async ({ cookies, request }) => {
        const data = await request.formData();
        const username = data.get('email');
        const password = data.get('password');

        if (!username || !password) {
            return fail(400, { 
                error: 'Email and password are required',
                username
            });
        }

        const result = await auth.login(username, password);

        if (!result.success) {
            return fail(400, {
                error: result.error,
                username
            });
        }

        // Set session cookie
        cookies.set('session', result.token, {
            path: '/',
            httpOnly: true,
            sameSite: 'strict',
            secure: process.env.NODE_ENV === 'production',
            maxAge: 60 * 60 * 24 * 7 // 1 week
        });

        throw redirect(303, '/');
    }
};