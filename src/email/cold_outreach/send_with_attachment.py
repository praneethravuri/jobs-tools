"""
Legacy script - redirects to send_cold_emails.py with attachment support.

This script is maintained for backward compatibility. Please use the new
send_cold_emails.py module for better type safety and features.
"""

from pathlib import Path
from src.email.cold_outreach.send_cold_emails import send_cold_emails

# Example usage - customize with your recipients
email_list = [
    {"name": "Recipient One", "email": "recipient1@example.com", "company": "TechCorp", "position": "Software Engineer"},
    {"name": "Recipient Two", "email": "recipient2@example.com", "company": "TechCorp", "position": "Software Engineer"}
]

company_name = "TechCorp"
subject = "Application for Software Engineer Position"

# Update this path to your resume location
resume_path = Path.home() / "Desktop" / "resume.pdf"

if __name__ == "__main__":
    # Set dry_run=False to actually send emails
    send_cold_emails(
        email_list=email_list,
        company_name=company_name,
        attachment_path=str(resume_path),
        dry_run=True  # Change to False to send emails
    )
