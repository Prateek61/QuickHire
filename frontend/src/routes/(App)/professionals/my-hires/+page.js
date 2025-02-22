import { redirect } from "@sveltejs/kit";
import { auth, authStore } from "$lib/auth_store";
import { PUBLIC_API_URL } from "$env/static/public";

export const ssr = false;

/** @type {import('./$types').PageLoad} */
export const load = async ({ fetch }) => {
    if (!auth.isLoggedIn()) {
        throw redirect(302, '/')
    }

    try {
        const url = `${PUBLIC_API_URL}/hires/`;
        const token = auth.getToken();
        const response = await fetch(url, {
            // mode: 'no-cors',
            headers: {
                Authorization: `Bearer ${token}`
            },
            credentials: 'include'
        });

        if (!response.ok) {
            const error = await response.json();
            console.error(error)
            throw new Error(error.detail || 'Failed to fetch hires');
        }

        const hires = await response.json();

        return {
            props: {
                ok: true,
                hires: hires
            }
        }
    } catch (error) {
        return {
            props: {
                ok: false,
                error: error.message
            }
        }
    }
}
