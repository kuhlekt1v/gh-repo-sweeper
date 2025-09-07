import getpass

import keyring

SERVICE_NAME = "github_repo_sweeper"
SYSTEM_USER = getpass.getuser()


def save_token(token) -> None:
    """
    Save the GitHub Personal Access Token (PAT) to the system keyring.

    Args:
        token (str): The GitHub personal access token to store.
    """
    keyring.set_password(SERVICE_NAME, SYSTEM_USER, token)


def load_token() -> str | None:
    """
    Load the GitHub Personal Access Token (PAT) from the system keyring.

    Returns:
        str: The stored GitHub token, or None if not found.
    """
    return keyring.get_password(SERVICE_NAME, SYSTEM_USER)
