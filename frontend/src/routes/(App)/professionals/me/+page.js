import { redirect } from "@sveltejs/kit";
import { authStore, auth } from "$lib/auth_store";
import { PUBLIC_API_URL } from "$env/static/public";
import { get } from 'svelte/store';

export const ssr = false;

/** @type {import('./$types').PageLoad} */
export const load = async () => {
    if (!auth.isLoggedIn()) {
        throw redirect(302, '/')
    }

    try {
        const user = await auth.fetchUser();

        const url = `${PUBLIC_API_URL}/professionals/${user.username}`;
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

        const reviewsresponse = await fetch(`${PUBLIC_API_URL}/reviews/professionals/${professional.professional.id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include'
        });

        if (!reviewsresponse.ok) {
            console.log("error")
            const error = await reviewsresponse.json();
            throw new Error(error.detail || 'Failed to fetch reviews');
        }

        const reviews = await reviewsresponse.json();


        return {
            props: {
                ok: true,
                professional,
                reviews
            }
        }
    } catch (error) {
        console.error(error)
        return {
            props: {
                ok: false,
                error: error.message
            }
        }
    }
}