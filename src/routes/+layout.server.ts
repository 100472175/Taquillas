import type { LayoutServerLoad } from './$types';
import { BASE_URL_API, TOKEN, add_user_db, add_association_db } from '$lib/api_taquillas';

// load serverside data
export const load: LayoutServerLoad = async (event) => {
	const fetchAuthorizedEmails = async (rango: String) => {
		const res = await fetch(`${BASE_URL_API}/api/authorizedEmails/${rango}${TOKEN}`);
		const data = await res.json();
		return data;
	};

	let session = await event.locals.auth();

	// Store the user in the Database using the api
	if (session?.user?.email?.endsWith('@alumnos.uc3m.es')){
		add_user_db(session?.user?.email, session?.user?.name);
	}
	else if (session?.user?.email?.endsWith('uc3m.es')) {
		add_association_db(session?.user?.email, session?.user.name);
	}	

	let emailsDespacho = await fetchAuthorizedEmails('atencion');
	if (emailsDespacho === null) {
		emailsDespacho = [];
	}
	let emailsEscuela = await fetchAuthorizedEmails('escuela');
	if (emailsEscuela === null) {
		emailsEscuela = [];
	}

	emailsDespacho = emailsDespacho.concat(emailsEscuela);
	// remove null values
	emailsDespacho = emailsDespacho.filter((email: String) => email !== null);

	return {
		session: session,
		authorizedEmailsLayoutEscuela: emailsEscuela,
		authorizedEmailsLayoutDespacho: emailsDespacho,
	};
};

