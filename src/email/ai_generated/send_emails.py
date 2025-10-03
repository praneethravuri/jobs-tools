"""
Send AI-generated personalized emails to multiple recipients.

This script sends customized emails using Ollama AI models for rephrasing
each message to avoid repetition while maintaining authenticity.
"""

import logging
from typing import List, Dict
from src.email.ai_generated.model import rephrase_content
from src.email.email_sender import EmailSender
from src.models.email import EmailRecipient, EmailMessage
from src.config import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Sample email list (replace with your actual recipients)
SAMPLE_EMAIL_LIST = [
    {'name': 'Test User', 'email': 'test@example.com', 'company': 'Example Corp', 'position': 'Software Engineer'},
]

# Default email template
DEFAULT_TEMPLATE_SUBJECT = "Discovering {position} opportunities at {company}"
DEFAULT_TEMPLATE_BODY = """Hi {name},

My name is [Your Name], and I am writing to express my interest in potential opportunities at {company}. I am a {position} with a strong background in developing scalable applications and a passion for leveraging technology to create impactful solutions. I hold a Master's degree in Computer Science from [Your University].

My technical skills include Python, JavaScript, TypeScript, React, Next.js, and MongoDB, among others. I have worked on diverse projects, including machine learning and full stack applications. I am particularly impressed by {company}'s commitment to innovation and excellence.

I believe that my expertise and enthusiasm for technology align well with {company}'s mission. I am eager to bring fresh perspectives and new talent to your team and contribute to {company}'s continued success.

Thank you for considering my application. I look forward to the possibility of discussing how I can contribute to your team.
"""

# Contact information footer
CONTACT_INFO = """
Best regards,
[Your Name]
Website: [Your Website]
Phone: [Your Phone]
LinkedIn: [Your LinkedIn]
GitHub: [Your GitHub]
"""


def send_ai_generated_emails(
    email_list: List[Dict[str, str]],
    model_name: str = "phi3",
    template_subject: str = DEFAULT_TEMPLATE_SUBJECT,
    template_body: str = DEFAULT_TEMPLATE_BODY,
    contact_info: str = CONTACT_INFO,
    dry_run: bool = False
) -> int:
    """
    Send AI-personalized emails to a list of recipients.

    This function generates and sends personalized emails using AI rephrasing
    to make each message unique while maintaining the core content. Each email
    is rephrased individually to avoid spam filters and provide authentic outreach.

    Args:
        email_list: List of dictionaries with recipient information
            Each dict should have: name, email, company, position
        model_name: Ollama model to use for rephrasing (default: "phi3")
        template_subject: Email subject template with placeholders
        template_body: Email body template with placeholders
        contact_info: Footer with contact information
        dry_run: If True, generate emails but don't send them

    Returns:
        Number of emails successfully sent

    Example:
        >>> recipients = [
        ...     {'name': 'John Doe', 'email': 'john@company.com',
        ...      'company': 'TechCorp', 'position': 'Software Engineer'}
        ... ]
        >>> count = send_ai_generated_emails(recipients, dry_run=True)
        >>> print(f"Generated {count} emails")
    """
    sent_count = 0
    settings = get_settings()

    logger.info(f"Starting email campaign for {len(email_list)} recipients")
    if dry_run:
        logger.info("🔸 DRY RUN MODE - Emails will not be sent")

    try:
        with EmailSender() as sender:
            for person_data in email_list:
                try:
                    # Validate recipient data
                    recipient = EmailRecipient(**person_data)

                    # Generate email content
                    subject = template_subject.format(
                        position=recipient.position,
                        company=recipient.company
                    )
                    body = template_body.format(
                        name=recipient.name,
                        position=recipient.position,
                        company=recipient.company
                    )

                    # Rephrase content using AI
                    logger.info(f"Generating personalized email for {recipient.name}")

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
                        .replace('\n', ' ')
                        .replace('\r', '')
                    )

                    rephrased_body = rephrase_content(
                        model_name,
                        body,
                        add_salutation=False
                    ).strip()

                    # Add contact info
                    full_body = f"{rephrased_body}\n{contact_info}"

                    # Create email message
                    message = EmailMessage(
                        to_email=recipient.email,
                        subject=rephrased_subject,
                        body=full_body
                    )

                    # Send email (or skip if dry run)
                    if dry_run:
                        logger.info(f"[DRY RUN] Would send to: {recipient.email}")
                        logger.info(f"Subject: {rephrased_subject}")
                        sent_count += 1
                    else:
                        if sender.send_email(message):
                            sent_count += 1

                except Exception as e:
                    logger.error(
                        f"Error processing email for "
                        f"{person_data.get('name', 'Unknown')}: {e}"
                    )
                    continue

    except Exception as e:
        logger.error(f"Email campaign failed: {e}")
        raise

    logger.info(f"✓ Email campaign complete. Sent {sent_count}/{len(email_list)} emails")
    return sent_count


if __name__ == "__main__":
    # Use sample email list - replace with your actual recipients
    # Set dry_run=False to actually send emails
    send_ai_generated_emails(SAMPLE_EMAIL_LIST, dry_run=True)
