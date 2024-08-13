# GitHub Repository Setup Automation

## Overview

This project automates the process of initializing a local Git repository, setting up a remote repository on GitHub, and pushing the initial commit.

Additional features:

- Create git repositories of old projects that have not been added to github yet via a directory search of folders the user can specify in the the .env file (Explained below in Setup)
- Allows the user to also make commits and edits to existing local git repos.
- It is designed to work seamlessly on both Windows Subsystem for Linux (WSL) and standard Linux environments.

## Prerequisites

Before using this script, ensure you have the following installed:

1. **Git:**

   - Install Git by following the instructions [here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

2. **GitHub CLI (gh):**

   - Install the GitHub CLI by following the instructions [here](https://docs.github.com/en/github-cli/github-cli/quickstart).

3. **Python:**

   - Ensure Python is installed. You can download it from [python.org](https://www.python.org/downloads/).

4. **termcolor (Python package):**

- Install termcolor using pip:

```bash {"id":"01J554C48QHGR2MSPNECEK83NE"}
pip install termcolor

```

5. **dotenv (Python package):**

- Install python-dotenv using pip:

```bash {"id":"01J554C48REGK8X2YC9BGDCH5A"}
pip install python-dotenv

```

6. **SSH Key:**

   - Ensure you have an SSH key generated and added to your GitHub account. Instructions can be found [here](https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh).

## Setup

1. **Clone the Repository:**

- Clone this repository to your local machine:

```bash {"id":"01J554C48REGK8X2YC9C33FKDJ"}
git clone git@github.com:YourUsername/YourRepository.git


```

2. **Environment Variables:**

- Create a `.env` file in the root of your project directory with the following content:

```dotenv {"id":"01J554C48REGK8X2YC9G2QW69A"}
// Github Token:
GITHUB_TOKEN=ghp_YourExampleToken1234567890abcdef1234567890abcdef

// Path if using WSL:
WSL_PATH1=/mnt/c/Users/yourusername/Desktop
WSL_PATH2=/mnt/c/Users/yourusername/Documents
WSL_PATH3=/mnt/c/Users/yourusername/Projects

// Path if using Git Bash or Command Prompt:
WIN_PATH1=C:\\Users\\yourusername\\Desktop
WIN_PATH2=C:\\Users\\yourusername\\Documents
WIN_PATH3=C:\\Users\\yourusername\\Projects


```

__Example of GITHUB_TOKEN:__

- The `GITHUB_TOKEN` is a Personal Access Token you generate from your GitHub account. It should look something like `ghp_YourExampleToken1234567890abcdef1234567890abcdef`. Keep this token secure and do not share it publicly.

3. **Configure Git:**

- Configure Git with your username and email:

```bash {"id":"01J554C48REGK8X2YC9JXH31WA"}
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"


```

## Path Searching

The script can search for the target directory in multiple base directories specified in your environment variables. This feature is useful for locating projects in different paths depending on your operating system.

- **For WSL (Windows Subsystem for Linux):**

   - The script uses paths specified by `WSL_PATH1`, `WSL_PATH2`, etc.

- **For Windows (Git Bash or Command Prompt):**

   - The script uses paths specified by `WIN_PATH1`, `WIN_PATH2`, etc.

Make sure to set these environment variables in the `.env` file. The script will ignore any path variables that are not set.

## Usage

1. **Run the Script:**

- Navigate to the project directory and run the script:

```bash {"id":"01J554C48REGK8X2YC9KQ4PFD4"}
python setup_git_repo.py

```

2. **Follow Prompts:**

   - Enter the directory name to search for (The DIRECTORY NAME not the folder path!!!).
   - Enter your GitHub email if prompted to generate an SSH key.
   - Enter the GitHub repository name (If the repo already exists, then type the repo name, if you type in the wrong thing then you need to exit this program and try again, This will be more robust in the future).
   - Enter a commit message (default: "Initial commit").
   - Enter the branch name to push to (default: master or main).

## Possible Use Cases

1. **Project Initialization:**

   - Quickly set up new projects with a Git repository and push them to GitHub without manual configuration.

2. **Classroom or Workshop Settings:**

   - Streamline the setup process for students or participants, ensuring everyone has a consistent starting point.

3. **Automated Backups:**

   - Use the script to automate the backup of local projects to GitHub, ensuring code is regularly pushed to a remote repository.

4. **Team Collaboration:**

   - Standardize the setup process for new team members, reducing the time and effort required to get everyone on the same page.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request with your changes. Fun fact this project was made using this script!

## Bugs and Issues

- Searching for local project folder only works if the user puts the local project folder name NOT the folder path. The script should be updated to accept both.
- If the repo already exists, if the user types in the wrong name, the script attempts to make a new repo under that name, this does fail however, it can create issues.
- For existing git repos the user can only "commit" and "push" changes to repos, more features like git reset, delete ammend commits etc. should be added
- (TBD, scope creep issue ??? ) maybe more collaborative team related features can be added, however at the moment this script is meant to streamline git repo initialization

## License and use of project code

This code must only be used and distributed with the persmission of the Author of this Repository. To contact the author email at: shah634@purdue.edu
