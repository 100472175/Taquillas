import type { PageServerLoad, Actions} from './$types';
import { BASE_URL_API, reservaOsciloscopio, TOKEN} from '$lib/api_taquillas';

export const load: PageServerLoad = async ({ request }) => {
	const split_url = request.url.split('/').filter((element) => (element.length <= 2 && element.length >= 1));
	split_url.map((url) => url.replace('?', ''));
	const puesto = split_url[0];

	const fetchOcupacionOsciloscopios = async () => {
		const res = await fetch(`${BASE_URL_API}/api/ocupacionOsciloscopio/${puesto}${TOKEN}`);
		const data = await res.json();
		return data;
	}

	const fetchPlantilla = async () => {
		const res = await fetch(`${BASE_URL_API}/api/plantilla${TOKEN}`);
		const data = await res.json();
		return data;
	}

	return {
		puesto: puesto,
        reservas: fetchOcupacionOsciloscopios(),
		plantilla: await fetchPlantilla(),
	};
};


export const actions = {
	registerOsciloscopio: async ({ cookies, request }) => {
		const data = await request.formData();
		const puesto = data.get('puesto');
		const nia = data.get('nia');
		const hora = parseInt(data?.get('hora').split(':')[0]);
		const dia = data.get('dia');
		const correo = data.get('correo');
		const nombre = data.get('nombre');
		const semana = data.get('semana');
		const result = reservaOsciloscopio(puesto, nia, hora, dia, correo, nombre, semana);
		return result;
	},
} satisfies Actions;
