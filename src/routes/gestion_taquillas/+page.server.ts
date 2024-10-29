import type { PageServerLoad, Actions} from './$types';
import {getReservasNia, getReservasTaquilla, reservaTaquilla, reservaTaquillaAsociacion, marcarRota, arreglarTaquilla, BASE_URL_API, TOKEN} from '$lib/api_taquillas';

export const load = (async () => {
    const fetchAuthorizedEmails = async (rango:String) => {
		const res = await fetch(`${BASE_URL_API}/api/authorizedEmails/${rango}${TOKEN}`);
		const data = await res.json();
		return data;
	};

	const fetchTablaPablo = async () => {
		const res = await fetch(`${BASE_URL_API}/api/tablaPablo${TOKEN}`);
		const data = await res.json();
		return data;
	};

	const fetchAsociaciones = async () => {
		const res = await fetch(`${BASE_URL_API}/api/getAsociaciones${TOKEN}`);
		const data = await res.json();
		return data;
	};

	let emailsDespacho = await fetchAuthorizedEmails('atencion');
	if (emailsDespacho === null) {
		emailsDespacho = [];
	}
	let emailsEscuela = await fetchAuthorizedEmails('escuela');
	if (emailsEscuela === null) {
		emailsEscuela = [];
	}
	emailsDespacho = emailsDespacho.concat(emailsEscuela);
	// remove null values
	emailsDespacho = emailsDespacho.filter((email: String) => email !== null);

    return {
        authorizedEmailsTaquillasEscuela: emailsEscuela,
		authorizedEmailsTaquillasDespacho: emailsDespacho,
		tablaPablo: await fetchTablaPablo(),
		asociaciones: await fetchAsociaciones(),
    };
}) satisfies PageServerLoad;


export const actions = {
	busquedaNia: async ({ cookies, request }) => {
		const data = await request.formData();
		// -------- Aquí se llama a la función de la API que busca las taquillas asociadas a un NIA --------
		const nia = data.get('NIA_s');
		const result = getReservasNia(nia);
		return result;
	},
	busquedaTaquilla: async ({ cookies, request }) => {
		const data = await request.formData();
		// -------- Aquí se llama a la función de la API que busca el estado de una Taquilla --------
		const taquilla = data.get('Taquilla_s');
		const result = getReservasTaquilla(taquilla);
		return result;
	},
	registerTaquilla: async ({ cookies, request }) => {
		const data = await request.formData();
		const taquilla = data.get('taquilla');
		const nia = data.get('nia');
		const correo = nia + "@alumnos.uc3m.es";
		const nombre = data.get('nombre');
		const result = reservaTaquilla(taquilla, nia, correo, nombre);
		return result;
	},
	registerTaquillaAssociation: async ({ cookies, request }) => {
		const data = await request.formData();
		const taquilla = data.get('taquilla');
		const correo = data.get('correo');
		const nombre = data.get('nombre');
		const result = reservaTaquillaAsociacion(taquilla, correo, nombre);
		return result;
	},
	setRota: async ({ request }) => {
		const data = await request.formData();
		const taquilla = data.get('taquilla');
		const correo = data.get('correo');
		const result = marcarRota(taquilla, correo);
		return result;
	},
	fixTaquilla: async ({ request }) => {
		const data = await request.formData();
		const taquilla = data.get('taquilla');
		const correo = data.get('correo');
		const result = arreglarTaquilla(taquilla, correo);
		return result;
	}
} satisfies Actions;