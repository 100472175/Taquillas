import type { PageLoad } from './$types';
import { error } from '@sveltejs/kit';


export const load = (({params}) => {
	if (!['1', '2', '4', '7'].includes(params.edificio)) {
		error(404, `Esta página no se ha podido encontrar: "${params.edificio}"`);
	}
	let imagenes: number[] = [];
	
	// Switch case para cargar las imágenes de los edificios
	switch (params.edificio) {
		case '1':
			imagenes = [0, 1]
			break;
		case '2':
			imagenes = [2, 3]
			break;
		case '4':
			imagenes = [0, 1, 2]
			break;
		case '7':
			imagenes = [0, 1, 2]
			break;
		default:
			imagenes = []
			break;
	}

	return {
			edificio: params.edificio,
			pisos: imagenes,
	};
}) satisfies PageLoad;
