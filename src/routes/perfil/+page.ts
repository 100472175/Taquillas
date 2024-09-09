// +page.ts
import type { PageLoad } from './$types';
import { redirect } from '@sveltejs/kit';

// Lo bueno sería cargar esto de la base de datos, pero de momento va bien aqui

export const load: PageLoad = async ({ parent, data }) => {
	const { session } = await parent();
	let reservas = data.reservas ?? [];
	
	return {
		reservas: reservas,
	}
};
