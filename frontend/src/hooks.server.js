import { redirect } from '@sveltejs/kit';

/** @type {import('@sveltejs/kit').Handle} */
export async function handle({ event, resolve }) {
    // Get auth token from cookies
    const token = event.cookies.get('session');

    // Protected routes - add your protected paths here
    const protectedPaths = ['/dashboard', '/profile', '/jobs'];
    const isProtectedRoute = protectedPaths.some(path => 
        event.url.pathname.startsWith(path)
    );

    // Auth routes
    const authPaths = ['/auth/login', '/auth/register'];
    const isAuthRoute = authPaths.some(path => 
        event.url.pathname.startsWith(path)
    );

    if (token) {
        try {
            // Try to fetch user data with token
            const response = await fetch(`${process.env.PUBLIC_API_URL}/auth/me`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                const user = await response.json();
                event.locals.user = user;
                event.locals.token = token;

                // Redirect from auth pages if logged in
                if (isAuthRoute) {
                    throw redirect(303, '/');
                }
            } else {
                // Clear invalid token
                event.cookies.delete('session');
                event.locals.user = null;
                event.locals.token = null;

                // Redirect to login if accessing protected route
                if (isProtectedRoute) {
                    throw redirect(303, '/auth/login');
                }
            }
        } catch (error) {
            // Error fetching user - clear token
            if (!(error instanceof redirect)) {
                event.cookies.delete('session');
                event.locals.user = null;
                event.locals.token = null;

                if (isProtectedRoute) {
                    throw redirect(303, '/auth/login');
                }
            } else {
                throw error;
            }
        }
    } else if (isProtectedRoute) {
        // No token and trying to access protected route
        throw redirect(303, '/auth/login');
    }

    return await resolve(event);
}
