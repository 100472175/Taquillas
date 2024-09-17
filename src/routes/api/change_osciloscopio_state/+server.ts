import type { RequestHandler } from './$types';
import { changeOsciloscopioState } from '$lib/api_taquillas';
import {json} from '@sveltejs/kit';

export const POST: RequestHandler = async ({ request }) => {
	const input = await request.json();
    const { email, puesto, estado } = input;
    
    // Llama a la API de reserva de la base de datos:
    const result = await changeOsciloscopioState(email, puesto, estado);
    	
    return json({result: result});
};

