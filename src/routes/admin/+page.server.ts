import type { PageServerLoad, Actions} from './$types';
import {addUserRol, BASE_URL_API} from '$lib/api_taquillas';

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
	addUserRol: async ({ cookies, request }) => {
		const data = await request.formData();
		// -------- Aquí se llama a la función de la API que añade un rol a un usuario --------
		const nia = data.get('NIA_add');
		const rol = data.get('rol_add');
		const result = addUserRol(nia, rol, "1", "A");
		return result;
	},
} satisfies Actions;