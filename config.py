import getpass

import keyring

SERVICE_NAME = "github_repo_sweeper"
SYSTEM_USER = getpass.getuser()


def save_token(token):
    keyring.set_password(SERVICE_NAME, SYSTEM_USER, token)


def load_token():
    return keyring.get_password(SERVICE_NAME, SYSTEM_USER)
