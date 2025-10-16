"""
GitHub repository creation and management module
Handles repo creation, file uploads, and GitHub Pages deployment
"""
import logging
import os
import subprocess
import tempfile
import shutil
import requests
from datetime import datetime
from github import Github, GithubException

logger = logging.getLogger(__name__)

# GitHub configuration
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')
GITHUB_USERNAME = os.environ.get('GITHUB_USERNAME', '')

def create_and_deploy_repo(task_name, app_code, brief, checks):
    """
    Create a GitHub repository, push code, and enable GitHub Pages

    Args:
        task_name (str): Name of the task (used for repo name)
        app_code (dict): Generated code files
        brief (str): Application brief
        checks (list): Validation checks

    Returns:
        dict: Repository information (repo_url, commit_sha, pages_url)
    """
    if not GITHUB_TOKEN:
        raise ValueError("GITHUB_TOKEN not configured")

    if not GITHUB_USERNAME:
        raise ValueError("GITHUB_USERNAME not configured")

    logger.info(f"Creating repository for task: {task_name}")

    # Initialize GitHub client
    g = Github(GITHUB_TOKEN)
    user = g.get_user()

    # Generate unique repo name
    repo_name = sanitize_repo_name(task_name)

    try:
        # Create the repository
        logger.info(f"Creating GitHub repository: {repo_name}")
        repo = user.create_repo(
            name=repo_name,
            description=f"Auto-generated application: {brief[:100]}",
            homepage="",
            private=False,
            has_issues=True,
            has_wiki=False,
            has_downloads=True,
            auto_init=False
        )

        logger.info(f"Repository created: {repo.html_url}")

        # Create and push files
        commit_sha = push_files_to_repo(repo, app_code, brief, checks)

        # Enable GitHub Pages
        pages_url = enable_github_pages(repo)

        return {
            'repo_url': repo.html_url,
            'commit_sha': commit_sha,
            'pages_url': pages_url
        }

    except GithubException as e:
        logger.error(f"GitHub API error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Failed to create repository: {str(e)}")
        raise

def sanitize_repo_name(task_name):
    """
    Convert task name to a valid GitHub repository name

    Args:
        task_name (str): Original task name

    Returns:
        str: Sanitized repository name
    """
    # Remove invalid characters
    repo_name = task_name.replace(' ', '-').replace('_', '-')
    repo_name = ''.join(c for c in repo_name if c.isalnum() or c == '-')

    # Ensure it doesn't start or end with a hyphen
    repo_name = repo_name.strip('-')

    # Ensure it's not too long
    if len(repo_name) > 100:
        repo_name = repo_name[:100]

    # Ensure it's not empty
    if not repo_name:
        repo_name = f"task-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"

    return repo_name

def push_files_to_repo(repo, app_code, brief, checks):
    """
    Push files to the GitHub repository using git commands

    Args:
        repo: GitHub repository object
        app_code (dict): Generated code files
        brief (str): Application brief
        checks (list): Validation checks

    Returns:
        str: Commit SHA
    """
    logger.info("Pushing files to repository")

    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    try:
        # Clone the repository
        clone_url = repo.clone_url.replace('https://', f'https://{GITHUB_TOKEN}@')
        subprocess.run(
            ['git', 'clone', clone_url, temp_dir],
            check=True,
            capture_output=True
        )

        # Configure git
        subprocess.run(
            ['git', 'config', 'user.email', 'bot@example.com'],
            cwd=temp_dir,
            check=True
        )
        subprocess.run(
            ['git', 'config', 'user.name', 'Deployment Bot'],
            cwd=temp_dir,
            check=True
        )

        # Write index.html
        if 'index.html' in app_code and app_code['index.html']:
            with open(os.path.join(temp_dir, 'index.html'), 'w', encoding='utf-8') as f:
                f.write(app_code['index.html'])
            logger.info("Created index.html")

        # Write README.md
        readme_content = app_code.get('README.md', generate_readme(brief, checks))
        with open(os.path.join(temp_dir, 'README.md'), 'w', encoding='utf-8') as f:
            f.write(readme_content)
        logger.info("Created README.md")

        # Write LICENSE
        license_content = get_mit_license()
        with open(os.path.join(temp_dir, 'LICENSE'), 'w', encoding='utf-8') as f:
            f.write(license_content)
        logger.info("Created LICENSE")

        # Add all files
        subprocess.run(
            ['git', 'add', '.'],
            cwd=temp_dir,
            check=True
        )

        # Commit
        subprocess.run(
            ['git', 'commit', '-m', 'Initial commit: Deploy generated application'],
            cwd=temp_dir,
            check=True
        )

        # Push
        subprocess.run(
            ['git', 'push', 'origin', 'main'],
            cwd=temp_dir,
            check=True,
            capture_output=True
        )

        # Get commit SHA
        result = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            cwd=temp_dir,
            check=True,
            capture_output=True,
            text=True
        )
        commit_sha = result.stdout.strip()

        logger.info(f"Files pushed successfully, commit SHA: {commit_sha}")
        return commit_sha

    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True)

