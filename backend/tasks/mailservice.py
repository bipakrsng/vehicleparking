import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

EMAIL_ADDRESS ='bipulkumarsng@gmail.com'
EMAIL_PASSWORD = 'whqs uehl pnnt uvuw'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

def send_email(subject,recipient,body,html_body=None,attachments=None):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(body,'plain'))

    if html_body:
        msg.attach(MIMEText(html_body,'html'))
    
    if attachments:
        for attachment in attachments:
            filename = attachment.get('filename')
            file_path = attachment.get('file_path')
            if os.path.exists(file_path):
                with open(file_path, 'rb') as file:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(file.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename={filename}')
                    msg.attach(part)
            else:
                print(f"Attachment {file_path} not found.")
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, recipient, msg.as_string())
            print(f"Email sent to {recipient}")
    except Exception as e:
        print(f"Failed to send email to {recipient}. Error: {e}")