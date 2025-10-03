"""
Configuration management for the jobs-tools package.

This module handles environment variables, settings, and configuration
for email, resume, and scraping tools.
"""

from src.config.settings import Settings, get_settings

__all__ = ["Settings", "get_settings"]
