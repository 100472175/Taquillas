import type { PageLoad } from './$types';
import { error } from '@sveltejs/kit';

// Page sizes 

export const load = (({params, data}) => {
	if (!['1', '2', '3'].includes(params.puesto)) {
		error(404, `Esta página no se ha podido encontrar el puesto: "${params.puesto}"`);
	}

	let plantilla = data.plantilla ?? {"plantilla": {}};

	return {
		puesto: data.puesto,
		reservas: data.reservas,	
		plantilla: plantilla
	};
}) satisfies PageLoad;

export function _handleResult(result: any) {
	const code = result.status;
	const body = result.body;

	if (code === 200) {
		alert('Puesto reservado correctamente');
	} else {
		alert('Error al reservar el puesto');
	}
}