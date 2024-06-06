import type { RequestHandler } from './$types';

export const GET: RequestHandler = async () => {
    return new Response();
};

export async function _ocupacionBloque(edificio: string, planta: string) {
    return await fetch(`http://localhost:18080/api/ocupacionBloque/${edificio}/${planta}`);
}