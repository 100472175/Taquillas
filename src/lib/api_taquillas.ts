// POST /api/taquillas/reservar
export async function reservaTaquilla(taquilla: String, usuario: Number) {
	// Llamada a la API de taquillas para reservar la taquilla

	try {
		const response = await fetch('http://127.0.0.1:18080/reservaTaquilla', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				taquilla: taquilla,
				usuario: usuario
			})
		});

		if (response.ok) {
			const data = await response.json();
			//console.log(data);
			return data;
		} else {
			console.error('Server response was not OK', response.status, response.statusText);
		}
	} catch (error) {
		console.error('Error:', error);
	}

	/*
   try {
    const response = await fetch('http://127.0.0.1:18080');
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    console.log(response);
    const data = await response.json();
    console.log(data);
    return data;
} catch (error) {
    console.error('Error:', error);
}
*/
}

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

//////////////////////

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
		const response = await fetch('http://127.0.0.1:18080/api/reservaTaquilla', options);
		if (!response.ok) {
			throw new Error('Network response was not ok');
		}
		const data = await response.json();
		return data;
	} catch (error) {
		console.error('Error:', error);
	}
}
