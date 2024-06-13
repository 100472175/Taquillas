import type { RequestHandler } from './$types';
import { eliminaReserva } from '$lib/api_taquillas';
import {json} from '@sveltejs/kit';

export const POST: RequestHandler = async ({ request }) => {
	const input = await request.json();
    const { taquilla, email } = input;
    
    // Llama a la API de reserva de la base de datos:
    const result = eliminaReserva(taquilla, email);
    
    return json({'message': 'Reserva eliminada correctamente, success'});
	
    return result;
};