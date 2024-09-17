// +page.ts
import type { PageLoad } from './$types';
import { redirect } from '@sveltejs/kit';

export const load: PageLoad = async ({ parent, data }) => {
	const { session } = await parent();
	let authorizedEmails = data.authorizedEmails ?? [];
	let users = data.users ?? [{
		nombre: "No se ha",
		nia: "podido encontrar",
		correo: "ninguna",
		rango: "persona.",
	}];
	let plantilla = data.plantilla ?? {"plantilla": {}};


	if (authorizedEmails.includes(session?.user?.email) === -1 || !session?.user?.email || authorizedEmails.includes(session?.user?.email) === false) { 
		throw redirect(302, '/');
	}
	
	return {
		session: session,
		authorizedEmails: authorizedEmails,
		users: users,
		plantilla: plantilla
	};
};
