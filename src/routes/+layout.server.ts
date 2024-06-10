import { signOut } from '@auth/sveltekit/client';
import type { LayoutServerLoad } from './$types';

// load serverside data
export const load: LayoutServerLoad = async (event) => {
	const fetchAuthorizedEmails = async () => {
		const res = await fetch('http://localhost:18080/api/authorizedEmails');
		const data = await res.json();
		return data;
	};

	let session = await event.locals.auth();
	//console.log(session);

	// Store the user in the Database using the api
	// TODO


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
