from typing import List

from github import Github
from github.Repository import Repository


class RepoContext:
    """
    Context manager for repository operations in GitHub Repo Sweeper.

    Handles listing, searching, and deleting repositories via the GitHub API.
    """

    def __init__(self, gh: Github) -> None:
        """
        Initialize the RepoContext.

        Args:
            gh (Github): An authenticated Github API client.
        """
        self.gh = gh
        self._to_delete: List[Repository] = []
        self._repos: List[Repository] = []

    def _get_repos(self) -> List[Repository]:
        """
        Retrieve all repositories for the authenticated user.

        Returns:
            List[Repository]: List of GitHub repositories.
        """
        if len(self._repos) == 0:
            print("Fetching repositories from GitHub API...")
            user = self.gh.get_user()
            self._repos = list(user.get_repos())

        return self._repos

    def _print_repo_names(self, repos: List[Repository]) -> None:
        """
        Print repository names and their main language.

        Args:
            repos (List[Repository]): List of GitHub repositories.
        """
        for i, repo in enumerate(repos, 1):
            print(f"{i}. {repo.full_name} [{repo.language}]")

    def list(self) -> None:
        """
        Print all repositories for the authenticated user.
        """

        repos = self._get_repos()
        if repos:
            self._print_repo_names(repos)
            self._delete(repos)
        else:
            print("No repositories found.")

    def search(self, keyword: str | None = None, language: str | None = None) -> None:
        """
        Search for repositories by keyword and/or programming language.

        Args:
            keyword (str, optional): Keyword to filter repository names.
            language (str, optional): Main language to filter repositories.
        """
        filtered_repos: List[Repository] = self._get_repos()
        if keyword:
            keyword = keyword.lower()
            filtered_repos = [
                r for r in filtered_repos if keyword in r.full_name.lower()
            ]

        if language:
            filtered_repos = [
                r
                for r in filtered_repos
                if r.language and r.language.lower() == language.lower()
            ]
        if filtered_repos:
            self._print_repo_names(filtered_repos)
            self._delete(filtered_repos)

        else:
            print("No matches found.")

    def _delete_by_index(self, repos: List[Repository]) -> None:
        """
        Prompt the user for repository indices to delete, and mark them for deletion.

        Args:
            repos (List[Repository]): List of repositories to choose from.
        """
        while True:
            index_str = input("Enter indices (e.g., 1,2,3 or 1-3,7-9): ").strip()
            indices: set[int] = set()

            try:
                # Parse comma-separated values and ranges
                for item in index_str.split(","):
                    item = item.strip()
                    if not item:
                        continue

                    if "-" in item:
                        start, end = map(int, item.split("-"))
                        if start < 1 or end > len(repos):
                            print(
                                f"Invalid range {start}-{end}. Indices must be between 1 and {len(repos)}."
                            )
                            continue
                        indices.update(range(start, end + 1))
                    else:
                        idx = int(item)
                        if idx < 1 or idx > len(repos):
                            print(
                                f"Invalid index {idx}. Must be between 1 and {len(repos)}."
                            )
                            continue
                        indices.add(idx)

                if not indices:
                    continue

                # Convert indices to repositories (adjust for 0-based indexing)
                self._to_delete = [repos[i - 1] for i in sorted(indices)]
                break

            except ValueError:
                print(
                    "Invalid input. Please enter numbers and ranges separated by commas only.\n"
                )

    def _delete_by_name(self, repos: List[Repository]) -> None:
        """
        Prompt the user for repository names to delete, and mark them for deletion.

        Args:
            repos (List[Repository]): List of repositories to choose from.
        """
        while True:  # keep prompting until at least one valid repo
            names = input(
                "Enter full repository names (e.g., username/repo1, username/repo2): "
            ).strip()

            if not names:
                print("No repository names provided. Please try again.\n")
                continue

            name_list = [name.strip() for name in names.split(",")]
            to_delete = []

            for name in name_list:
                matching_repos = [
                    repo for repo in repos if repo.full_name.lower() == name.lower()
                ]
                if matching_repos:
                    to_delete.extend(matching_repos)
                else:
                    print(f"Repository '{name}' not found in the list.")

            if not to_delete:
                print("No valid repositories found. Please try again.\n")
                continue

            # At least one valid repo found, store and exit
            self._to_delete = to_delete
            break

    def _confirm_delete(self, repos: List[Repository]) -> None:
        """
        Prompt the user for confirmation before deleting repositories.

        Args:
            repos (List[Repository]): List of repositories to delete.
        """
        print("\nYou are about to delete the following repositories:")
        for repo in self._to_delete:
            print(f"- {repo.full_name}")

        confirm = (
            input(
                "\nAre you sure? This action cannot be undone! Type 'yes' to confirm: "
            )
            .strip()
            .lower()
        )

        if confirm == "yes":
            for repo in self._to_delete:
                try:
                    repo.delete()
                    self._repos.remove(repo)
                    print(f"✓ Deleted {repo.full_name}")
                except Exception as e:
                    print(f"✗ Failed to delete {repo.full_name}: {e}")

        else:
            print("Deletion canceled.")

    def _delete(self, repos: List[Repository]) -> None:
        """
        Delete GitHub repositories either by indices or by repository names.

        Args:
            repos (List[Repository]): List of repositories to filter and delete.
        """

        print("\n=== Delete Repositories ===\n")

        while True:
            choice = input(
                "Delete options:\n"
                "1. Delete by indices (e.g. 1,2,3 or 1-3,7-9)\n"
                "2. Delete by names (e.g. repo1, username/repo2)\n"
                "3. Cancel\n"
                "> "
                #
            ).strip()

            if choice == "1":
                self._delete_by_index(repos)
                break
            elif choice == "2":
                self._delete_by_name(repos)
                break
            elif choice == "3":
                print("Deletion canceled.")
                return
            else:
                print("Invalid choice. Please enter 1, 2, or 3.\n")

        if self._to_delete:
            self._confirm_delete(repos)
