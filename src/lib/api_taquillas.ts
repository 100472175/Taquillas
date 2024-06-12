export const BASE_URL_API = process.env.DESTINO_API ?? 'http://127.0.0.1:18080'
//const BASE_URL_API = 'https://et-emirates-springs-cinema.trycloudflare.com'


// POST /api/taquillas/reservar
export async function reservaTaquilla(taquilla: FormDataEntryValue | null | String, usuario: FormDataEntryValue | null | Number, correo: FormDataEntryValue | null | String, nombre: FormDataEntryValue | null | String) {
	// Llamada a la API de taquillas para reservar la taquill
	try {
		const response = await fetch(`${BASE_URL_API}/api/reservaTaquilla`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'Access-Control-Allow-Origin': '*'
			},
			body: JSON.stringify({
				taquilla: taquilla,
				usuario: usuario,
				correo: correo,
				nombre: nombre,
			})
		});

		if (response.ok) {
			const data = await response.json();
			return data;
		} else {
			console.error('Server response was not OK reservando taquilla', response.status, response.statusText);
		}
	} catch (error) {
		console.error('Error:', error);
	}

}


export async function prueba(taquilla: FormDataEntryValue | null, nia: FormDataEntryValue | null) {
	try {
		const options = {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'Access-Control-Allow-Origin': '*'
			},
			body: JSON.stringify({
				taquilla: taquilla,
				usuario: nia
			})
		};
		const response = await fetch(`${BASE_URL_API}/api/reservaTaquilla`, options);
		if (!response.ok) {
			throw new Error('Network response was not ok');
		}
		const data = await response.json();
		return data;
	} catch (error) {
		console.error('Error:', error);
	}	
}

export async function ocupacionBloque(edificio: String, planta: String) {
	try {
		const response = await fetch(`${BASE_URL_API}/api/ocupacionBloque/${edificio}/${planta}`);
		if (!response.ok) {
			throw new Error('Network response was not ok');
		}
		const data = await response.json();
		return data;
	} catch (error) {
		console.error('Error:', error);
	}
}

export async function addUserRol(nia: FormDataEntryValue | null | String, rol: FormDataEntryValue | null | String) {
	rol = rol?.toString().toLowerCase() || 'general';
	try {
		const response = await fetch(`${BASE_URL_API}/api/addUserRol`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'Access-Control-Allow-Origin': '*'
			},
			body: JSON.stringify({
				nia: nia,
				rol: rol,
			})
		});

		if (response.ok) {
			const data = await response.json();
			return data;
		} else {
			console.error('Server response was not OK añadiendo rol', response.status, response.statusText);
		}

	} catch (error) {
		console.error(error);
	}
} 


export async function add_user_db(email: String, name: String | null | undefined) {
	const nia = email.split('@')[0];
	try {
		const response = await fetch(`${BASE_URL_API}/api/createUser`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'Access-Control-Allow-Origin': '*'
			},
			body: JSON.stringify({
				nia: nia,
				email: email,
				name: name
			})
		});

		if (response.ok) {
			const data = await response.json();
			return data;
		} else {
			console.error('Server response was not OK add_user_db', response.status, response.statusText);
		}

	} catch (error) {
		console.error(error);
	}
}

export async function getReservasNia(nia: FormDataEntryValue | null | String) {
	try {
		const response = await fetch(`${BASE_URL_API}/api/getReservas/nia/${nia}`);
		if (response.ok) {
			const data = await response.json();
			return data;
		} else {
			console.error('Server response was not OK when consulting NIA', response.status, response.statusText);
		}
	
	} catch (error) {
		console.error(error);
	}
}

export async function getReservasTaquilla(taquilla: FormDataEntryValue | null | String) {
	try {
		const response = await fetch(`${BASE_URL_API}/api/getReservas/taquilla/${taquilla}`);
		if (response.ok) {
			const data = await response.json();
			return data;
		} else {
			console.error('Server response was not OK, when consulting taquilla', response.status, response.statusText);
		}
	
	} catch (error) {
		console.error(error);
	}
}
		

/*

// DELETE /api/taquillas/liberar
function liberarTaquilla(taquilla: String) {
	// Llamada a la API de taquillas para liberar la taquilla

	// Devolver la respuesta de la API
	return {
		taquilla: taquilla
	};
}

// GET /api/taquillas/usuario
function taquillasUsuario(usuario: Number) {
	// Llamada a la API de taquillas para obtener las taquillas reservadas por el usuario

	// Devolver la respuesta de la API
	return {
		usuario: 0
	};
}

// GET /api/taquillas/seccion
function taquillasLibresSeccion(edificio: String, planta: String, seccion: String) {
	// Llamada a la API de taquillas para obtener las taquillas libres de una sección

	// Devolver la respuesta de la API
	return [];
}

// GET /api/taquillas/libres
function numeroTaquillasLibres() {
	// Llamada a la API de taquillas para obtener las taquillas libres

	// Devolver la respuesta de la API
	return {
		libres: 0
	};
}

// GET /api/taquillas/ocupadas
function numeroTaquillasOcupadas() {
	// Llamada a la API de taquillas para obtener las taquillas ocupadas

	// Devolver la respuesta de la API
	return {
		ocupadas: 0
	};
}

// GET /api/taquillas/ocupacion-seccion
function ocupacionPorSección(edificio: String, planta: String, seccion: String) {
	// Llamada a la API de taquillas para obtener la ocupación por sección

	// Devolver la respuesta de la API
	return 0;
}

// GET /api/taquillas/status
function statusTaquilla(taquilla: String) {
	// Llamada a la API de taquillas para obtener el estado de una taquilla

	// Devolver la respuesta de la API
	return {
		taquilla: taquilla,
		ocupada: false
	};
}

// UPDATE /api/taquillas/modificar
function modificarDatosTaquilla(taquilla: String, datos: Object) {
	// Llamada a la API de taquillas para modificar los datos de una taquilla

	// Devolver la respuesta de la API
	return {
		taquilla: taquilla,
		datos: datos
	};
}

// UPDATE /api/taquillas/cambiar
function cambiarTaquilla(taquilla: String, nuevaTaquilla: String) {
	// Llamada a la API de taquillas para cambiar una taquilla por otra

	// Devolver la respuesta de la API
	return {
		taquilla: taquilla,
		nuevaTaquilla: nuevaTaquilla
	};
}
*/
//////////////////////