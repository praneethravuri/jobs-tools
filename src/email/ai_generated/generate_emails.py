"""
Generate AI-personalized emails for multiple recipients and save to JSON files.

This script generates customized emails using Ollama AI models for rephrasing
and personalization. Emails are organized by company and saved as JSON files.
"""

import json
import logging
from pathlib import Path
from typing import List, Dict
from src.email.ai_generated.model import rephrase_content
from src.models.email import EmailRecipient, EmailTemplate

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Sample email list (replace with your actual recipients)
SAMPLE_EMAIL_LIST = [
    {'name': 'Julie Smith', 'email': 'jsmith@example.com', 'company': 'Example Inc', 'position': 'Software Engineer'},
    {'name': 'John Doe', 'email': 'jdoe@example.com', 'company': 'Example Inc', 'position': 'Software Engineer'},
]

# Default email template
DEFAULT_TEMPLATE_SUBJECT = "Discovering {position} opportunities at {company}"
DEFAULT_TEMPLATE_BODY = """Hi {name},

My name is Praneeth Ravuri, and I am writing to express my interest in potential opportunities at {company}. I am a {position} with a strong background in developing scalable applications and a passion for leveraging technology to create impactful solutions. I hold a Master's degree in Computer Science from George Mason University.

My technical skills include Python, JavaScript, TypeScript, React, Next.js, and MongoDB, among others. I have worked on diverse projects, including machine learning and full stack applications. I am particularly impressed by {company}'s commitment to innovation and excellence.

I believe that my expertise and enthusiasm for technology align well with {company}'s mission. I am eager to bring fresh perspectives and new talent to your team and contribute to {company}'s continued success.

Thank you for considering my application. I look forward to the possibility of discussing how I can contribute to your team.
"""


def generate_emails(
    email_list: List[Dict[str, str]],
    model_name: str = "phi3",
    template_subject: str = DEFAULT_TEMPLATE_SUBJECT,
    template_body: str = DEFAULT_TEMPLATE_BODY,
    output_dir: Path = Path(".")
) -> Dict[str, List[Dict]]:
    """
    Generate AI-personalized emails for a list of recipients.

    This function takes a list of email recipients, generates personalized emails
    using AI rephrasing, and organizes them by company. Each email is rephrased
    to avoid repetition while maintaining the core message.

    Args:
        email_list: List of dictionaries containing recipient information
            Each dict should have: name, email, company, position
        model_name: Ollama model to use for rephrasing (default: "phi3")
        template_subject: Email subject template with {company}, {position} placeholders
        template_body: Email body template with {name}, {company}, {position} placeholders
        output_dir: Directory to save generated email JSON files

    Returns:
        Dictionary mapping company names to lists of generated emails

    Example:
        >>> recipients = [
        ...     {'name': 'John Doe', 'email': 'john@company.com',
        ...      'company': 'TechCorp', 'position': 'Software Engineer'}
        ... ]
        >>> emails = generate_emails(recipients)
        >>> print(f"Generated {len(emails['TechCorp'])} emails for TechCorp")
    """
    company_emails: Dict[str, List[Dict]] = {}
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Starting email generation for {len(email_list)} recipients")

    for person_data in email_list:
        try:
            # Validate recipient data using Pydantic model
            recipient = EmailRecipient(**person_data)

            # Create email template
            subject = template_subject.format(
                position=recipient.position,
                company=recipient.company
            )
            body = template_body.format(
                name=recipient.name,
                position=recipient.position,
                company=recipient.company
            )

            # Rephrase using AI model
            logger.info(f"Generating email for {recipient.name} at {recipient.company}")

            rephrased_subject = rephrase_content(
                model_name,
                subject,
                add_salutation=False
            ).strip()

            # Apply subject replacements for consistency
            rephrased_subject = (
                rephrased_subject
                .replace("Investigating", "Discovering")
                .replace("Uncovering", "Discovering")
                .replace("Explore", "Exploring")
            )

            rephrased_body = rephrase_content(
                model_name,
                body,
                add_salutation=False
            ).strip()

            # Create generated email object
            generated_email = {
                "name": recipient.name,
                "email": recipient.email,
                "position": recipient.position,
                "company": recipient.company,
                "generatedSubject": rephrased_subject,
                "generatedEmail": rephrased_body.replace("\n", " ")
            }

            # Organize by company
            if recipient.company not in company_emails:
                company_emails[recipient.company] = []

            company_emails[recipient.company].append(generated_email)
            logger.info(f"✓ Generated email for {recipient.name}")

        except Exception as e:
            logger.error(f"Error generating email for {person_data.get('name', 'Unknown')}: {e}")
            continue

    # Save emails to JSON files organized by company
    for company, emails in company_emails.items():
        output_file = output_dir / f"generated_emails_{company}.json"
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(emails, json_file, indent=4, ensure_ascii=False)
        logger.info(f"✓ Saved {len(emails)} emails to {output_file}")

    logger.info(f"Email generation complete. Generated {sum(len(e) for e in company_emails.values())} total emails")
    return company_emails


if __name__ == "__main__":
    # Use sample email list - replace with your actual recipients
    generate_emails(SAMPLE_EMAIL_LIST)
