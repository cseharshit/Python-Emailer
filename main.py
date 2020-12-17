import smtplib, ssl
import os
from smtplib import SMTPAuthenticationError
from dotenv import load_dotenv, main
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders, message
from getpass import getpass

load_dotenv('.env')

def email():
    global email_text, sender_email, receiver_email
    sender_email=os.getenv('EMAIL')
    receiver_email=input('Enter receiver\'s mail address: ')
    subject = input("\nSubject: ")
    lines = []
    print("\nBody: \n")
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            break
    body = '\n'.join(lines)

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    
    message.attach(MIMEText(body,"plain"))

    if input('\nDo you want to add an attachment:(y/n) ').lower() == 'y':
        filename = input("Enter filename: ")
        with open(filename, "rb") as attachment:
            part = MIMEBase("application","octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)

        part.add_header("Content-Disposition", f"attachment; filename = {filename}",)

        message.attach(part)
    
    else:
        print("Sending mail without email-attachment")
    
    email_text = message.as_string()


def mailer():
    smtp_server = os.getenv('SERVER')
    smtp_port=int(os.getenv('PORT'))
    password=getpass("Enter your password: ")
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
        try:
            server.login(sender_email,password)
            server.sendmail(sender_email,receiver_email, email_text)
            server.quit()
        except SMTPAuthenticationError:
            print("Invalid User Name or Password.\n\
            Make sure you have disabled the google's protection against less secure apps. https://www.google.com/settings/security/lesssecureapps ")
            

if __name__ == "__main__":
    email()
    mailer()