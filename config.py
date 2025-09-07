"""Configuration module for GitHub Repository Sweeper.

Handles secure storage and retrieval of GitHub Personal Access Tokens
using the system keyring for persistent authentication across sessions.
"""

import getpass

import keyring

SERVICE_NAME = "github_repo_sweeper"
SYSTEM_USER = getpass.getuser()


def save_token(token):
    """Save GitHub Personal Access Token to system keyring.
    
    Args:
        token: GitHub Personal Access Token to store securely.
    """
    keyring.set_password(SERVICE_NAME, SYSTEM_USER, token)


def load_token():
    """Load GitHub Personal Access Token from system keyring.
    
    Returns:
        str or None: The stored GitHub token if found, None otherwise.
    """
    return keyring.get_password(SERVICE_NAME, SYSTEM_USER)
