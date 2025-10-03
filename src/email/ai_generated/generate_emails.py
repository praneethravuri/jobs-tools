from model import rephrase_content
import json

email_list = [
    {'name': 'Julie', 'email': 'jsmith@greylock.com', 'company': 'Greylock', 'position': 'Software Engineer'},
    {'name': 'Katy', 'email': 'kamaya@greylock.com', 'company': 'Greylock', 'position': 'Software Engineer'},
    {'name': 'Abby', 'email': 'ahart@greylock.com', 'company': 'Greylock', 'position': 'Software Engineer'},
    {'name': 'Omar', 'email': 'omunoz@greylock.com', 'company': 'Greylock', 'position': 'Software Engineer'},
    {'name': 'Dwane', 'email': 'dhamilton@greylock.com', 'company': 'Greylock', 'position': 'Software Engineer'},
    {'name': 'Vish', 'email': 'vpatel@greylock.com', 'company': 'Greylock', 'position': 'Software Engineer'},
    {'name': 'Natalia', 'email': 'nkeohane@greylock.com', 'company': 'Greylock', 'position': 'Software Engineer'},
    {'name': 'Glen', 'email': 'gevans@greylock.com', 'company': 'Greylock', 'position': 'Software Engineer'},
    {'name': 'John', 'email': 'jdelaney@greylock.com', 'company': 'Greylock', 'position': 'Software Engineer'},
    {'name': 'Renee', 'email': 'rsignore@greylock.com', 'company': 'Greylock', 'position': 'Software Engineer'},
    {'name': 'Holly', 'email': 'hollyrose@greylock.com', 'company': 'Greylock', 'position': 'Software Engineer'},
    {'name': 'Holly', 'email': 'hollyrose@greylock.com', 'company': 'Test', 'position': 'Software Engineer'},
    {'name': 'Holly', 'email': 'hollyrose@greylock.com', 'company': 'Test', 'position': 'Software Engineer'},
]

def generate_emails(email_list):
    template_subject = "Discovering {position} opportunities at {company}"
    template_body = """
Hi {name},

My name is Praneeth Ravuri, and I am writing to express my interest in potential opportunities at {company}. I am a {position} with a strong background in developing scalable applications and a passion for leveraging technology to create impactful solutions. I hold a Master's degree in Computer Science from George Mason University.

My technical skills include Python, JavaScript, TypeScript, React, Next.js, and MongoDB, among others. I have worked on diverse projects, including machine learning and full stack applications. I am particularly impressed by {company}'s commitment to partnering with entrepreneurs from idea to IPO and your focus on fostering innovative, AI-driven companies.

I believe that my expertise and enthusiasm for technology align well with {company}'s mission to support and develop the next generation of transformative tech companies. I am eager to bring fresh perspectives and new talent to your team and contribute to {company}'s legacy of success.

Thank you for considering my application. I look forward to the possibility of discussing how I can contribute to your team.

"""

    company_emails = {}

    for person in email_list:
        subject = template_subject.format(position=person['position'], company=person['company'])
        body = template_body.format(name=person['name'], position=person['position'], company=person['company'])

        # Rephrase using the model
        rephrased_subject = rephrase_content("phi3", subject, add_salutation=False).strip().replace("Investigating", "Discovering").replace("Uncovering", "Discovering").replace("Explore", "Exploring")
        rephrased_body = rephrase_content("phi3", body, add_salutation=False).strip()

        generated_email = {
            "name": person['name'],
            "email": person['email'],
            "position": person['position'],
            "company": person['company'],
            "generatedSubject" : rephrased_subject,
            "generatedEmail" : rephrased_body.replace("\n", ' ')
        }

        if person['company'] not in company_emails:
            company_emails[person['company']] = []

        company_emails[person['company']].append(generated_email)

        print(f"Generated email for {person['name']}")

    for company, emails in company_emails.items():
        with open(f'generated_emails_{company}.json', 'w') as json_file:
            json.dump(emails, json_file, indent=4)

if __name__ == "__main__":
    generate_emails(email_list)
