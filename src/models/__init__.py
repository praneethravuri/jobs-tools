"""
Data models for the jobs-tools package.

This module provides Pydantic models for type-safe data validation and serialization
across email, resume, and scraping operations.
"""

from src.models.email import EmailRecipient, EmailConfig, EmailTemplate, EmailMessage
from src.models.resume import (
    ResumeHeader,
    WorkExperience,
    Education,
    SkillGroup,
    Project,
    Resume,
)
from src.models.scraping import H1BCompany

__all__ = [
    # Email models
    "EmailRecipient",
    "EmailConfig",
    "EmailTemplate",
    "EmailMessage",
    # Resume models
    "ResumeHeader",
    "WorkExperience",
    "Education",
    "SkillGroup",
    "Project",
    "Resume",
    # Scraping models
    "H1BCompany",
]
