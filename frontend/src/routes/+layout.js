import { browser } from '$app/environment';
import { PUBLIC_API_URL } from '$env/static/public';

export const prerender = false;
export const ssr = true;

// Handle client-side theme initialization
if (browser) {
    const theme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', theme);
}