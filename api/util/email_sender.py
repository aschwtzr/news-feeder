import smtplib
import ssl
import os

port = 465
password = os.environ.get('EMAIL_PASSWORD')
email = os.environ.get('EMAIL_ADDRESS')

context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(email, password)
    message = """\
    Subject: hi hello

    I am an email. """
    server.sendmail(email, 'schweitzer.albert@gmail.com', message)