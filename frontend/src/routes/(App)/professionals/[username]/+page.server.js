import { redirect } from "@sveltejs/kit";
import { auth } from "$lib/auth_store";
import { PUBLIC_API_URL } from "$env/static/public";

/** @type {import('./$types').PageLoad} */
export const load = async ({ params, fetch }) => {
    try {
        const url = `${PUBLIC_API_URL}/professionals/${params.username}`;
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include'
        });

        if (!response.ok) {
            const error = await response.json();
            throw redirect(302, '/');
        }

        const professional = await response.json();

        return {
            props: {
                ok: true,
                professional
            }
        }
    } catch (error) {
        throw redirect(302, '/');

        return {
            props: {
                ok: false,
                error: error.message
            }
        }
    }
}