// +page.ts
import type { PageLoad } from './$types';
import { redirect } from '@sveltejs/kit';

// Lo bueno sería cargar esto de la base de datos, pero de momento va bien aqui

export const load: PageLoad = async ({ parent, data }) => {
	const { session } = await parent();

	let authorizedEmails = data.authorizedEmails ?? [];
	let tablaPablo = data.tablaPablo ?? [{
			nombre: "No se ha ",
			nia: "Podido encontrar",
			taquilla: "ninguna taquilla.",
			codigo: "La base está al",
			fecha: 100000000,
			status: "% de su capacidad.",
		}];

	if (authorizedEmails.includes(session?.user?.email) === -1 || !session?.user?.email || authorizedEmails.includes(session?.user?.email) === false) { 
		throw redirect(302, '/');
	}
	
	return {
		session: session,
		authorizedEmails: authorizedEmails,
		tablaPablo : tablaPablo
	};
};
