// +page.ts
import type { PageLoad } from './$types';
import { redirect } from '@sveltejs/kit';

export const load: PageLoad = async ({ parent, data }) => {
	const { session } = await parent();
	let authorizedEmails = data.authorizedEmails ?? [];

	if (authorizedEmails.includes(session?.user?.email) === -1 || !session?.user?.email || authorizedEmails.includes(session?.user?.email) === false) { 
		throw redirect(302, '/');
	}
	
	return {
		session: session,
		authorizedEmails: authorizedEmails
	};
};