def enable_github_pages(repo):
    """
    Enable GitHub Pages for the repository

    Args:
        repo: GitHub repository object

    Returns:
        str: GitHub Pages URL
    """
    logger.info("Enabling GitHub Pages")

    try:
        # Use the REST API directly to enable GitHub Pages
        # PyGithub doesn't have great support for Pages API
        url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo.name}/pages"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }

        data = {
            "source": {
                "branch": "main",
                "path": "/"
            }
        }

        response = requests.post(url, headers=headers, json=data)

        # Construct Pages URL
        pages_url = f"https://{GITHUB_USERNAME}.github.io/{repo.name}/"

        if response.status_code in [201, 204]:
            logger.info(f"GitHub Pages enabled: {pages_url}")
            return pages_url
        elif response.status_code == 409:
            # Pages already enabled
            logger.info("GitHub Pages already enabled")
            return pages_url
        else:
            logger.warning(f"GitHub Pages API returned {response.status_code}: {response.text}")
            # Return the URL anyway - Pages often enables automatically
            logger.info(f"Returning Pages URL anyway: {pages_url}")
            return pages_url

    except Exception as e:
        logger.error(f"Failed to enable GitHub Pages: {str(e)}")
        # Return the URL anyway, Pages might be enabled automatically
        pages_url = f"https://{GITHUB_USERNAME}.github.io/{repo.name}/"
        logger.info(f"Returning Pages URL anyway: {pages_url}")
        return pages_url

def generate_readme(brief, checks):
    """
    Generate a comprehensive README.md

    Args:
        brief (str): Application brief
        checks (list): Validation checks

    Returns:
        str: README content
    """
    checks_text = "\n".join([f"- {check}" for check in checks]) if checks else "No specific checks."

    readme = f"""# Generated Application

## Summary
This application was automatically generated and deployed using an LLM-based code deployment system.

**Brief:** {brief}

## Features
This application implements the following requirements:
{checks_text}

## Setup
No setup required! This is a static web application.

## Usage
1. Visit the GitHub Pages URL for this repository
2. The application will load automatically in your browser
3. Follow any on-screen instructions

## Technology Stack
- **Frontend:** HTML5, CSS3, JavaScript
- **Styling:** Bootstrap 5
- **Deployment:** GitHub Pages

## Code Explanation
This application was generated based on the provided brief and requirements. The code is structured as follows:

- **index.html:** Main application file containing HTML structure, embedded styles, and JavaScript logic
- **README.md:** This file, containing project documentation
- **LICENSE:** MIT License file

The application uses modern web technologies and follows best practices for:
- Responsive design
- Cross-browser compatibility
- User experience
- Code organization and readability

## Deployment
This application is automatically deployed to GitHub Pages. Any commits to the main branch will trigger a redeployment.

## License
MIT License

Copyright (c) {datetime.utcnow().year}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

*Generated by LLM Code Deployment System on {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC*
"""
    return readme

def get_mit_license():
    """
    Get MIT License text

    Returns:
        str: MIT License content
    """
    year = datetime.utcnow().year
    return f"""MIT License

Copyright (c) {year}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
