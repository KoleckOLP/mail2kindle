import os, argparse, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from config import smtp_server, smtp_port, sender_email, sender_password, receiver_email

# define your command line arguments
parser = argparse.ArgumentParser(description='Script to send chapters of a comic/manga to kindle')
# Argumetns for sending comic chapters
parser.add_argument('-pn', '--PathName', help='Path to where chapters are stored including the name of the comic, '+
                    'example: "C:\\Users\\Guest\\Downloads\\Manga\\Spy X Family\\Spy X Family Chapter "')
parser.add_argument('-r', '--Range', help='Range of chapters you want to send, example: 40-45')
parser.add_argument('-e', '--Extencion', help='Extencion of comics, example: .mobi [default = .epub]', default='.epub')
parser.add_argument('-as', '--AllowSubChapters', help='Allow sub chapters, example: 40.1, 40.5, 40.9 [default = False]', default=False)
# Arguments for sending books
parser.add_argument('-bl', '--BookList', help='Manual list of books that don\'t share numbers, paths in quotes separated by space, '+
                    'example: "D:\\Books\\Little Prince.mobi" "D:\\Books\\Lolita.epub" [can\'t be combined with other arguments]', nargs='+')

# parse command line arguments
args = parser.parse_args()

filelist = []

if args.BookList:  # This path is taken for books
    for filepath in args.BookList:
        fileexists = os.path.isfile(filepath)
        if fileexists:
                    filelist += [filepath]

else:  # THis path is taken for comics
    start, end = map(int, args.Range.split('-'))

    # creates a list of files in the range that atually exist
    for chapter in range(start, end+1):
        filepath = (f'{args.PathName}{chapter}{args.Extencion}')
        fileexists = os.path.isfile(filepath)
        if fileexists:
            filelist += [filepath]
        if args.AllowSubChapters:
            for subchapter in range(1, 11):
                filepath = (f'{args.PathName}{chapter}.{subchapter}{args.Extencion}')
                fileexists = os.path.isfile(filepath)
                if fileexists:
                    filelist += [filepath]        

for filepath in filelist:  # Paths combine here
    filename = os.path.splitext(os.path.basename(filepath))[0]

    # Create the MIMEMultipart message object and load it with appropriate headers
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = filename

    # Add your message body
    message_body = filepath
    message.attach(MIMEText(message_body, 'plain'))

    # Add your attachment
    with open(filepath, 'rb') as attachment:
        part = MIMEApplication(attachment.read(), Name='attachment_name')
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(filepath)}"'
        message.attach(part)

    print(f'emailing {filename}...')

    # Send the message using the SMTP server object
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("sent.")
