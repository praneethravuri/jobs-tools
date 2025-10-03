"""
Resume-related Pydantic models for type-safe resume generation.

This module provides models for resume components including header, work experience,
education, skills, and projects. These models are used for generating formatted
DOCX resumes from structured JSON data.
"""

from typing import List
from pydantic import BaseModel, Field, field_validator


class ResumeHeader(BaseModel):
    """
    Resume header containing personal information and contact details.

    Attributes:
        name: Full name of the resume owner
        contact: List of contact information (email, phone, LinkedIn, etc.)
    """

    name: str = Field(..., min_length=1, description="Full name")
    contact: List[str] = Field(..., min_items=1, description="Contact information list")

    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "contact": [
                    "john.doe@email.com",
                    "(555) 123-4567",
                    "linkedin.com/in/johndoe",
                    "github.com/johndoe"
                ]
            }
        }


class WorkExperience(BaseModel):
    """
    Work experience entry for a resume.

    Attributes:
        company: Company or organization name
        location: Geographic location (city, state/country)
        position: Job title or role
        start_date: Start date (formatted string, e.g., "Jan 2020")
        end_date: End date or "Present" for current positions
        bullets: List of achievement/responsibility bullet points
    """

    company: str = Field(..., min_length=1, description="Company name")
    location: str = Field(..., min_length=1, description="Location")
    position: str = Field(..., min_length=1, description="Job title")
    start_date: str = Field(..., min_length=1, description="Start date")
    end_date: str = Field(..., min_length=1, description="End date or 'Present'")
    bullets: List[str] = Field(..., min_items=1, description="Achievement bullet points")

    @field_validator("bullets")
    @classmethod
    def validate_bullets(cls, v: List[str]) -> List[str]:
        """Ensure all bullet points are non-empty."""
        return [bullet.strip() for bullet in v if bullet.strip()]

    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "company": "Tech Corp",
                "location": "San Francisco, CA",
                "position": "Senior Software Engineer",
                "start_date": "Jan 2020",
                "end_date": "Present",
                "bullets": [
                    "Led development of microservices architecture serving 10M+ users",
                    "Reduced API latency by 40% through optimization and caching strategies"
                ]
            }
        }


class Education(BaseModel):
    """
    Education entry for a resume.

    Attributes:
        institution: University or school name
        location: Geographic location
        degree: Degree type and major (e.g., "M.S. in Computer Science")
        start_date: Start date (formatted string)
        end_date: Graduation date or expected graduation date
    """

    institution: str = Field(..., min_length=1, description="School name")
    location: str = Field(..., min_length=1, description="Location")
    degree: str = Field(..., min_length=1, description="Degree and major")
    start_date: str = Field(..., min_length=1, description="Start date")
    end_date: str = Field(..., min_length=1, description="End date")

    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "institution": "George Mason University",
                "location": "Fairfax, VA",
                "degree": "M.S. in Computer Science",
                "start_date": "Aug 2018",
                "end_date": "May 2020"
            }
        }


class SkillGroup(BaseModel):
    """
    Grouped skill category for organizing technical skills.

    Attributes:
        name: Category name (e.g., "Languages", "Frameworks", "Tools")
        items: List of skills in this category
    """

    name: str = Field(..., min_length=1, description="Skill category name")
    items: List[str] = Field(..., min_items=1, description="List of skills")

    @field_validator("items")
    @classmethod
    def validate_items(cls, v: List[str]) -> List[str]:
        """Ensure all skill items are non-empty."""
        return [item.strip() for item in v if item.strip()]

    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "name": "Languages",
                "items": ["Python", "JavaScript", "TypeScript", "Java", "Go"]
            }
        }


class Project(BaseModel):
    """
    Project entry for a resume.

    Attributes:
        name: Project name
        bullets: List of project description and achievement bullet points
    """

    name: str = Field(..., min_length=1, description="Project name")
    bullets: List[str] = Field(..., min_items=1, description="Project bullet points")

    @field_validator("bullets")
    @classmethod
    def validate_bullets(cls, v: List[str]) -> List[str]:
        """Ensure all bullet points are non-empty."""
        return [bullet.strip() for bullet in v if bullet.strip()]

    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "name": "AI-Powered Job Search Assistant",
                "bullets": [
                    "Built full-stack application using React, Node.js, and MongoDB",
                    "Integrated OpenAI API for personalized job recommendations"
                ]
            }
        }


class Resume(BaseModel):
    """
    Complete resume data structure.

    Attributes:
        header: Resume header with name and contact info
        work_experience: List of work experience entries
        education: List of education entries
        skills: List of skill groups
        projects: List of project entries
    """

    header: ResumeHeader = Field(..., description="Resume header")
    work_experience: List[WorkExperience] = Field(
        ..., min_items=1, description="Work experience entries"
    )
    education: List[Education] = Field(..., min_items=1, description="Education entries")
    skills: List[SkillGroup] = Field(..., min_items=1, description="Skill groups")
    projects: List[Project] = Field(..., min_items=1, description="Project entries")

    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "header": {
                    "name": "John Doe",
                    "contact": ["john@email.com", "linkedin.com/in/johndoe"]
                },
                "work_experience": [],
                "education": [],
                "skills": [],
                "projects": []
            }
        }
