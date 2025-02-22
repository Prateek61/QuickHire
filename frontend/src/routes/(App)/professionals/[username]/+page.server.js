import { redirect } from '@sveltejs/kit';
import { PUBLIC_API_URL } from '$env/static/public';

/** @type {import('./$types').PageLoad} */
export const load = async ({ params, fetch }) => {
	return {
		props: {
			ok: true,
			reviews: [
				{
					id: 0,
					hire_id: 0,
					rating: 0,
					reviewer_name: 'string',
					reviewer_profile_pic: 'string',
					review: 'string'
				}
			],
			professional: {
				professional: {
					user_id: 1,
					skill_id: 3,
					title: 'Senior Non-Sleeper',
					experience: 3,
					hourly_rate: '42',
					location: 'Remote',
					id: 1,
					cover_letter: 'hmm',
					is_available: true,
					updated_at: '2025-02-22T15:29:43.216737',
					created_at: '2025-02-22T15:29:43.216737'
				},
				user: {
					username: 'Prateek',
					email: 'prateekpoudel61@gmail',
					phone_no: '9841234567',
					password_hash: null,
					id: 1,
					first_name: 'Prateek',
					last_name: 'Poudel',
					profile_pic_url: null,
					is_active: true,
					birthday: null,
					last_login: '2025-02-22T15:29:43.197570',
					updated_at: '2025-02-22T15:29:43.197570',
					created_at: '2025-02-22T15:29:43.197570'
				},
				skill: {
					name: 'Sleepdeprivation',
					id: 3,
					description: 'Professional all-nighter'
				}
			}
		}
		// try {
		// 	const url = `${PUBLIC_API_URL}/professionals/${params.username}`;
		// 	const response = await fetch(url, {
		// 		method: 'GET',
		// 		headers: {
		// 			'Content-Type': 'application/json'
		// 		},
		// 		credentials: 'include'
		// 	});
		// 	if (!response.ok) {
		// 		const error = await response.json();
		// 		throw redirect(302, '/');
		// 	}
		// 	const professional = await response.json();
		// 	const reviewsresponse = await fetch(
		// 		`${PUBLIC_API_URL}/reviews/professionals/${professional.professional.id}`,
		// 		{
		// 			method: 'GET',
		// 			headers: {
		// 				'Content-Type': 'application/json'
		// 			},
		// 			credentials: 'include'
		// 		}
		// 	);
		// 	if (!reviewsresponse.ok) {
		// 		console.log('error');
		// 		const error = await reviewsresponse.json();
		// 		throw new Error(error.detail || 'Failed to fetch reviews');
		// 	}
		// 	const reviews = await reviewsresponse.json();
		// 	// const reviews = [];
		// 	return {
		// 		props: {
		// 			ok: true,
		// 			professional,
		// 			reviews
		// 		}
		// 	};
		// } catch (error) {
		// 	// throw redirect(302, '/');
		// 	console.error(error);
		// 	return {
		// 		props: {
		// 			ok: false,
		// 			error: error.message
		// 		}
		// 	};
		// }
	};
};
