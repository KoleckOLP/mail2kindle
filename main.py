import argparse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from config import smtp_server, smtp_port, sender_email, sender_password, receiver_email

# define your command line arguments
parser = argparse.ArgumentParser(description='sending multiple files to your kindle')
parser.add_argument('path', help='path where you files are stored')
parser.add_argument('-r', '--range', help='range of chapters example: 5-10', required=False)

# parse command line arguments
args = parser.parse_args()

# Accessing arguments values
print('path ', args.path)

print(smtp_server, smtp_port, sender_email, sender_password, receiver_email)

# Create the MIMEMultipart message object and load it with appropriate headers
message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email
message['Subject'] = 'here is test.jpg'

# Add your message body
message_body = 'I hope you like test.jpg'
message.attach(MIMEText(message_body, 'plain'))

file_to_send = "test.jpg"

# Add your attachment
with open(file_to_send, 'rb') as attachment:
    part = MIMEApplication(attachment.read(), Name='attachment_name')
    part['Content-Disposition'] = f'attachment; filename="{file_to_send}"'
    message.attach(part)

print("starting sever")

# Send the message using the SMTP server object
with smtplib.SMTP(smtp_server, smtp_port) as server:
    print("starting TLS")
    server.starttls()
    print("logging in")
    server.login(sender_email, sender_password)
    print("sending mail")
    server.sendmail(sender_email, receiver_email, message.as_string())
    print("all done")
