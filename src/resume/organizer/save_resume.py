import os
import shutil

def create_folder_and_duplicate_resume(company_name, position):
    # Define the path for the base folder where applications will be saved.
    base_folder_path = os.path.join(os.path.expanduser('~'), 'Documents', 'saved-applications')

    # Combine company name and position to form the folder name.
    folder_name = f"{company_name}-{position}"
    folder_path = os.path.join(base_folder_path, folder_name)

    # Define the path of the resume file on the desktop.
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    resume_file = os.path.join(desktop_path, 'praneeth_ravuri_resume.pdf')
    destination_file = os.path.join(folder_path, 'praneeth_ravuri_resume.pdf')

    # Ensure the base folder exists.
    os.makedirs(base_folder_path, exist_ok=True)
    # Create the specific application folder.
    os.makedirs(folder_path, exist_ok=True)

    # Copy the resume file to the new folder.
    shutil.copy(resume_file, destination_file)

    print(f"Folder '{folder_name}' created in Documents/saved-applications, and resume duplicated successfully.")

def main():
    while True:
        print("Enter the company name and position (or type 'exit' to quit):")
        company_name = input("Company name: ")
        if company_name.lower() == 'exit':
            break
        position = input("Position: ")
        if position.lower() == 'exit':
            break

        create_folder_and_duplicate_resume(company_name, position)

if __name__ == "__main__":
    main()
