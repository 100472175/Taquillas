import configparser
import smtplib
import ssl
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def send_email_verification(nombre: str, nia: str, taquilla: str, codigo: str) -> None:
    """
    Envía un email de confirmación de la reserva de una taquilla
    :param nombre: Nombre del cliente que ha reservado la taquilla
    :param nia: NIA del cliente que ha reservado la taquilla, con el formato 100XXXXXX
    :param taquilla: Taquilla que el cliente ha reservado
    :param codigo: Código de confirmación de la reserva de la taquilla que se envía al cliente
    :return: None
    """
    # Configuración del email
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Configuración del servidor SMTP
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # Default TLS port

    # Configuración del email, remitente, destinatario, contraseña y asunto
    sender_email = config["EMAIL"]["email"]
    receiver_email = f"{nia}@alumnos.uc3m.es"
    password = config["EMAIL"]["password"]
    subject = f"Código de confirmación para la reserva de taquillas: {codigo}"

    # Maqueta del mensaje
    with open("confirmation/email.html", "r") as f:
        body_unformated = f.read()
    html_message = body_unformated.format(nombre=nombre, taquilla=taquilla, codigo=codigo)

    # Configuración del mensaje
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(html_message, 'html'))  # Set the content type to 'html'
    context = ssl.create_default_context()

    # Configuración del archivo adjunto, intentando establecer una conexión con el servidor SMTP
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls(context=context)  # Upgrade the connection to use TLS
        server.login(sender_email, password)
    except Exception as e:
        print(f"Error: {e}")

    # Intento de envio del email, si no se puede, se imprime el error y se cierra la conexión siempre
    try:
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully to " + receiver_email)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.quit()


def send_backup_email_db() -> None:
    """
    Envía un email con la base de datos adjunta
    :return:
    """
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Configuración del servidor SMTP
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # Default TLS port

    # Configuración del email, remitente, destinatario, contraseña y asunto
    sender_email = config["EMAIL"]["email"]
    receiver_email = config["EMAIL"]["email"]
    password = config["EMAIL"]["password"]

    # Configuración del mensaje
    html_message = f"""
    <html>
        <body>
            <p>Adjunto copia de seguridad de la base de datos.</p>
        </body>
    </html>
    """

    # Configuración del mensaje
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = sender_email
    msg['Subject'] = f"Copia de Seguridad de la Base de datos a {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
    msg.attach(MIMEText(html_message, 'html'))  # Set the content type to 'html'

    # Configuración del archivo adjunto, lectura de la base de datos
    with open("database/database.db", "rb") as fil:
        part = MIMEApplication(
            fil.read(),
            Name="database.db")
        fil.close()

    # Configuración del archivo adjunto, estableciendo el nombre del archivo en el correo. Se adjunta la base de datos
    part['Content-Disposition'] = 'attachment; filename="database.db"'
    msg.attach(part)

    # Se intenta establecer una conexión con el servidor SMTP. Si no se puede, se imprime el error
    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls(context=context)  # Mejora la conexión a TLS
        server.login(sender_email, password)
    except Exception as e:
        print(f"Error: {e}")

    # Envia el email. Si no se puede, se imprime el error y se cierra la conexión siempre
    try:
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully to " + receiver_email)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.quit()


if __name__ == "__main__":
    send_backup_email_db("100472175")
