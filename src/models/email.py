"""
Email-related Pydantic models for type-safe email operations.

This module provides models for email recipients, configuration, templates,
and complete email messages used throughout the email automation tools.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


class EmailRecipient(BaseModel):
    """
    Represents an email recipient with their contact and job application details.

    Attributes:
        name: Full name of the recipient
        email: Valid email address
        company: Company name where the recipient works
        position: Job position being applied for
    """

    name: str = Field(..., min_length=1, description="Recipient's full name")
    email: EmailStr = Field(..., description="Valid email address")
    company: str = Field(..., min_length=1, description="Company name")
    position: str = Field(..., min_length=1, description="Position being applied for")

    @field_validator("name", "company", "position")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        """Remove leading and trailing whitespace from string fields."""
        return v.strip()

    @property
    def first_name(self) -> str:
        """Extract the first name from the full name."""
        return self.name.split()[0] if self.name else ""

    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john.doe@techcorp.com",
                "company": "TechCorp",
                "position": "Software Engineer"
            }
        }


class EmailConfig(BaseModel):
    """
    SMTP email server configuration.

    Attributes:
        smtp_server: SMTP server hostname
        smtp_port: SMTP server port (typically 587 for TLS)
        email_from: Sender's email address
        password: SMTP authentication password (app password for Gmail)
    """

    smtp_server: str = Field(default="smtp.gmail.com", description="SMTP server hostname")
    smtp_port: int = Field(default=587, ge=1, le=65535, description="SMTP port number")
    email_from: EmailStr = Field(..., description="Sender email address")
    password: str = Field(..., min_length=1, description="SMTP password")

    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "email_from": "your.email@gmail.com",
                "password": "your_app_password"
            }
        }


class EmailTemplate(BaseModel):
    """
    Email template with placeholder support for personalization.

    Attributes:
        subject: Email subject line (supports {company}, {position} placeholders)
        body: Email body text (supports {name}, {company}, {position} placeholders)
    """

    subject: str = Field(..., min_length=1, description="Email subject template")
    body: str = Field(..., min_length=1, description="Email body template")

    def render(self, recipient: EmailRecipient, **kwargs) -> "EmailMessage":
        """
        Render the template with recipient data and additional context.

        Args:
            recipient: EmailRecipient instance with personalization data
            **kwargs: Additional template variables

        Returns:
            Rendered EmailMessage instance
        """
        context = {
            "name": recipient.name,
            "company": recipient.company,
            "position": recipient.position,
            **kwargs
        }

        return EmailMessage(
            to_email=recipient.email,
            subject=self.subject.format(**context),
            body=self.body.format(**context)
        )

    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "subject": "Discovering {position} opportunities at {company}",
                "body": "Hi {name},\n\nI am writing to express my interest in the {position} role at {company}..."
            }
        }


class EmailMessage(BaseModel):
    """
    Complete email message ready to be sent.

    Attributes:
        to_email: Recipient's email address
        subject: Rendered email subject
        body: Rendered email body
        attachment_path: Optional path to file attachment
    """

    to_email: EmailStr = Field(..., description="Recipient email address")
    subject: str = Field(..., min_length=1, description="Email subject")
    body: str = Field(..., min_length=1, description="Email body")
    attachment_path: Optional[str] = Field(None, description="Path to attachment file")

    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "to_email": "hiring@company.com",
                "subject": "Application for Software Engineer Position",
                "body": "Dear Hiring Manager,\n\nI am writing to apply...",
                "attachment_path": "/path/to/resume.pdf"
            }
        }
