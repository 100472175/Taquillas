import type { PageServerLoad, Actions} from './$types';
import {addUserRol, backupDB, deleteDB, BASE_URL_API} from '$lib/api_taquillas';

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
	addUserRol: async ({ request }) => {
		const data = await request.formData();
		// -------- Aquí se llama a la función de la API que añade un rol a un usuario --------
		const nia = data.get('NIA_add');
		const rol = data.get('rol_add');
		const nia_admin = data.get('nia_admin');
		const nombre_admin = data.get('nombre_admin');

		const result = addUserRol(nia, rol, nia_admin, nombre_admin);
		return result;
	},
	BackupDB: async ({ request }) => {
		const data = await request.formData();
		// -------- Aquí se llama a la función de la API que añade un rol a un usuario --------
		const email_admin = data.get('email_admin');
		console.log('email_admin:', email_admin);
		const result = backupDB(email_admin);

		return result;
	},
	DeleteDB : async ({ request }) => {
		const data = await request.formData();
		// -------- Aquí se llama a la función de la API que añade un rol a un usuario --------
		const email_admin = data.get('email_admin');
		const result = deleteDB(email_admin);
		return result;
	}

} satisfies Actions;