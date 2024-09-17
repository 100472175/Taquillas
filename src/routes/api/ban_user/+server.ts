import type { RequestHandler } from './$types';
import { banUser } from '$lib/api_taquillas';
import {json} from '@sveltejs/kit';

export const POST: RequestHandler = async ({ request }) => {
	const input = await request.json();
    const { user, dias, email } = input;
    
    // Llama a la API de reserva de la base de datos:
    const result = await banUser(user, dias, email);
    	
    return json({result: result});
};