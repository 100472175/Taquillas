import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import configparser


def send_email_verification(nombre, nia, taquilla, codigo):
    return # Desactivamos el envío de emails
    # Configuración del email
    config = configparser.ConfigParser()
    config.read("config.ini")

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # Default TLS port

    sender_email = config["EMAIL"]["email"]
    receiver_email = f"{nia}@alumnos.uc3m.es"
    password = config["EMAIL"]["password"]
    subject = f"Código de confirmación para la reserva de taquillas: {codigo}"

    with open("confirmation/email.html", "r") as f:
        body_unformated = f.read()
    html_message = body_unformated.format(nombre=nombre, taquilla=taquilla, codigo=codigo)

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
    send_email_verification("Edu", "100472175", "1.0.G001", "123456a")