import type { RequestHandler } from './$types';
import { changeHoraState } from '$lib/api_taquillas';
import {json} from '@sveltejs/kit';

export const POST: RequestHandler = async ({ request }) => {
	const input = await request.json();
    const { email, dia, hora, estado } = input;
    
    // Llama a la API de reserva de la base de datos:
    const result = await changeHoraState(email, dia, hora, estado);
    	
    return json({result: result});
};