import os
import requests

from dotenv import load_dotenv
from urllib.parse import urlparse

from models.skill import Skill
from models.project import Project
from models import db


# --------------------------------------------------
# Environment configuration
# --------------------------------------------------

load_dotenv()

GITHUB_API = "https://api.github.com"

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

REQUEST_TIMEOUT = 10


# --------------------------------------------------
# GitHub API headers
# --------------------------------------------------

GITHUB_HEADERS = {
    "Accept": "application/vnd.github+json"
}

if GITHUB_TOKEN:
    GITHUB_HEADERS["Authorization"] = (
        f"Bearer {GITHUB_TOKEN}"
    )


# --------------------------------------------------
# Custom GitHub error
# --------------------------------------------------

class GitHubAPIError(Exception):
    """
    Raised when GitHub API cannot provide
    the requested data.
    """
    pass


# --------------------------------------------------
# Extract GitHub username from profile URL
# --------------------------------------------------

def extract_github_username(github_url):
    """
    Extract GitHub username from a GitHub profile URL.

    Examples:

    https://github.com/octocat
    -> octocat

    https://github.com/octocat/
    -> octocat

    https://www.github.com/octocat
    -> octocat
    """

    if not github_url:
        return None

    github_url = github_url.strip()

    try:
        parsed = urlparse(github_url)
    except Exception:
        return None

    hostname = (
        parsed.hostname or ""
    ).lower()

    if hostname not in {
        "github.com",
        "www.github.com"
    }:
        return None

    parts = [
        part
        for part in parsed.path
        .strip("/")
        .split("/")
        if part
    ]

    if not parts:
        return None

    return parts[0]


# --------------------------------------------------
# Handle GitHub API errors
# --------------------------------------------------

def handle_github_error(response):
    """
    Convert GitHub HTTP errors into
    application-friendly errors.
    """

    if response.status_code == 401:
        raise GitHubAPIError(
            "GitHub authentication failed. "
            "Please check the GitHub token."
        )

    if response.status_code == 404:
        raise GitHubAPIError(
            "GitHub user or repository not found"
        )

    if response.status_code == 403:

        remaining = response.headers.get(
            "X-RateLimit-Remaining"
        )

        if remaining == "0":
            raise GitHubAPIError(
                "GitHub API rate limit exceeded. "
                "Please try again later."
            )

        raise GitHubAPIError(
            "GitHub API access forbidden"
        )

    if response.status_code != 200:
        raise GitHubAPIError(
            f"GitHub API returned status "
            f"{response.status_code}"
        )


# --------------------------------------------------
# Get all public repositories
# --------------------------------------------------

def get_user_repositories(username):
    """
    Get all public repositories owned
    by a GitHub user.

    Handles pagination automatically.
    """

    repositories = []

    page = 1

    while True:

        url = (
            f"{GITHUB_API}/users/"
            f"{username}/repos"
        )

        try:

            response = requests.get(
                url,
                headers=GITHUB_HEADERS,
                params={
                    "per_page": 100,
                    "page": page,
                    "type": "owner",
                },
                timeout=REQUEST_TIMEOUT,
            )

        except requests.RequestException as exc:

            raise GitHubAPIError(
                "Unable to connect to GitHub"
            ) from exc

        handle_github_error(response)

        page_data = response.json()

        if not page_data:
            break

        repositories.extend(page_data)

        if len(page_data) < 100:
            break

        page += 1

    return repositories


# --------------------------------------------------
# Get languages for one repository
# --------------------------------------------------

def get_repository_languages(owner, repository):
    """
    Get programming languages detected
    by GitHub for a repository.
    """

    url = (
        f"{GITHUB_API}/repos/"
        f"{owner}/{repository}/languages"
    )

    try:

        response = requests.get(
            url,
            headers=GITHUB_HEADERS,
            timeout=REQUEST_TIMEOUT,
        )

    except requests.RequestException as exc:

        raise GitHubAPIError(
            "Unable to connect to GitHub"
        ) from exc

    handle_github_error(response)

    return response.json()


# --------------------------------------------------
# Extract GitHub skills
# --------------------------------------------------

def extract_github_skills(username):
    """
    Extract unique programming languages
    from all public repositories.
    """

    repositories = get_user_repositories(
        username
    )

    skills = set()

    for repository in repositories:

        owner = repository["owner"]["login"]

        repository_name = repository["name"]

        languages = get_repository_languages(
            owner,
            repository_name
        )

        for language in languages.keys():

            skills.add(language)

    return sorted(skills)


# --------------------------------------------------
# Extract GitHub projects
# --------------------------------------------------

def extract_github_projects(username):
    """
    Extract project information from
    public GitHub repositories.
    """

    repositories = get_user_repositories(
        username
    )

    projects = []

    for repository in repositories:

        project = {
            "name": repository.get("name"),
            "description": repository.get(
                "description"
            ),
            "github_url": repository.get(
                "html_url"
            ),
            "language": repository.get(
                "language"
            )
        }

        projects.append(project)

    return projects


# --------------------------------------------------
# Save GitHub skills
# --------------------------------------------------

def save_github_skills(user_id, github_skills):
    """
    Save GitHub-derived skills.

    Existing skills are preserved.
    Duplicate skills are skipped.
    """

    existing_skills = Skill.query.filter_by(
        user_id=user_id
    ).all()

    existing_skill_names = {
        skill.skill_name.lower()
        for skill in existing_skills
        if skill.skill_name
    }

    new_skills = []

    for skill_name in github_skills:

        normalized_name = skill_name.strip()

        if not normalized_name:
            continue

        if (
            normalized_name.lower()
            in existing_skill_names
        ):
            continue

        skill = Skill(
            user_id=user_id,
            skill_name=normalized_name
        )

        db.session.add(skill)

        new_skills.append(
            normalized_name
        )

        existing_skill_names.add(
            normalized_name.lower()
        )

    db.session.commit()

    return new_skills


# --------------------------------------------------
# Save GitHub projects
# --------------------------------------------------

def save_github_projects(user_id, github_projects):
    """
    Save GitHub repositories as projects.

    Duplicate GitHub links are skipped.
    """

    existing_projects = Project.query.filter_by(
        user_id=user_id
    ).all()

    existing_github_links = {
        project.github_link
        for project in existing_projects
        if project.github_link
    }

    new_projects = []

    for project_data in github_projects:

        github_link = project_data.get(
            "github_url"
        )

        if not github_link:
            continue

        # Prevent duplicate projects
        if github_link in existing_github_links:
            continue

        project = Project(
            user_id=user_id,

            project_name=project_data.get(
                "name"
            ),

            description=project_data.get(
                "description"
            ),

            technology=project_data.get(
                "language"
            ),

            github_link=github_link,

            demo_link=None
        )

        db.session.add(project)

        new_projects.append({
            "name": project.project_name,
            "github_url": project.github_link,
            "language": project.technology
        })

        existing_github_links.add(
            github_link
        )

    db.session.commit()

    return new_projects