import { PUBLIC_API_URL } from '$env/static/public';

export async function load({ fetch }) {
    try {
        const url = `${PUBLIC_API_URL}/professionals`;

        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include'
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to fetch professionals');
        }

        const professionals_data = await response.json();

        return {
            props: {
                ok: true,
                professionals: professionals_data
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