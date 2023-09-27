import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import configparser
import openpyxl


def send_email_verification(nombre, nia, usuario, passwd):
    # Configuración del email
    config = configparser.ConfigParser()
    config.read("../config.ini")

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # Default TLS port

    sender_email = config["EMAIL"]["email"]
    receiver_email = f"{nia}@alumnos.uc3m.es"
    password = config["EMAIL"]["password"]
    subject = f"Acceso a la aplicación de taquillas: {usuario}"

    html_message = f"""
    <html>
        <body>
            <p>Hola {nombre},</p>
            <p>Para acceder a la aplicación de taquillas, por favor, introduce el usuario <b>{usuario}</b> y la siguiente contraseña: <b>{passwd}</b></p>
            <p>Un saludo,</p>
            <p>El equipo de taquillas</p>
        </body>
    </html>
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(html_message, 'html'))  # Set the content type to 'html'

    context = ssl.create_default_context()

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls(context=context)  # Upgrade the connection to use TLS
        server.login(sender_email, password)
    except Exception as e:
        print(f"Error: {e}")

    # Send the email
    try:
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully to " + receiver_email)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.quit()



if __name__ == "__main__":
    archivo = openpyxl.load_workbook("tax.xlsx")
    sheet = archivo["Hoja1"]
    i = 2
    while sheet[f"A{i}"].value is not None:
        send_email_verification(sheet[f"A{i}"].value, sheet[f"C{i}"].value, sheet[f"B{i}"].value, sheet[f"E{i}"].value)
        i += 1
