import getpass
import logging

from github import Auth, Github
from github.GithubException import BadCredentialsException, GithubException

from ..config import load_token, save_token

logger = logging.getLogger(__name__)


def _get_github_token() -> str:
    """
    Retrieve a GitHub Personal Access Token (PAT) from the system keyring or prompt the user.

    Returns:
        str: GitHub personal access token.

    Raises:
        ValueError: If no token is entered by the user.
    """
    token = load_token()
    if token:
        use_existing = input("Use existing saved PAT? (Y/n): ").strip().lower()
        if use_existing in ("", "y", "yes"):
            return token
    token = getpass.getpass("Enter your GitHub Personal Access Token: ")
    if input("Save token for future use? (y/N): ").strip().lower() == "y":
        save_token(token)
    return token


def initialize_github_auth() -> Github:
    """
    Initialize and validate GitHub authentication, returning an authenticated Github instance.

    Returns:
        Github: Authenticated Github instance.

    Raises:
        BadCredentialsException: If the provided token is invalid.
        GithubException: For other GitHub API errors.
        Exception: For unexpected errors.
    """
    token = _get_github_token()
    auth = Auth.Token(token)

    try:
        github_session = Github(auth=auth)
        login_user = github_session.get_user().login  # Test API call to validate auth
        print(f"\nAuthenicated as: {login_user}")
        return github_session
    except BadCredentialsException as e:
        logger.error(f" Authentication failed: ({e.status}) {e.message}")
        raise
    except GithubException as e:
        logger.error(f"GitHub API error: ({e.status}) {e.message}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error: ({type(e).__name__}) {e}")
        raise
