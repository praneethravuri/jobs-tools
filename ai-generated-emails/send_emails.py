import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from model import rephrase_content

smtp_port = 587
smtp_server = "smtp.gmail.com"

email_from = os.getenv('EMAIL_FROM')  # Hide email in environment variable
email_list = [
    {'name': 'Test1', 'email': 'Test1@gmail.com', 'company': 'TEst_Company', 'position': 'Software Engineer'},
    {'name': 'Test20', 'email': 'Test21@gmail.com', 'company': 'TEst2_Company', 'position': 'Software Engineer'}
]

gmail_password = os.getenv('GMAIL_APP_PASSWORD')


def send_emails(email_list):
    template_subject = "Discovering {position} opportunities at {company}"
    template_body = """
Hi {name},

My name is [REDACTED], and I am writing to express my interest in potential opportunities at {company}. I am a {position} with a strong background in developing scalable applications and a passion for leveraging technology to create impactful solutions. I hold a Master's degree in Computer Science from [REDACTED].

My technical skills include Python, JavaScript, TypeScript, React, Next.js, and MongoDB, among others. I have worked on diverse projects, including machine learning and full stack applications. I am particularly impressed by {company}'s commitment to partnering with entrepreneurs from idea to IPO and your focus on fostering innovative, AI-driven companies.

I believe that my expertise and enthusiasm for technology align well with {company}'s mission to support and develop the next generation of transformative tech companies. I am eager to bring fresh perspectives and new talent to your team and contribute to {company}'s legacy of success.

Thank you for considering my application. I look forward to the possibility of discussing how I can contribute to your team.

"""

    contact_info = """
Best regards,
[REDACTED]
Website: [REDACTED]
Phone: [REDACTED]
LinkedIn: [REDACTED]
GitHub: [REDACTED]
"""

    for person in email_list:
        subject = template_subject.format(position=person['position'], company=person['company'])
        body = template_body.format(name=person['name'], position=person['position'], company=person['company'])

        # Rephrase using the model
        rephrased_subject = rephrase_content("phi3", subject, add_salutation=False).strip().replace("Investigating", "Discovering").replace("Uncovering", "Discovering").replace("Explore", "Exploring")
        rephrased_body = rephrase_content("phi3", body, add_salutation=False).strip() + "\n" + contact_info

        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = person['email']
        msg['Subject'] = rephrased_subject.replace('\n', ' ').replace('\r', '')

        msg.attach(MIMEText(rephrased_body, 'plain'))

        text = msg.as_string()

        print("Connecting to server...")
        TIE_server = smtplib.SMTP(smtp_server, smtp_port)
        TIE_server.starttls()
        TIE_server.login(email_from, gmail_password)
        print("Successfully connected to server")

        print(f"Sending email to: {person['email']}...")
        TIE_server.sendmail(email_from, person['email'], text)
        print(f"Email sent to: {person['email']}")
        print()

    TIE_server.quit()

send_emails(email_list)
