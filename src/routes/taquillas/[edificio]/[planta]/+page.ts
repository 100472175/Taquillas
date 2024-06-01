import type { PageLoad } from './$types';
import { error } from '@sveltejs/kit';


export const load = (({params}) => {
	if (!['0', '1', '2', '3'].includes(params.planta)) {
		error(404, `Esta página no se ha podido encontrar la planta: "${params.planta}"`);
	}
	return {
			planta: params.planta,
            edificio: params.edificio,
	};
}) satisfies PageLoad;
