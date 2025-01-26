import { redirect } from '@sveltejs/kit';

export const actions = {
    register: async ({ locals, request }) => {
        const formData = await request.formData();
        const data = Object.fromEntries(formData);

        console.log(data);

        try {
            const newUser = await locals.pb.collection('users').create(data);

            const { token, user } = await locals.pb.collection('users').authWithPassword(data.email, data.password);

            const updatedProfile = await locals.pb.collection('profiles').update(user.profile.id, {
                name: data.name
            });

            locals.pb.authStore.save(token, user);

            // Redirect to the professionals page after successful registration
            throw redirect(303, '/professionals');
        } catch (error) {
            console.error(error);
            return {
                error: true,
                message: error.message
            };
        }
    }
};