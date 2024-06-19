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

export async function addUserRol(nia: FormDataEntryValue | null | String, rol: FormDataEntryValue | null | String, nia_delegado: String, nombre: String) {
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
	
export async function aceptaReserva(taquilla: FormDataEntryValue | null | String, responsable: FormDataEntryValue | null | String){
	const taquilla_res = taquilla || '';
	let responsable_res = responsable || '';
	if (taquilla_res === '' || responsable_res === '') {
		return JSON.stringify({status: 'Error, datos incompletos'});
	}

	responsable_res = responsable_res.toString().split('@')[0];

	try {
		const response = await fetch(`${BASE_URL_API}/api/aceptaReserva`, {
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
		const response = await fetch(`${BASE_URL_API}/api/eliminaReserva`, {
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
		console.log('email:', email);
		const response = await fetch(`${BASE_URL_API}/api/backupDB`, {
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
			console.log(data);
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
		console.log('email:', email);
		const response = await fetch(`${BASE_URL_API}/api/deleteDB`, {
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
