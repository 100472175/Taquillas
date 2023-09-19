# Aplicación de Reserva de Taquillas UC3M

## Descripción

Esta aplicación ha sido creada por la Comisión de Tecnología y Servicios, perteneciente a la [delegación de estudiantes](https://delegacion.uc3m.es/home/eps/) de la Escuela Politécnica Superior de la Universidad Carlos III de Madrid, con el objetivo de facilitar la reserva de taquillas a los estudiantes de la universidad.
Utiliza la librería 'streamlit' para la creación de la interfaz gráfica, y 'jsons' para el tratamiento de los datos.
Pensada como paso intermedio entre el sistema creado con hojas de cálculo de google y una aplicación web completa utilizando una base de datos con SQL.

## Instalación
Para poder ejejcutar la aplicación es necesario tener instalado Python 3.7 o superior.
También hay que usar el gestor de paquetes de Python, [Pip](https://pip.pypa.io/en/stable/), para instalar las librerías necesarias.
```bash
pip install requirements.txt
```

## Uso
Para usar esta aplicación, necesitas tener una cuenta de correo que permita el envio de correos desde una aplicación externa.
Para obtener esto, la manera más sencilla es crear una cuenta de gmail y activar la opción de [acceso a aplicaciones menos seguras](https://support.google.com/accounts/answer/6010255?hl=es).

Una vez obtenida la cuenta de correo, hay que crear un archivo 'config.ini'
```ini
[EMAIL]
email = <email>
password = <password>
```

Y luego, para ejecutar la aplicación, simplemente hay que ejecutar el archivo 'app.py' con streamlit:
```bash
streamlit run Reserva_Taquillas.py
```

## Contribución
Las contribuciones son bienvenidas. Para cambios importantes, por favor, haz una pull request.
Muchas gracias a todos los participantes de este proyecto.

