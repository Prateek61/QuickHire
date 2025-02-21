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
        const confirmPassword = data.get('confirmPassword');
        const firstName = data.get('firstName');
        const lastName = data.get('lastName');
        const phone = data.get('phone');

        // Validation
        if (!username || !password || !confirmPassword) {
            return fail(400, {
                error: 'All required fields must be filled',
                username,
                firstName,
                lastName,
                phone
            });
        }

        if (password !== confirmPassword) {
            return fail(400, {
                error: 'Passwords do not match',
                username,
                firstName,
                lastName,
                phone
            });
        }

        const result = await auth.register({
            username,
            email: username,
            password,
            first_name: firstName,
            last_name: lastName,
            phone_no: phone || ''
        });

        if (!result.success) {
            return fail(400, {
                error: result.error,
                username,
                firstName,
                lastName,
                phone
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