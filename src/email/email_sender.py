"""
SMTP email sending utilities with support for attachments.

This module provides a reusable EmailSender class for sending emails
via SMTP with optional file attachments.
"""

import smtplib
import logging
from pathlib import Path
from typing import Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from src.models.email import EmailConfig, EmailMessage
from src.config import get_settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailSender:
    """
    SMTP email sender with attachment support.

    This class handles SMTP connection management and email sending
    with support for both plain text emails and emails with attachments.

    Attributes:
        config: EmailConfig instance with SMTP settings
        server: Active SMTP server connection (when connected)
    """

    def __init__(self, config: Optional[EmailConfig] = None):
        """
        Initialize email sender with configuration.

        Args:
            config: EmailConfig instance. If None, loads from settings.
        """
        if config is None:
            settings = get_settings()
            config = EmailConfig(
                smtp_server=settings.smtp_server,
                smtp_port=settings.smtp_port,
                email_from=settings.email_from,
                password=settings.gmail_app_password
            )
        self.config = config
        self.server: Optional[smtplib.SMTP] = None

    def __enter__(self):
        """Context manager entry - connect to SMTP server."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - disconnect from SMTP server."""
        self.disconnect()

    def connect(self) -> None:
        """
        Establish connection to SMTP server.

        Raises:
            smtplib.SMTPException: If connection fails
        """
        try:
            logger.info(f"Connecting to SMTP server: {self.config.smtp_server}:{self.config.smtp_port}")
            self.server = smtplib.SMTP(self.config.smtp_server, self.config.smtp_port)
            self.server.starttls()
            self.server.login(self.config.email_from, self.config.password)
            logger.info("✓ Successfully connected to SMTP server")
        except Exception as e:
            logger.error(f"Failed to connect to SMTP server: {e}")
            raise

    def disconnect(self) -> None:
        """Disconnect from SMTP server if connected."""
        if self.server:
            try:
                self.server.quit()
                logger.info("✓ Disconnected from SMTP server")
            except Exception as e:
                logger.warning(f"Error disconnecting from SMTP server: {e}")
            finally:
                self.server = None

    def send_email(
        self,
        message: EmailMessage,
        from_email: Optional[str] = None
    ) -> bool:
        """
        Send a single email message.

        Args:
            message: EmailMessage instance with to, subject, body, and optional attachment
            from_email: Override sender email (uses config default if None)

        Returns:
            True if email sent successfully, False otherwise

        Example:
            >>> sender = EmailSender()
            >>> sender.connect()
            >>> msg = EmailMessage(
            ...     to_email="recipient@example.com",
            ...     subject="Test",
            ...     body="Hello!"
            ... )
            >>> sender.send_email(msg)
            >>> sender.disconnect()
        """
        if not self.server:
            raise RuntimeError("Not connected to SMTP server. Call connect() first.")

        try:
            from_email = from_email or self.config.email_from

            # Create MIME message
            mime_msg = MIMEMultipart()
            mime_msg['From'] = from_email
            mime_msg['To'] = message.to_email
            mime_msg['Subject'] = message.subject.replace('\n', ' ').replace('\r', '')

            # Attach body
            mime_msg.attach(MIMEText(message.body, 'plain'))

            # Attach file if specified
            if message.attachment_path:
                self._attach_file(mime_msg, message.attachment_path)

            # Send email
            logger.info(f"Sending email to: {message.to_email}")
            self.server.sendmail(from_email, message.to_email, mime_msg.as_string())
            logger.info(f"✓ Email sent to: {message.to_email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email to {message.to_email}: {e}")
            return False

    def _attach_file(self, mime_msg: MIMEMultipart, file_path: str) -> None:
        """
        Attach a file to a MIME message.

        Args:
            mime_msg: MIMEMultipart message to attach file to
            file_path: Path to file to attach

        Raises:
            FileNotFoundError: If file does not exist
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Attachment file not found: {file_path}")

        logger.info(f"Attaching file: {path.name}")

        with open(path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename={path.name}'
        )
        mime_msg.attach(part)
