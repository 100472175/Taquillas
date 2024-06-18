import {json} from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { aceptaReserva } from '$lib/api_taquillas';

export const POST: RequestHandler = async ({ request }) => {
	const input = await request.json();
    const { taquilla, email } = input;
    
    // Llama a la API de reserva de la base de datos:
    const result = await aceptaReserva(taquilla, email);

    return json({result: result});
};