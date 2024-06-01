import type { PageLoad } from './$types';
import { error } from '@sveltejs/kit';


export const load = (({params}) => {
	if (!['1', '2', '4', '7'].includes(params.edificio)) {
		error(404, `Esta página no se ha podido encontrar: "${params.edificio}"`);
	}
	return {
			edificio: params.edificio
	};
}) satisfies PageLoad;
