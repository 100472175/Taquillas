import type { PageServerLoad, Actions} from './$types';
import size from '$lib/size';
import { prueba, reservaTaquilla } from '$lib/api_taquillas';


export const load: PageServerLoad = async () => {
	return {
		serverMessage: 'hello from server load function',
        size: size,
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
