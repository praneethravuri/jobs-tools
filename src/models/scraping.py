"""
Scraping-related Pydantic models for H1B company data.

This module provides models for company information scraped from H1B sponsorship
data sources. Used for validating and structuring scraped company data.
"""

from typing import Optional
from pydantic import BaseModel, Field, field_validator


class H1BCompany(BaseModel):
    """
    Company information from H1B visa sponsorship database.

    Attributes:
        rank: Company ranking by number of H1B filings
        company_name: Official company name
        approvals: Number of approved H1B petitions
        denials: Number of denied H1B petitions (optional)
        average_salary: Average salary for H1B positions (optional)
        location: Primary company location (optional)
    """

    rank: Optional[int] = Field(None, ge=1, description="Company rank by H1B filings")
    company_name: str = Field(..., min_length=1, description="Company name")
    approvals: Optional[int] = Field(None, ge=0, description="Number of approvals")
    denials: Optional[int] = Field(None, ge=0, description="Number of denials")
    average_salary: Optional[str] = Field(None, description="Average salary")
    location: Optional[str] = Field(None, description="Company location")

    @field_validator("company_name")
    @classmethod
    def clean_company_name(cls, v: str) -> str:
        """Clean and normalize company name."""
        return v.strip()

    @property
    def total_petitions(self) -> int:
        """Calculate total H1B petitions filed."""
        approvals = self.approvals or 0
        denials = self.denials or 0
        return approvals + denials

    @property
    def approval_rate(self) -> float:
        """Calculate H1B approval rate as percentage."""
        total = self.total_petitions
        if total == 0:
            return 0.0
        return (self.approvals or 0) / total * 100

    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "rank": 1,
                "company_name": "Cognizant Technology Solutions",
                "approvals": 15000,
                "denials": 500,
                "average_salary": "$85,000",
                "location": "Teaneck, NJ"
            }
        }
