import { signOut } from '@auth/sveltekit/client';
import type { LayoutServerLoad } from './$types';
import { BASE_URL_API, add_user_db } from '$lib/api_taquillas';

// load serverside data
export const load: LayoutServerLoad = async (event) => {
	const fetchAuthorizedEmails = async () => {
		const res = await fetch(`${BASE_URL_API}/api/authorizedEmails/escuela`);
		const data = await res.json();
		return data;
	};

	let session = await event.locals.auth();
	//console.log(session);

	// Store the user in the Database using the api
	if (session?.user?.email?.endsWith('uc3m.es')){
		add_user_db(session?.user?.email, session?.user?.name);
	}


	return {
		session: session,
		authorizedEmailsLayout: await fetchAuthorizedEmails()
	};
};


export const _check_user: LayoutServerLoad = async ({ email }) => {
	if (email_list.includes(email)) {
		return {
			status: 200
		};
	} else {
		return {
			status: 401
		};
	}
};
