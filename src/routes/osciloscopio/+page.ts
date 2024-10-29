import type { PageLoad } from './$types';

import { redirect } from '@sveltejs/kit';

export const load: PageLoad = async ({ parent, data }) => {
	const { session } = await parent();
	if (!session?.user?.email?.endsWith('@alumnos.uc3m.es')) { 
		throw redirect(302, '/');
	}

	return {
        osciloscopio: data.osciloscopio,
	};	
};
