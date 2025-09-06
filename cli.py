import sys

from github.GithubException import BadCredentialsException, GithubException

from actions import RepoContext
from auth import initialize_github_auth


def main():
    """
    Main entry point for the GitHub Repository Sweeper CLI.
    """
    try:
        print("\n=== GitHub Repo Sweeper ===\n")
        print(
            "A lightweight utility for cleaning up your GitHub repositories.\n"
            "You can list repositories, search by name, and optionally delete\n"
            "repos you no longer need.\n"
        )

        gh = initialize_github_auth()
        repo_context = RepoContext(gh)

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
                repo_context.list()

            elif choice == "2":
                print("\n=== Search Repositories ===\n")
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
                        keyword = input(
                            "Enter search keyword (press Enter to skip): "
                        ).strip()

                    if search_type in ("2", "3"):
                        language = input(
                            "Enter programming language (press Enter to skip): "
                        ).strip()

                    if search_type in ("1", "2", "3"):
                        break
                    else:
                        print("Invalid selection. Enter 1, 2, or 3.")

                print("\nResults:\n")
                repo_context.search(keyword=keyword, language=language)

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
