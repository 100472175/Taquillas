// +page.ts
import type { PageLoad } from './$types';
import { redirect } from '@sveltejs/kit';

// Lo bueno sería cargar esto de la base de datos, pero de momento va bien aqui

export const load: PageLoad = async ({ parent, data }) => {
	const { session } = await parent();

	let authorizedEmailsDespacho = data.authorizedEmailsTaquillasDespacho ?? [];
	let authorizedEmailsEscuela = data.authorizedEmailsTaquillasEscuela ?? [];
	let tablaPablo = data.tablaPablo ?? [{
			nombre: "No se ha ",
			nia: "Podido encontrar",
			taquilla: "ninguna taquilla.",
			codigo: "La base está al",
			fecha: 100000000,
			status: "% de su capacidad.",
		}];

	if ((authorizedEmailsDespacho.includes(session?.user?.email) === -1 && authorizedEmailsEscuela.includes(session?.user?.email) === -1) || !session?.user?.email || (authorizedEmailsDespacho.includes(session?.user?.email) === false && authorizedEmailsEscuela.includes(session?.user?.email) === false)) { 
		throw redirect(302, '/');
	}

	let asociaciones = data.asociaciones ?? [];
	
	return {
		session: session,
		authorizedEmailsDespacho: authorizedEmailsDespacho,
		authorizedEmailsEscuela: authorizedEmailsEscuela,
		tablaPablo : tablaPablo,
		asociaciones: asociaciones,
	};
};
