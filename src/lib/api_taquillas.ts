export const BASE_URL_API = process.env.DESTINO_API ?? 'http://127.0.0.1:8502'
export const TOKEN = process.env.TOKEN_API ?? 'noup-casi';

//const BASE_URL_API = 'https://et-emirates-springs-cinema.trycloudflare.com'


// POST /api/taquillas/reservar
export async function reservaTaquilla(taquilla: FormDataEntryValue | null | String, usuario: FormDataEntryValue | null | Number, correo: FormDataEntryValue | null | String, nombre: FormDataEntryValue | null | String) {
	// Llamada a la API de taquillas para reservar la taquill
	try {
		const response = await fetch(`${BASE_URL_API}/api/reservaTaquilla${TOKEN}`, {
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

export async function reservaTaquillaAsociacion(taquilla: FormDataEntryValue | null | String, correo: FormDataEntryValue | null | String, nombre: FormDataEntryValue | null | String) {
	// Llamada a la API de taquillas para reservar la taquill
	try {
		const response = await fetch(`${BASE_URL_API}/api/reservaTaquillaAsociacion${TOKEN}`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'Access-Control-Allow-Origin': '*'
			},
			body: JSON.stringify({
				taquilla: taquilla,
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
		const response = await fetch(`${BASE_URL_API}/api/reservaTaquilla${TOKEN}`, options);
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
		const response = await fetch(`${BASE_URL_API}/api/ocupacionBloque/${edificio}/${planta}${TOKEN}`);
		if (!response.ok) {
			throw new Error('Network response was not ok');
		}
		const data = await response.json();
		return data;
	} catch (error) {
		console.error('Error:', error);
	}
}

export async function addUserRol(nia: FormDataEntryValue | null | String, rol: FormDataEntryValue | null | String, nia_delegado: String, nombre: String) {
	rol = rol?.toString().toLowerCase() || 'general';
	try {
		const response = await fetch(`${BASE_URL_API}/api/addUserRol${TOKEN}`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'Access-Control-Allow-Origin': '*'
			},
			body: JSON.stringify({
				nia: nia,
				rol: rol,
				nia_delegado: nia_delegado,
				nombre: nombre
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
		const response = await fetch(`${BASE_URL_API}/api/createUser${TOKEN}`, {
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

export async function add_association_db(email: String, name: String | null | undefined) {
	try {
		const response = await fetch(`${BASE_URL_API}/api/createAssociation${TOKEN}`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'Access-Control-Allow-Origin': '*'
			},
			body: JSON.stringify({
				email: email,
				name: name
			})
		});

		if (response.ok) {
			const data = await response.json();
			return data;
		} else {
			console.error('Server response was not OK add_association_db', response.status, response.statusText);
		}

	} catch (error) {
		console.error(error);
	}
}

export async function getReservasNia(nia: FormDataEntryValue | null | String) {
	try {
		const response = await fetch(`${BASE_URL_API}/api/getReservas/nia/${nia}${TOKEN}`);
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
		const response = await fetch(`${BASE_URL_API}/api/getReservas/taquilla/${taquilla}${TOKEN}`);
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
	
export async function aceptaReserva(taquilla: FormDataEntryValue | null | String, responsable: FormDataEntryValue | null | String){
	const taquilla_res = taquilla || '';
	let responsable_res = responsable || '';
	if (taquilla_res === '' || responsable_res === '') {
		return JSON.stringify({status: 'Error, datos incompletos'});
	}

	responsable_res = responsable_res.toString().split('@')[0];

	try {
		const response = await fetch(`${BASE_URL_API}/api/aceptaReserva${TOKEN}`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'Access-Control-Allow-Origin': '*'
			},
			body: JSON.stringify({
				taquilla: taquilla_res,
				responsable: responsable_res
			})
		});

		if (response.ok) {
			const data = await response.json();
			return data;
		} else {
			console.error('Server response was not OK aceptando reserva', response.status, response.statusText);
		}

	} catch (error) {
		console.error(error);
	}
	
}

export async function eliminaReserva(taquilla: FormDataEntryValue | null | String, responsable: FormDataEntryValue | null | String){
	const taquilla_res = taquilla || '';
	let responsable_res = responsable || '';
	if (taquilla_res === '' || responsable_res === '') {
		return JSON.stringify({status: 'Error, datos incompletos'});
	}

	responsable_res = responsable_res.toString().split('@')[0];

	try {
		const response = await fetch(`${BASE_URL_API}/api/eliminaReserva${TOKEN}`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'Access-Control-Allow-Origin': '*'
			},
			body: JSON.stringify({
				taquilla: taquilla_res,
				responsable: responsable_res
			})
		});

		if (response.ok) {
			const data = await response.json();
			return data;
		} else {
			console.error('Server response was not OK aceptando reserva', response.status, response.statusText);
		}

	} catch (error) {
		console.error(error);
	}
	
}

export async function backupDB(email: FormDataEntryValue | null | String) {
	try {
		const response = await fetch(`${BASE_URL_API}/api/backupDB${TOKEN}`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'Access-Control-Allow-Origin': '*'
			},
			body: JSON.stringify({
				email: email
			})
		
		});
		if (response.ok) {
			const data = await response.json();
			return data;
		} else {
			console.error('Server response was not OK when backing up DB', response.status, response.statusText);
		}
	
	} catch (error) {
		console.error(error);
	}
}

export async function deleteDB(email: FormDataEntryValue | null | String) {
	try {
		const response = await fetch(`${BASE_URL_API}/api/deleteDB${TOKEN}`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'Access-Control-Allow-Origin': '*'
			},
			body: JSON.stringify({
				email: email,
			})
		
		});
		if (response.ok) {
			const data = await response.json();
			return data;
		} else {
			console.error('Server response was not OK when deleting DB', response.status, response.statusText);
		}
	
	} catch (error) {
		console.error(error);
	}
}


export async function marcarRota(taquilla: FormDataEntryValue | null | String, correo: FormDataEntryValue | null | String) {
	try {
		const response = await fetch(`${BASE_URL_API}/api/marcarRota${TOKEN}`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'Access-Control-Allow-Origin': '*'
			},
			body: JSON.stringify({
				taquilla: taquilla,
				correo: correo,
			})
		});

		if (response.ok) {
			const data = await response.json();
			return data;
		} else {
			console.error('Server response was not OK when marking rota', response.status, response.statusText);
		}

	} catch (error) {
		console.error(error);
	}
}

export async function arreglarTaquilla(taquilla: FormDataEntryValue | null | String, correo: FormDataEntryValue | null | String) {
	try {
		const response = await fetch(`${BASE_URL_API}/api/arreglarTaquilla${TOKEN}`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'Access-Control-Allow-Origin': '*'
			},
			body: JSON.stringify({
				taquilla: taquilla,
				correo: correo,
			})
		});

		if (response.ok) {
			const data = await response.json();
			return data;
		} else {
			console.error('Server response was not OK when marking rota', response.status, response.statusText);
		}

	} catch (error) {
		console.error(error);
	}
}