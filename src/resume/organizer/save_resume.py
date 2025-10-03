"""
Organize tailored resumes by company and position.

This script helps maintain an organized archive of job applications by creating
dedicated folders for each company/position combination and copying resume files.
"""

import logging
from pathlib import Path
from typing import Optional
import shutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ResumeOrganizer:
    """
    Organize and archive tailored resumes by company and position.

    This class provides functionality to systematically save customized resumes
    in an organized folder structure for easy tracking of job applications.

    Attributes:
        base_folder: Base directory for storing application folders
        resume_source: Default source path for resume file
    """

    def __init__(
        self,
        base_folder: Optional[Path] = None,
        resume_source: Optional[Path] = None
    ):
        """
        Initialize resume organizer.

        Args:
            base_folder: Base directory for applications (default: ~/Documents/saved-applications)
            resume_source: Default resume file location (default: ~/Desktop/resume.pdf)
        """
        home = Path.home()
        self.base_folder = base_folder or (home / 'Documents' / 'saved-applications')
        self.resume_source = resume_source or (home / 'Desktop' / 'resume.pdf')

        # Ensure base folder exists
        self.base_folder.mkdir(parents=True, exist_ok=True)
        logger.info(f"Resume organizer initialized. Base folder: {self.base_folder}")

    def save_application(
        self,
        company_name: str,
        position: str,
        resume_path: Optional[Path] = None
    ) -> Path:
        """
        Create a folder and save resume for a job application.

        This method creates a dedicated folder for the application and copies
        the resume file into it, helping maintain an organized application archive.

        Args:
            company_name: Name of the company
            position: Job position title
            resume_path: Path to resume file (uses default if None)

        Returns:
            Path to the created application folder

        Raises:
            FileNotFoundError: If resume file doesn't exist

        Example:
            >>> organizer = ResumeOrganizer()
            >>> folder = organizer.save_application("TechCorp", "Software Engineer")
            >>> print(f"Application saved to: {folder}")
        """
        # Use default resume source if not provided
        source = resume_path or self.resume_source

        if not source.exists():
            raise FileNotFoundError(
                f"Resume file not found: {source}\n"
                f"Please ensure your resume is at the correct location or specify the path."
            )

        # Create folder name and path
        folder_name = f"{company_name}-{position}".replace('/', '-').replace('\\', '-')
        folder_path = self.base_folder / folder_name

        # Create application folder
        folder_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created application folder: {folder_path}")

        # Copy resume to folder
        destination = folder_path / source.name
        shutil.copy2(source, destination)
        logger.info(f"✓ Resume copied to: {destination}")

        print(f"✓ Application saved: {folder_name}")
        return folder_path


def main():
    """
    Interactive CLI for organizing resumes.

    Prompts the user for company names and positions, then creates organized
    folders with resume copies for each application.
    """
    print("=== Resume Organizer ===")
    print("Save your tailored resumes in an organized folder structure.\n")

    organizer = ResumeOrganizer()

    print(f"📁 Base folder: {organizer.base_folder}")
    print(f"📄 Default resume: {organizer.resume_source}")
    print("\nType 'exit' at any prompt to quit.\n")

    while True:
        try:
            print("Enter job application details:")

            company_name = input("  Company name: ").strip()
            if company_name.lower() == 'exit':
                break

            position = input("  Position: ").strip()
            if position.lower() == 'exit':
                break

            if not company_name or not position:
                print("⚠️  Both company name and position are required.\n")
                continue

            # Save application
            folder = organizer.save_application(company_name, position)
            print(f"✓ Saved to: {folder}\n")

        except FileNotFoundError as e:
            logger.error(f"Resume file not found: {e}")
            print(f"\n⚠️  Error: {e}\n")
            break

        except Exception as e:
            logger.error(f"Error saving application: {e}")
            print(f"\n⚠️  Error: {e}\n")
            continue

    print("\nGoodbye! 👋")


if __name__ == "__main__":
    main()
