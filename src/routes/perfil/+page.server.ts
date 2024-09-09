import type { PageServerLoad, Actions} from './$types';
import {getReservasNia, BASE_URL_API, TOKEN} from '$lib/api_taquillas';

export const load = (async (event) => {
    const fetchReservas = async (nia, nombre) => {
		const res = await fetch(`${BASE_URL_API}/api/getReservas/perfil/${nia}/${nombre}${TOKEN}`);
		const data = await res.json();
		return data;
	};

	let session = await event.locals.auth();
	let nia = session?.user?.email?.split('@')[0];
	let nombre = session?.user?.name;
	
	let reserva = null;
	
	if (session?.user?.email?.endsWith("@alumnos.uc3m.es")) {
		reserva = await fetchReservas(nia, nombre);
	}
	else if (session?.user?.email?.endsWith("uc3m.es")) {
		reserva = await fetchReservas(0, nombre);
	}

	if (reserva == null) {
		reserva = []
	}

	return {
		reservas: reserva,
	};
}) satisfies PageServerLoad;

export const actions = {
	
} satisfies Actions;