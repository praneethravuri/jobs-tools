"""
Send cold outreach emails with optional resume attachments.

This module provides functionality for sending cold emails to recruiters
and hiring managers with or without resume attachments.
"""

import logging
from typing import List, Dict, Optional
from pathlib import Path

from src.email.email_sender import EmailSender
from src.models.email import EmailRecipient, EmailMessage
from src.config import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Sample email list
SAMPLE_EMAIL_LIST = [
    {"name": "Jane Recruiter", "email": "jane@company.com", "company": "TechCorp", "position": "Software Engineer"},
]

# Default templates
DEFAULT_SUBJECT = "Looking for opportunities at {company}"
DEFAULT_BODY_TEMPLATE = """Hello {first_name},

I noticed that you are working at {company}. I'm a CS grad looking for new opportunities and wonder if you could refer me to various positions at {company}.

The Job IDs:
{job_ids}

Thank you,
[Your Name]
Ph: [Your Phone Number]
LinkedIn: [Your LinkedIn URL]
Website: [Your Website URL]
GitHub: [Your GitHub URL]
"""


def send_cold_emails(
    email_list: List[Dict[str, str]],
    company_name: Optional[str] = None,
    job_ids: Optional[List[str]] = None,
    subject_template: str = DEFAULT_SUBJECT,
    body_template: str = DEFAULT_BODY_TEMPLATE,
    attachment_path: Optional[str] = None,
    dry_run: bool = False
) -> int:
    """
    Send cold outreach emails to recruiters and hiring managers.

    This function sends personalized cold emails to a list of recipients,
    optionally including a resume attachment. Each email can be customized
    with specific job IDs and company information.

    Args:
        email_list: List of recipient dictionaries with name, email, company, position
        company_name: Override company name for all emails (optional)
        job_ids: List of job IDs to include in email
        subject_template: Email subject template with {company} placeholder
        body_template: Email body template with {first_name}, {company}, {job_ids} placeholders
        attachment_path: Path to resume PDF file to attach (optional)
        dry_run: If True, generate emails but don't send them

    Returns:
        Number of emails successfully sent

    Example:
        >>> recipients = [
        ...     {"name": "John Doe", "email": "john@company.com",
        ...      "company": "TechCorp", "position": "Recruiter"}
        ... ]
        >>> job_ids = ["JOB-123", "JOB-456"]
        >>> count = send_cold_emails(
        ...     recipients,
        ...     job_ids=job_ids,
        ...     attachment_path="/path/to/resume.pdf",
        ...     dry_run=True
        ... )
    """
    sent_count = 0

    # Format job IDs for email body
    if job_ids:
        job_ids_text = "\n".join(f"{i+1}. {job_id}" for i, job_id in enumerate(job_ids))
    else:
        job_ids_text = "(Please see attached resume for details)"

    # Validate attachment path if provided
    if attachment_path:
        attachment = Path(attachment_path)
        if not attachment.exists():
            raise FileNotFoundError(f"Attachment not found: {attachment_path}")
        logger.info(f"Using attachment: {attachment}")

    logger.info(f"Starting cold email campaign for {len(email_list)} recipients")
    if dry_run:
        logger.info("🔸 DRY RUN MODE - Emails will not be sent")

    try:
        with EmailSender() as sender:
            for person_data in email_list:
                try:
                    # Validate recipient data
                    recipient = EmailRecipient(**person_data)

                    # Use provided company name or recipient's company
                    company = company_name or recipient.company

                    # Generate email content
                    subject = subject_template.format(company=company)
                    body = body_template.format(
                        first_name=recipient.first_name,
                        company=company,
                        job_ids=job_ids_text
                    )

                    # Create email message
                    message = EmailMessage(
                        to_email=recipient.email,
                        subject=subject,
                        body=body,
                        attachment_path=attachment_path
                    )

                    # Send email (or skip if dry run)
                    if dry_run:
                        logger.info(f"[DRY RUN] Would send to: {recipient.name} ({recipient.email})")
                        if attachment_path:
                            logger.info(f"  With attachment: {Path(attachment_path).name}")
                        sent_count += 1
                    else:
                        if sender.send_email(message):
                            sent_count += 1

                except Exception as e:
                    logger.error(
                        f"Error sending email to {person_data.get('name', 'Unknown')}: {e}"
                    )
                    continue

    except Exception as e:
        logger.error(f"Cold email campaign failed: {e}")
        raise

    logger.info(f"✓ Campaign complete. Sent {sent_count}/{len(email_list)} emails")
    return sent_count


if __name__ == "__main__":
    # Example usage
    job_ids_list = ["JOB-12345", "JOB-67890"]

    # Send without attachment
    send_cold_emails(
        SAMPLE_EMAIL_LIST,
        company_name="ServiceNow",
        job_ids=job_ids_list,
        dry_run=True
    )

    # Send with attachment (uncomment to use)
    # send_cold_emails(
    #     SAMPLE_EMAIL_LIST,
    #     company_name="ServiceNow",
    #     job_ids=job_ids_list,
    #     attachment_path="~/Desktop/resume.pdf",
    #     dry_run=True
    # )
