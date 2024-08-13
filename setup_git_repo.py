import os
import subprocess
import json
from datetime import datetime
from collections import deque
from typing import Optional, List
from termcolor import cprint
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_paths_to_search() -> List[str]:
    if os.name == 'posix' and 'microsoft' in os.uname().release.lower():
        # Running in WSL
        print("Running WSL\n")
        paths = [
            os.getenv("WSL_PATH1"),
            os.getenv("WSL_PATH2"),
            os.getenv("WSL_PATH3"),
            os.getenv("WSL_PATH4"),
            os.getenv("WSL_PATH5"),
            os.getenv("WSL_PATH6"),
            os.getenv("WSL_PATH7"),
        ]
    else:
        # Running in Git Bash or Command Prompt
        print("Running Bash\n")
        paths = [
            os.getenv("WIN_PATH1"),
            os.getenv("WIN_PATH2"),
            os.getenv("WIN_PATH3"),
            os.getenv("WIN_PATH4"),
            os.getenv("WIN_PATH5"),
            os.getenv("WIN_PATH6"),
            os.getenv("WIN_PATH7"),
        ]
    return [path for path in paths if path]  # Remove None values

def search_directory(target_dir_name: str, paths: List[str]) -> Optional[str]:
    for base_path in paths:
        cprint(f"Searching in base directory: {base_path}", "white")
        if not os.path.exists(base_path):
            cprint(f"Base directory does not exist: {base_path}", "red")
            continue
        
        # Use deque for efficient pops from the left
        queue = deque([base_path])
        
        while queue:
            current_path = queue.popleft()
            try:
                with os.scandir(current_path) as it:
                    for entry in it:
                        if entry.is_dir(follow_symlinks=False):
                            if entry.name == target_dir_name:
                                found_path = entry.path
                                cprint(f"\nTarget directory found: {found_path}", "green")
                                return found_path
                            queue.append(entry.path)
            except PermissionError:
                cprint(f"Permission denied: {current_path}", "red")
    
    cprint(f"Directory '{target_dir_name}' does not exist.", "red")
    return None

def read_input(prompt: str) -> str:
    return input(prompt)

def check_gh_auth():
    result = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True)
    if "You are not logged into any GitHub hosts" in result.stderr:
        cprint("You are not logged into GitHub CLI. Logging in now...", "yellow")
        subprocess.run(["gh", "auth", "login", "--with-token"], input=os.getenv('GITHUB_TOKEN'), text=True, check=True)

def setup_ssh():
    ssh_key_path = os.path.expanduser("~/.ssh/id_ed25519")
    ssh_pub_key_path = f"{ssh_key_path}.pub"

    # Check if SSH key already exists
    if not os.path.exists(ssh_key_path):
        cprint("SSH key not found. Generating a new SSH key.", "yellow")
        email = read_input("Enter your GitHub email: ")
        subprocess.run(["ssh-keygen", "-t", "ed25519", "-C", email, "-f", ssh_key_path, "-N", ""])

    # Ensure SSH agent is running and add the SSH key to it
    cprint("Adding SSH key to the SSH agent.", "white")
    start_ssh_agent()
    subprocess.run(["ssh-add", ssh_key_path])

    # Display the public key
    with open(ssh_pub_key_path, "r") as pub_key_file:
        pub_key = pub_key_file.read()
        cprint(f"\nCopy the following SSH key and add it to your GitHub account:\n{pub_key}", "green")

    cprint("\nGo to GitHub Settings -> SSH and GPG keys -> New SSH key, and add the key there.", "white")
    input("Press Enter after you have added the SSH key to GitHub.")

def start_ssh_agent():
    result = subprocess.run(["ssh-agent"], capture_output=True, text=True, shell=True)
    if result.returncode == 0:
        agent_info = result.stdout.strip()
        with open(os.path.expanduser("~/.ssh/ssh-agent-info"), "w") as f:
            f.write(agent_info)
        subprocess.run(["source ~/.ssh/ssh-agent-info"], shell=True)
        subprocess.run(["ssh-add -l"], shell=True)
    else:
        cprint("Could not start the SSH agent.", "red")
        exit(1)

def get_github_username() -> str:
    result = subprocess.run(["gh", "api", "user"], capture_output=True, text=True)
    if result.returncode != 0:
        cprint("Failed to get GitHub username", "red")
        exit(1)
    user_data = json.loads(result.stdout)
    return user_data["login"]

