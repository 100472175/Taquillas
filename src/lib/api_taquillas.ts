// POST /api/taquillas/reservar
function reservaTaquilla(taquilla: String, usuario: Number) {
    // Llamada a la API de taquillas para reservar la taquilla

    // Devolver la respuesta de la API
    return {
        taquilla: taquilla,
        usuario: usuario,
    }
}

// DELETE /api/taquillas/liberar
function liberarTaquilla(taquilla: String) {
    // Llamada a la API de taquillas para liberar la taquilla

    // Devolver la respuesta de la API
    return {
        taquilla: taquilla,
    }
}

// GET /api/taquillas/usuario
function taquillasUsuario(usuario: Number) {
    // Llamada a la API de taquillas para obtener las taquillas reservadas por el usuario

    // Devolver la respuesta de la API
    return {
        usuario: 0,
    }
}

// GET /api/taquillas/seccion
function taquillasLibresSeccion(edificio: String, planta: String, seccion: String) {
    // Llamada a la API de taquillas para obtener las taquillas libres de una sección

    // Devolver la respuesta de la API
    return []
}

//GET /api/taquillas/libres
function numeroTaquillasLibres() {
    // Llamada a la API de taquillas para obtener las taquillas libres

    // Devolver la respuesta de la API
    return {
        libres: 0,
    }
}

//GET /api/taquillas/ocupadas
function numeroTaquillasOcupadas() {
    // Llamada a la API de taquillas para obtener las taquillas ocupadas

    // Devolver la respuesta de la API
    return {
        ocupadas: 0,
    }
}

//GET /api/taquillas/ocupacion-seccion
function ocupacionPorSección(edificio: String, planta: String, seccion: String) {
    // Llamada a la API de taquillas para obtener la ocupación por sección

    // Devolver la respuesta de la API
    return 0
}

//GET /api/taquillas/status
function statusTaquilla(taquilla: String) {
    // Llamada a la API de taquillas para obtener el estado de una taquilla

    // Devolver la respuesta de la API
    return {
        taquilla: taquilla,
        ocupada: false,
    }
}

// UPDATE /api/taquillas/modificar
function modificarDatosTaquilla(taquilla: String, datos: Object) {
    // Llamada a la API de taquillas para modificar los datos de una taquilla

    // Devolver la respuesta de la API
    return {
        taquilla: taquilla,
        datos: datos,
    }
}

// UPDATE /api/taquillas/cambiar
function cambiarTaquilla(taquilla: String, nuevaTaquilla: String) {
    // Llamada a la API de taquillas para cambiar una taquilla por otra

    // Devolver la respuesta de la API
    return {
        taquilla: taquilla,
        nuevaTaquilla: nuevaTaquilla,
    }
}