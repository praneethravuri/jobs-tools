"""
AI model integration for email content generation and rephrasing.

This module provides functionality to rephrase email content using Ollama AI models
for personalized and varied email outreach campaigns.
"""

import logging
from typing import Optional
import ollama
from src.config import get_settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OllamaClient:
    """
    Client for interacting with Ollama AI models.

    This class provides methods for rephrasing email content using local
    Ollama models to generate personalized variations.

    Attributes:
        client: Ollama client instance
        host: Ollama API host URL
    """

    def __init__(self, host: Optional[str] = None):
        """
        Initialize Ollama client.

        Args:
            host: Ollama API host URL. If None, loads from settings.
        """
        settings = get_settings()
        self.host = host or settings.ollama_host
        self.client = ollama.Client(host=self.host)
        logger.info(f"Initialized Ollama client with host: {self.host}")

    def rephrase_content(
        self,
        model_name: str,
        content: str,
        add_salutation: bool = True
    ) -> str:
        """
        Rephrase email content using an Ollama AI model.

        This method takes email content and uses an AI model to rephrase it
        while maintaining the core message. Useful for creating varied email
        campaigns without sounding repetitive.

        Args:
            model_name: Name of the Ollama model to use (e.g., 'phi3', 'llama2')
            content: Original email content to rephrase
            add_salutation: If False, removes common salutations from output

        Returns:
            Rephrased email content as a string

        Raises:
            Exception: If Ollama API call fails

        Example:
            >>> client = OllamaClient()
            >>> original = "Hi John, I'm interested in the role at your company."
            >>> rephrased = client.rephrase_content("phi3", original, False)
            >>> print(rephrased)
        """
        instruction = (
            "Please rephrase the following content without adding extra "
            "salutations and ensure there are no extra whitespaces: "
        )
        prompt = instruction + content

        try:
            logger.info(f"Rephrasing content using model: {model_name}")
            stream = self.client.chat(
                model=model_name,
                messages=[{'role': 'user', 'content': prompt}],
                stream=True,
            )

            response = ""
            for chunk in stream:
                response += chunk['message']['content']

            if not add_salutation:
                response = (
                    response
                    .replace("Best regards,", "")
                    .replace("Sincerely,", "")
                    .strip()
                )

            logger.info("Successfully rephrased content")
            return response

        except Exception as e:
            logger.error(f"Error rephrasing content: {e}")
            raise


# Create a global instance for backward compatibility
_settings = get_settings()
_default_client = OllamaClient()


def rephrase_content(
    model_name: str,
    content: str,
    add_salutation: bool = True
) -> str:
    """
    Convenience function for rephrasing content using the default Ollama client.

    Args:
        model_name: Name of the Ollama model to use
        content: Original email content to rephrase
        add_salutation: If False, removes common salutations from output

    Returns:
        Rephrased email content
    """
    return _default_client.rephrase_content(model_name, content, add_salutation)
