import type { RequestHandler } from './$types';
import { BASE_URL_API, TOKEN } from '$lib/api_taquillas';


export const GET: RequestHandler = async () => {
    return new Response();
};

export async function _ocupacionOsciloscopio(puesto: string) {
    return await fetch(`${BASE_URL_API}/api/ocupacionOsciloscopio/${puesto}${TOKEN}`);
}