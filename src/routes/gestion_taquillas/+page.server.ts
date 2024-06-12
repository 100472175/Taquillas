import type { PageServerLoad, Actions} from './$types';
import {getReservasNia, getReservasTaquilla, BASE_URL_API} from '$lib/api_taquillas';

export const load = (async () => {
    const fetchAuthorizedEmails = async () => {
		const res = await fetch(`${BASE_URL_API}/api/authorizedEmails/escuela`);
		const data = await res.json();
		return data;
	};

    return {
        authorizedEmails: await fetchAuthorizedEmails(),
    };
}) satisfies PageServerLoad;


export const actions = {
	busquedaNia: async ({ cookies, request }) => {
		const data = await request.formData();
		// -------- Aquí se llama a la función de la API que añade un rol a un usuario --------
		const nia = data.get('NIA_s');
		const result = getReservasNia(nia);
		return result;
	},
	busquedaTaquilla: async ({ cookies, request }) => {
		const data = await request.formData();
		// -------- Aquí se llama a la función de la API que añade un rol a un usuario --------
		const taquilla = data.get('Taquilla_s');
		const result = getReservasTaquilla(taquilla);
		return result;
	},
} satisfies Actions;