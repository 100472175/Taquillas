import type { RequestHandler } from './$types';
import { BASE_URL_API } from '$lib/api_taquillas';


export const GET: RequestHandler = async () => {
    return new Response();
};

export async function _ocupacionBloque(edificio: string, planta: string) {
    return await fetch(`${BASE_URL_API}/api/ocupacionBloque/${edificio}/${planta}`);
}