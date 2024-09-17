import type { RequestHandler } from './$types';
import { unbanUser } from '$lib/api_taquillas';
import {json} from '@sveltejs/kit';

export const POST: RequestHandler = async ({ request }) => {
	const input = await request.json();
    const { user, email } = input;
    
    // Llama a la API de reserva de la base de datos:
    const result = await unbanUser(user, email);
    	
    return json({result: result});
};