def create_github_repo(repo_name: str, username: str):
    cprint(f"Creating GitHub repository '{repo_name}'", "white")
    result = subprocess.run(["gh", "repo", "create", repo_name, "--public", "--confirm"], capture_output=True, text=True)
    if result.returncode == 0:
        cprint(f"GitHub repository '{repo_name}' created.", "green")
    elif "Name already exists on this account" in result.stderr:
        cprint(f"Repository '{repo_name}' already exists on this account.", "yellow")
    else:
        cprint(f"Error creating GitHub repository: {result.stderr}", "red")
        exit(1)

def initialize_git_repo(project_dir: str, repo_name: str, username: str):
    os.chdir(project_dir)
    cprint(f"Changed directory to: {project_dir}", "white")

    if not os.path.isdir(".git"):
        cprint(f"Initializing git repository in {project_dir}", "white")
        subprocess.run(["git", "init"], check=True)
    
    # Check if remote origin already exists
    result = subprocess.run(["git", "remote"], capture_output=True, text=True)
    remotes = result.stdout.strip().split()
    git_repo = f"git@github.com:{username}/{repo_name}.git"
    
    if "origin" in remotes:
        cprint("Remote origin already exists. Updating URL.", "yellow")
        subprocess.run(["git", "remote", "set-url", "origin", git_repo], check=True)
    else:
        subprocess.run(["git", "remote", "add", "origin", git_repo], check=True)
    
    # Verify remote URL
    result = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True)
    if result.stdout.strip() != git_repo:
        cprint(f"Error setting remote URL: {result.stderr}", "red")
        exit(1)
    
    cprint("Git repository initialized and remote set.", "green")

def commit_and_push_changes(project_dir: str, repo_name: str, username: str):
    os.chdir(project_dir)
    cprint("Adding changes to git...", "white")
    subprocess.run(["git", "add", "."], check=True)

    # Commit message
    default_commit_msg = "Initial commit"
    commit_msg = read_input(f"Enter commit message (default: '{default_commit_msg}'): ") or default_commit_msg

    # Commit changes
    cprint("Committing changes...", "white")
    result = subprocess.run(["git", "commit", "-m", commit_msg], capture_output=True, text=True)
    if result.returncode == 0:
        cprint("Changes committed.", "green")
    else:
        cprint("No changes to commit.", "yellow")
        exit(0)

    # Get the branch name from the user
    default_branch = "main" if branch_exists("main") else "master"
    git_branch = read_input(f"Enter the branch name to push to (default: {default_branch}): ") or default_branch

    # Push changes to remote repository
    cprint("Pushing changes to remote repository for the first time...", "white")
    result = subprocess.run(["git", "push", "-u", "origin", git_branch], capture_output=True, text=True)
    if result.returncode == 0:
        cprint(f"Changes pushed successfully on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "green")
    else:
        if "Repository not found" in result.stderr:
            cprint("Repository not found. Verifying repository existence and access rights.", "red")
            subprocess.run(["gh", "repo", "view", f"{username}/{repo_name}"], check=True)
            cprint("Retrying to push changes...", "yellow")
            result = subprocess.run(["git", "push", "-u", "origin", git_branch], capture_output=True, text=True)
            if result.returncode == 0:
                cprint(f"Changes pushed successfully on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "green")
            else:
                cprint("Error: Failed to push changes to remote repository.", "red")
                cprint(result.stderr, "red")
                exit(1)
        else:
            cprint("Error: Failed to push changes to remote repository.", "red")
            cprint(result.stderr, "red")
            exit(1)

def branch_exists(branch_name: str) -> bool:
    result = subprocess.run(["git", "rev-parse", "--verify", branch_name], capture_output=True, text=True)
    return result.returncode == 0

def main():
    target_dir_name = read_input("Enter the directory name to search for: ")
    paths_to_search = get_paths_to_search()
    cprint("Starting search in the following base directories:", "white")
    for path in paths_to_search:
        cprint(path, "white")
    
    found_path = search_directory(target_dir_name, paths_to_search)
    if found_path:
        cprint(f"Target directory found at: {found_path}", "green")
        check_gh_auth()  # Ensure GitHub CLI is authenticated
        setup_ssh()  # Ensure SSH setup is complete
        repo_name = read_input("Enter the GitHub repository name: ")
        username = get_github_username()
        create_github_repo(repo_name, username)
        initialize_git_repo(found_path, repo_name, username)
        commit_and_push_changes(found_path, repo_name, username)
    else:
        cprint(f"Directory '{target_dir_name}' does not exist.", "red")

if __name__ == "__main__":
    main()
