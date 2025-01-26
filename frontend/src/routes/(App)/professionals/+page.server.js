import PocketBase from 'pocketbase';
import { redirect } from '@sveltejs/kit';

export async function load() {
    const pb = new PocketBase('http://localhost:8090');

    try {
        const results = await pb.collection('professional').getFullList({
            expand: 'user,skill'
        });

        let professionals_list = [];

        // loop through the results and format the data
        for (let result of results) {
            // console.log('result:', result); // Log the result to check the structure
            // console.log('expanded user:', result.expand.user); // Log the expanded user field

            let professional = {
                id: result.id,
                name: result.expand.user ? result.expand.user.name : 'Unknown', // Check if user is expanded
                skill: result.expand.skill ? result.expand.skill.name : 'Unknown', // Check if skill is expanded
                hourly_rate: result.hourly_rate,
                experience: result.experience,
            };

            professionals_list.push(professional);
        }

        return {
            professionals: professionals_list
        };
    } catch (error) {
        console.error(error);
        return {
            error: error.message
        };
    }
}