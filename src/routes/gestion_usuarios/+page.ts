// +page.ts
import type { PageLoad } from './$types';
import { redirect } from '@sveltejs/kit';

// Lo bueno sería cargar esto de la base de datos, pero de momento va bien aqui
let despacho_list = ['100472175'];

export const load: PageLoad = async ({ parent }) => {
	const { session } = await parent();
	/*
    // Check if the user is not logged in
    if (!session?.user?.email) {
        // Redirect to the homepage
        throw redirect(302, '/');
    }*/

	if (
		!despacho_list.includes(session?.user?.email.substring(0, session?.user?.email.indexOf('@')))
	) {
		// Redirect to the homepage
		throw redirect(302, '/');
	}
	return {
		session
	};
};
