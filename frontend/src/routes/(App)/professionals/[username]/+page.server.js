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

        // const reviews = [];

        return {
            props: {
                ok: true,
                professional,
                reviews
            }
        }
    } catch (error) {
        // throw redirect(302, '/');
        console.error(error)
        return {
            props: {
                ok: false,
                error: error.message
            }
        }
    }
}