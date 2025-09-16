import logging
import sys
from typing import List

from github.GithubException import BadCredentialsException, GithubException
from github.Repository import Repository

from gh_repo_sweeper.services.auth_service import initialize_github_auth
from gh_repo_sweeper.services.repo_service import RepoService


def _print_repo_names(repos: List[Repository]) -> None:
    """
    Print repository names and their main language.

    Args:
        repos (List[Repository]): List of GitHub repositories.
    """
    if not repos:
        print("No repositories found.")
    else:
        for i, repo in enumerate(repos, 1):
            print(f"{i}. {repo.full_name} [{repo.language}]")


def _prompt_search() -> tuple[str | None, str | None]:
    """
    Prompt for search keyword and programming language.

    Returns:
        Tuple of (keyword, language), each may be None.
    """
    keyword = None
    language = None
    while True:
        search_type = input(
            "Search options\n"
            "==========================\n"
            "1. Keyword\n"
            "2. Programming language\n"
            "3. Both\n"
            "> "
        )

        if search_type in ("1", "3"):
            keyword = input("Enter search keyword (press Enter to skip): ").strip()

        if search_type in ("2", "3"):
            language = input(
                "Enter programming language (press Enter to skip): "
            ).strip()

        if search_type in ("1", "2", "3"):
            return keyword, language
        else:
            print("Invalid selection. Enter 1, 2, or 3.")


def main() -> None:
    """
    Main entry point for the GitHub Repository Sweeper CLI.

    Handles user interaction, menu selection, and error logging.

    Raises:
        SystemExit: If authentication fails or an unrecoverable error occurs.
    """
    logging.basicConfig(
        filename="sweeper.log",
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    try:
        print("\n=== GitHub Repo Sweeper ===\n")
        print(
            "A lightweight utility for cleaning up your GitHub repositories.\n"
            "You can list repositories, search by name, and optionally delete\n"
            "repos you no longer need.\n"
        )

        gh = initialize_github_auth()
        service = RepoService(gh)

        while True:
            choice = input(
                "\nWhat would you like to do?\n"
                "==========================\n"
                "1. List all repositories\n"
                "2. Search for a repository\n"
                "3. Exit\n"
                "\n> "
            ).strip()

            if choice == "1":
                print("\n=== Your Repositories ===\n")
                repos = service.list()
                _print_repo_names(repos)

                if repos:
                    service.delete(repos)

            elif choice == "2":
                print("\n=== Search Repositories ===\n")
                keyword, language = _prompt_search()

                print("\nResults:\n")
                repos = service.search(keyword=keyword, language=language)
                _print_repo_names(repos)

                if repos:
                    service.delete(repos)

            elif choice == "3":
                print("Exiting GitHub Repo Sweeper. Press enter to exit...")
                break

            else:
                print("Invalid choice. Please try again.")

        gh.close()
        input("")

    except BadCredentialsException:
        print("\nAuthentication failed. Please check your GitHub token.")
        sys.exit(1)
    except GithubException as e:
        print(f"\nGitHub API error: ({e.status}) {e.data.get('message', e)}")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {type(e).__name__}: {e}")
