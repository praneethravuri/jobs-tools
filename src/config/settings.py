"""
Application settings and configuration management.

This module provides a centralized Settings class for managing environment
variables and application configuration using Pydantic settings management.
"""

import os
from functools import lru_cache
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    This class uses Pydantic settings management to load and validate
    configuration from environment variables and .env files.

    Attributes:
        gmail_app_password: Gmail application-specific password
        email_from: Sender email address
        smtp_server: SMTP server hostname
        smtp_port: SMTP server port
        ollama_host: Ollama API host URL for AI model inference
    """

    # Email configuration
    gmail_app_password: str = Field(
        ...,
        description="Gmail app-specific password",
        validation_alias="GMAIL_APP_PASSWORD"
    )
    email_from: str = Field(
        ...,
        description="Sender email address",
        validation_alias="EMAIL_FROM"
    )
    smtp_server: str = Field(
        default="smtp.gmail.com",
        description="SMTP server hostname",
        validation_alias="SMTP_SERVER"
    )
    smtp_port: int = Field(
        default=587,
        description="SMTP server port",
        validation_alias="SMTP_PORT"
    )

    # Ollama configuration for AI-generated emails
    ollama_host: str = Field(
        default="http://localhost:11434",
        description="Ollama API host URL",
        validation_alias="OLLAMA_HOST"
    )

    # Optional paths
    resume_path: Optional[str] = Field(
        default=None,
        description="Path to resume file",
        validation_alias="RESUME_PATH"
    )
    save_directory: Optional[str] = Field(
        default=None,
        description="Directory for saving applications",
        validation_alias="SAVE_DIRECTORY"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    """
    Get cached application settings instance.

    This function creates and caches a Settings instance, loading configuration
    from environment variables and .env file. The settings are cached to avoid
    repeated file I/O and environment variable lookups.

    Returns:
        Settings: Cached application settings instance

    Example:
        >>> settings = get_settings()
        >>> print(settings.email_from)
        'your.email@gmail.com'
    """
    return Settings()
