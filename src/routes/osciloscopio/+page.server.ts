import type { PageServerLoad, Actions } from './$types';
import { BASE_URL_API, TOKEN } from '$lib/api_taquillas';

export const load: PageServerLoad = async ({ request }) => {
	const fetchDisponibilidadOsciloscopios = async () => {
		const res = await fetch(`${BASE_URL_API}/api/disponibilidadOsciloscopio${TOKEN}`);
		const data = await res.json();
		return data;
	}

	return {
        osciloscopio: fetchDisponibilidadOsciloscopios(),
	};
};
