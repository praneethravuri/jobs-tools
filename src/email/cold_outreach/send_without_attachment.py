"""
Legacy script - redirects to send_cold_emails.py for backward compatibility.

This script is maintained for backward compatibility. Please use the new
send_cold_emails.py module for better type safety and features.
"""

from src.email.cold_outreach.send_cold_emails import send_cold_emails

# Example usage - customize with your recipients
email_list = [
    {"name": "Recipient One", "email": "recipient1@example.com", "company": "ServiceNow", "position": "Software Engineer"},
    {"name": "Recipient Two", "email": "recipient2@example.com", "company": "ServiceNow", "position": "Software Engineer"}
]

company_name = "ServiceNow"
job_ids = [
    "Technical Support Engineer - JB0044741",
    "Software Engineer - JB0044400",
    "Software Engineer - JB0045871"
]

if __name__ == "__main__":
    # Set dry_run=False to actually send emails
    send_cold_emails(
        email_list=email_list,
        company_name=company_name,
        job_ids=job_ids,
        dry_run=True  # Change to False to send emails
    )
