import type { PageLoad } from './$types';
import { error } from '@sveltejs/kit';

// Page sizes 

export const load = (({params, data}) => {
	if (!['0', '1', '2', '3'].includes(params.planta)) {
		error(404, `Esta página no se ha podido encontrar la planta: "${params.planta}"`);
	}
	return {
			size: data.size,
			planta: params.planta,
            edificio: params.edificio,
			bloques: data.bloques,
	};
}) satisfies PageLoad;

export function _handleResult(result: any) {
	const code = result.status;
	const body = result.body;

	if (code === 200) {
		alert('Taquilla reservada correctamente');
	} else {
		alert('Error al reservar la taquilla');
	}
}