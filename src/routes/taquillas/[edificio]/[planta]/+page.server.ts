import type { PageServerLoad, Actions} from './$types';
import size from '$lib/size';
import { prueba, reservaTaquilla, ocupacionBloque } from '$lib/api_taquillas';


export const load: PageServerLoad = async ({ request }) => {
	const [edificio, planta] = request.url.split('/').filter((element) => element.length == 1);
	return {
		serverMessage: 'hello from server load function',
        size: size,
		bloques: ocupacionBloque(edificio, planta).then((data) => {data}),
	};
};


export const actions = {
	registerTaquilla: async ({ cookies, request }) => {
		console.log('registerTaquilla ha sido invocado');
		const data = await request.formData();
		const taquilla = data.get('taquilla');
		const nia = data.get('nia');
		const result = prueba(taquilla, nia);
		return result;
	},
} satisfies Actions;
