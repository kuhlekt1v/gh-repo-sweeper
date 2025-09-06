from github import Github
from github.Repository import Repository


class RepoContext:
    """Manage GitHub repository operations including listing, searching, and deletion."""

    def __init__(self, gh: Github) -> None:
        """Initialize repository context with GitHub client.
        
        Args:
            gh: Authenticated GitHub client instance.
        """
        self.gh = gh
        self._to_delete: list[Repository] = []
        self._available_repos: list[Repository] = []

    def _print_repo_names(self):
        """Print numbered list of available repositories with their languages."""
        for i, repo in enumerate(self._available_repos, 1):
            print(f"{i}. {repo.full_name} [{repo.language}]")

    def list(self) -> None:
        """List all repositories for the authenticated user and offer deletion options."""
        self._available_repos = list(self.gh.get_user().get_repos())
        self._print_repo_names()

        if self._available_repos:
            self._delete()

    def search(self, keyword: str | None = None, language: str | None = None) -> None:
        """Filter repositories by keyword and/or programming language.
        
        Args:
            keyword: Substring to match in repository full name (case-insensitive).
            language: Programming language to filter by (case-insensitive exact match).
        """
        results = self._available_repos

        if keyword:
            keyword = keyword.lower()
            results = [r for r in results if keyword in r.full_name.lower()]

        if language:
            results = [
                r
                for r in results
                if r.language and r.language.lower() == language.lower()
            ]

        if not results:
            print("No matches found.")
            return

        # Replace available_repos with filtered set
        self._available_repos = results
        self._print_repo_names()
        self._delete()

    def _delete_by_index(self):
        """Prompt user to select repositories for deletion by index numbers or ranges."""
        while True:
            index_str = input("Enter indices (e.g., 1,2,3 or 1-3,7-9): ").strip()
            indices = set()

            try:
                # Parse comma-separated values and ranges
                for item in index_str.split(","):
                    item = item.strip()
                    if not item:
                        continue

                    if "-" in item:
                        start, end = map(int, item.split("-"))
                        if start < 1 or end > len(self._available_repos):
                            print(
                                f"Invalid range {start}-{end}. Indices must be between 1 and {len(self._available_repos)}."
                            )
                            continue
                        indices.update(range(start, end + 1))
                    else:
                        idx = int(item)
                        if idx < 1 or idx > len(self._available_repos):
                            print(
                                f"Invalid index {idx}. Must be between 1 and {len(self._available_repos)}."
                            )
                            continue
                        indices.add(idx)

                if not indices:
                    continue

                # Convert indices to repositories (adjust for 0-based indexing)
                self._to_delete = [
                    self._available_repos[i - 1] for i in sorted(indices)
                ]
                break

            except ValueError:
                print(
                    "Invalid input. Please enter numbers and ranges separated by commas only.\n"
                )

    def _delete_by_name(self):
        """Prompt user to select repositories for deletion by full repository names."""
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
                    repo
                    for repo in self._available_repos
                    if repo.full_name.lower() == name.lower()
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

    def _confirm_delete(self):
        """Display selected repositories and confirm deletion with user."""
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
                    self._available_repos.remove(repo)
                    print(f"✓ Deleted {repo.full_name}")
                except Exception as e:
                    print(f"✗ Failed to delete {repo.full_name}: {e}")
        else:
            print("Deletion canceled.")

    def _delete(self):
        """Present deletion options and handle repository deletion workflow."""
        if not self._available_repos:
            print("No repositories to delete.")
            return

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
                self._delete_by_index()
                break
            elif choice == "2":
                self._delete_by_name()
                break
            elif choice == "3":
                print("Deletion canceled.")
                return
            else:
                print("Invalid choice. Please enter 1, 2, or 3.\n")

        if self._to_delete:
            self._confirm_delete()
