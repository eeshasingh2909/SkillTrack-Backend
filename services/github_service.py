import requests
from urllib.parse import urlparse
from models.skill import Skill
from app import db

GITHUB_API = "https://api.github.com"

REQUEST_TIMEOUT = 10


class GitHubAPIError(Exception):
    """Raised when the GitHub API cannot provide the requested data."""
    pass


def extract_github_username(github_url):
    """
    Extract the GitHub username from a GitHub profile URL.

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

    hostname = (parsed.hostname or "").lower()

    if hostname not in {"github.com", "www.github.com"}:
        return None

    parts = [
        part
        for part in parsed.path.strip("/").split("/")
        if part
    ]

    if not parts:
        return None

    return parts[0]


def get_user_repositories(username):
    """
    Get public repositories owned by a GitHub user.

    Returns a list of repository objects.
    """

    repositories = []

    page = 1

    while True:
        url = f"{GITHUB_API}/users/{username}/repos"

        try:
            response = requests.get(
                url,
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

        if response.status_code == 404:
            raise GitHubAPIError(
                "GitHub user not found"
            )

        if response.status_code == 403:
            raise GitHubAPIError(
                "GitHub API rate limit exceeded"
            )

        if response.status_code != 200:
            raise GitHubAPIError(
                f"GitHub API returned status {response.status_code}"
            )

        page_data = response.json()

        if not page_data:
            break

        repositories.extend(page_data)

        if len(page_data) < 100:
            break

        page += 1

    return repositories


def get_repository_languages(owner, repository):
    """
    Get programming languages detected by GitHub
    for a specific repository.
    """

    url = f"{GITHUB_API}/repos/{owner}/{repository}/languages"

    try:
        response = requests.get(
            url,
            timeout=REQUEST_TIMEOUT,
        )
    except requests.RequestException as exc:
        raise GitHubAPIError(
            "Unable to connect to GitHub"
        ) from exc

    if response.status_code == 404:
        return {}

    if response.status_code == 403:
        raise GitHubAPIError(
            "GitHub API rate limit exceeded"
        )

    if response.status_code != 200:
        raise GitHubAPIError(
            f"GitHub language API returned status "
            f"{response.status_code}"
        )

    return response.json()


def extract_github_skills(username):
    """
    Extract unique programming languages from
    all public repositories owned by the user.
    """

    repositories = get_user_repositories(username)

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

def save_github_skills(user_id, github_skills):
    """
    Save GitHub-derived skills for a user.

    Existing skills are preserved.
    Only skills that do not already exist are inserted.

    Returns a list containing the newly added skill names.
    """

    existing_skills = Skill.query.filter_by(
        user_id=user_id
    ).all()

    existing_skill_names = {
        skill.skill_name.lower()
        for skill in existing_skills
    }

    new_skills = []

    for skill_name in github_skills:

        normalized_name = skill_name.strip()

        if not normalized_name:
            continue

        if normalized_name.lower() in existing_skill_names:
            continue

        skill = Skill(
            user_id=user_id,
            skill_name=normalized_name
        )

        db.session.add(skill)

        new_skills.append(normalized_name)

        existing_skill_names.add(
            normalized_name.lower()
        )

    db.session.commit()

    return new_skills