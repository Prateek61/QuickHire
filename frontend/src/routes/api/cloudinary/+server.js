import { CLOUDINARY_API_SECRET } from '$env/static/private';
import { v2 as cloudinary } from 'cloudinary';
import { error, json } from '@sveltejs/kit';

export async function POST() {
	try {
		const timestamp = Math.round(new Date().getTime() / 1000);
		const signature = cloudinary.utils.api_sign_request(
			{
				timestamp: timestamp
			},
			CLOUDINARY_API_SECRET
		);
		return json({ signature, timestamp });
	} catch (err) {
		return error(500, `${err}`);
	}
}
