import type { PageServerLoad, Actions} from './$types';
import {addUserRol, BASE_URL_API} from '$lib/api_taquillas';
import { Session } from 'inspector';

export const load = (async (event) => {
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
	addUserRol: async ({ cookies, request }) => {
		const data = await request.formData();
		// -------- Aquí se llama a la función de la API que añade un rol a un usuario --------
		const nia = data.get('NIA_add');
		const rol = data.get('rol_add');
		const nia_admin = data.get('nia_admin');
		const nombre_admin = data.get('nombre_admin');

		const result = addUserRol(nia, rol, nia_admin, nombre_admin);
		return result;
	},
} satisfies Actions;