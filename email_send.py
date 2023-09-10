import smtplib
from email.mime.text import MIMEText


def send_email_verification(nombre, nia, taquilla, codigo):
    taquilla = taquilla
    sender_email = "noreplytaquillaseps@gmail.com"
    sender_password = "ktjolryomwuzjejw"
    subject = f"Código de confirmación para la reserva de taquillas: {codigo}"
    recipient_email = f"{nia}@alumnos.uc3m.es"

    with open("email.html", "r") as f:
        body_unformated = f.read()
    body = body_unformated.format(nombre=nombre, taquilla=taquilla, codigo=codigo)

    html_message = MIMEText(str(body), 'html')
    html_message['Subject'] = subject
    html_message['From'] = sender_email
    html_message['To'] = recipient_email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, html_message.as_string())
    print("Email sent successfully to " + recipient_email)

if __name__ == "__main__":
    send_email_verification("Edu", "100472175", "1.0.G001", "123456a")