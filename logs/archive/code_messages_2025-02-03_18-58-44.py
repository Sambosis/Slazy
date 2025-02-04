C:\mygit\BLazy\repo\blazie2\setup_repo.py
Language detected: python
# Import the git module from gitpython
from git import Repo
import os

def clone_and_checkout(repository_url, branch_name):
    # Set up the repository URL and branch name
    repository_url = repository_url
    branch_name = branch_name
    
    # Get the repository name from the repository URL
    repository_name = os.path.basename(repository_url).split('.')[0]
    
    # Clone the repository if it doesn't exist
    try:
        print(f"Cloning repository {repository_name}...")
        Repo.clone_from(repository_url, repository_name)
        print(f"Repository {repository_name} cloned successfully.")
    except:
        print(f"Repository {repository_name} already exists.")
    
    # Change into the repository directory
    print(f"Changing into repository directory {repository_name}...")
    os.chdir(repository_name)
    
    # Checkout the specified branch
    try:
        print(f"Checking out branch {branch_name}...")
        repo = Repo()
        repo.git.checkout(branch_name)
        print(f"Branch {branch_name} checked out successfully.")
    except:
        print(f"Branch {branch_name} does not exist.")

# Set up the repository URL and branch name
repository_url = "https://github.com/sambosis/BLazy.git"
branch_name = "idkhere"

# Call the clone_and_checkout function
clone_and_checkout(repository_url, branch_name)
