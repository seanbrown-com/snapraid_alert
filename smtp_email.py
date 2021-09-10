import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import socket

# Create a secure SSL context
context = ssl.create_default_context()


class SmtpEmail:
    def __init__(self, sender_email, destination_email, server, port, password, command, attachment=None):
        self.server = server
        self.port = port
        self.password = password
        self.sender_email = sender_email
        self.destination_email = destination_email
        self.command = command
        self.attachment = attachment

    def send_email(self, msg=None):
        subject = 'Snapraid ' + self.command + ' failed'
        body = "This is an email with attachment sent from Python"

        # Create a multipart message and set headers
        message = MIMEMultipart('alternative')
        message['From'] = self.sender_email
        message['To'] = self.destination_email
        message['Subject'] = subject
        # message['Bcc'] = receiver_email  # Recommended for mass emails

        hostname = socket.gethostname()
        html = '<html> <body> <p>' \
               'Hey Peter, what\'s happening?<br> Ummm, I\'m gonna need you to go ahead and check ' \
               'on ' + hostname + '. It looks like Snapraid had an unsuccessful ' + self.command + ' last night, kay.' \
                                  ' So if you could do that,  that\'d be great, mmmk?<br>' \
                                  '<img src="https://memegenerator.net/img/instances/55887803.jpg" ' \
                                  'width=320 height=172><br><br>' \
                                  'error_msg: ' + msg if msg is not None else '' + \
                                  '</p> </body> </html>'

        # Add HTML parts to MIMEMultipart message
        message.attach(MIMEText(html, 'html'))

        if self.attachment:
            # Open PDF file in binary mode
            with open(self.attachment, 'rb') as attachment:
                # Add file as application/octet-stream
                # Email client can usually download this automatically as attachment
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            # Encode file in ASCII characters to send by email
            encoders.encode_base64(part)
            # Add header as key/value pair to attachment part
            part.add_header(
                'Content-Disposition',
                f"attachment; filename= {self.attachment}",
            )
            # Add attachment to message and convert message to string
            message.attach(part)

        # Log in to server using secure context and send email
        my_context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.server, self.port, context=my_context) as server:
            try:
                server.login(self.sender_email, self.password)
                server.sendmail(self.sender_email, self.destination_email, message.as_string())
            except Exception as e:
                print(e)
                exit(1)



def test():
    email = SmtpEmail('your_email@email.com', 'some_email@email.com', 'smtp.email.com', 123,
                      'your_password', 'sync', 'your_log_file.log')
    email.send_email()


if __name__ == '__main__':
    test()
