import getpass
import logging

from github import Auth, Github
from github.GithubException import BadCredentialsException, GithubException

from config import load_token, save_token

logger = logging.getLogger(__name__)


def _get_github_token() -> str:
    """
    Retrieve a GitHub personal access token from saved storage or user input.

    This function first attempts to load a previously saved token. If a token
    exists, it asks the user whether to use it. If no token exists or the user
    chooses not to use the saved token, it prompts for a new token and offers
    to save it for future use.

    Returns:
        str: The GitHub personal access token to use for authentication.

    Raises:
        Exception: If authentication fails or the token is invalid, with status code and message.
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
    """Initialize and validate GitHub authentication, returning a ready-to-use GitHub session.

    Returns:
        Github: A fully authenticated Github instance ready for API operations.

    Raises:
        Exception: If authentication fails or the token is invalid.
    """
    token = _get_github_token()
    auth = Auth.Token(token)

    # Create and validate Github session
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
