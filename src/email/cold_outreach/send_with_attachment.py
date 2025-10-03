import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from dotenv import load_dotenv


load_dotenv()

main_file_directory = r"C:\Projects\jobs\cold-emails"


smtp_port = 587                
smtp_server = "smtp.gmail.com"  

email_from = "pravdev10@gmail.com"
email_list = []

pswd = os.getenv("GMAIL_APP_PASSWORD")

subject = "New email from TIE with attachments!!"

def send_emails(email_list):

    for person in email_list:
        body = f"""
        line 1
        line 2
        line 3
        etc
        """

        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = person
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        #filename = r"C:\Projects\jobs\cold-emails\praneeth_ravuri_resume.pdf"

        filename = main_file_directory + "\praneeth_ravuri_resume.pdf"


        try:
            attachment = open(filename, 'rb')
        except FileNotFoundError:
            print(f"Error: The file {filename} was not found.")

        attachment_package = MIMEBase('application', 'octet-stream')
        attachment_package.set_payload((attachment).read())
        encoders.encode_base64(attachment_package)
        attachment_package.add_header('Content-Disposition', "attachment; filename= " + filename)
        msg.attach(attachment_package)

        text = msg.as_string()

        print("Connecting to server...")
        TIE_server = smtplib.SMTP(smtp_server, smtp_port)
        TIE_server.starttls()
        TIE_server.login(email_from, pswd)
        print("Succesfully connected to server")
        print()


        print(f"Sending email to: {person}...")
        TIE_server.sendmail(email_from, person, text)
        print(f"Email sent to: {person}")
        print()

    TIE_server.quit()

send_emails(email_list)
