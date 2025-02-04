C:\mygit\BLazy\repo\rap\setup_project_dirs.py
Language detected: python
import os

def create_directory_structure():
    # Define the main directory path
    main_dir = '/repo/diss'

    # Create the main directory if it doesn't exist
    if not os.path.exists(main_dir):
        os.makedirs(main_dir)
        print(f"Main directory '{main_dir}' created successfully.")

    # Define the subdirectories
    subdirectories = [
        'analysis',
        'best_lines',
        'feedback',
        'lyrics',
        'personas',
        'planning',
        'research',
        'structure',
        'submissions'
    ]

    # Create each subdirectory if it doesn't exist
    for subdirectory in subdirectories:
        subdirectory_path = os.path.join(main_dir, subdirectory)
        if not os.path.exists(subdirectory_path):
            os.makedirs(subdirectory_path)
            print(f"Subdirectory '{subdirectory}' created successfully.")
        else:
            print(f"Subdirectory '{subdirectory}' already exists.")

if __name__ == '__main__':
    create_directory_structure()
C:\mygit\BLazy\repo\rap\setup_project_dirs.py
Language detected: python
import os

def create_project_directory_structure():
    # Define the main directory path
    main_dir = "C:/mygit/BLazy/repo/rap/diss"

    # Create the main directory if it doesn't exist
    try:
        os.makedirs(main_dir, exist_ok=True)
        print(f"Main directory '{main_dir}' created successfully.")
    except OSError as e:
        print(f"Error creating main directory '{main_dir}': {e}")

    # Define the subdirectory names
    subdirectories = [
        "analysis",
        "best_lines",
        "feedback",
        "lyrics",
        "personas",
        "planning",
        "research",
        "structure",
        "submissions"
    ]

    # Create each subdirectory if it doesn't exist
    for subdirectory in subdirectories:
        subdirectory_path = os.path.join(main_dir, subdirectory)
        try:
            os.makedirs(subdirectory_path, exist_ok=True)
            print(f"Subdirectory '{subdirectory}' created successfully.")
        except OSError as e:
            print(f"Error creating subdirectory '{subdirectory}': {e}")

    print("Project directory structure created successfully.")

if __name__ == "__main__":
    create_project_directory_structure()
