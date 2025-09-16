from typing import List

from github.Repository import Repository

from .repo_selector import RepoSelector


class DeleteCommand:
    def __init__(self, repos: List[Repository]):
        self.repos = repos

    def _prompt_indices(self, selector: RepoSelector):
        while True:
            raw = input(
                "Enter indices (e.g., 1,2,3 or 1-3,7-9) OR press 'c' to cancel:\n> "
            ).strip()
            if raw.lower() == "c":
                print("Deletion canceled.")
                return []
            try:
                return selector.by_indices(raw)
            except ValueError as e:
                print(f"{e}\n")

    def _prompt_names(self, selector: RepoSelector):
        while True:
            raw = input(
                "Enter repo names (e.g., user/repo1, user/repo2) OR press 'c' to cancel:\n> "
            ).strip()
            if raw.lower() == "c":
                print("Deletion canceled.")
                return []
            try:
                return selector.by_names(raw)
            except ValueError as e:
                print(f"{e}\n")

    def _confirm(self, repos: List[Repository]):
        print("\nYou are about to delete the following repositories:")
        for repo in repos:
            print(f"- {repo.full_name}")
        return input("\nAre you sure? Type 'yes' to confirm: ").strip().lower() == "yes"

    def _delete(self, repos: List[Repository]):
        results = []
        for repo in repos:
            try:
                repo.delete()
                repos.remove(repo)
                results.append(f"✓ Deleted {repo.full_name}")
            except Exception as e:
                results.append(f"✗ Failed to delete {repo.full_name}: {e}")
        return results

    def run(self):
        selector = RepoSelector(self.repos)

        print("\n=== Delete Repositories ===\n")
        while True:
            choice = input(
                "Delete options:\n"
                "1. Delete by indices (e.g. 1,2,3 or 1-3,7-9)\n"
                "2. Delete by names (e.g. repo1, username/repo2)\n"
                "3. Cancel\n> "
            ).strip()

            if choice == "1":
                repos_to_delete = self._prompt_indices(selector)
            elif choice == "2":
                repos_to_delete = self._prompt_names(selector)
            elif choice == "3":
                print("Deletion canceled.")
                return
            else:
                print("Invalid choice.\n")
                continue

            if repos_to_delete and self._confirm(repos_to_delete):
                results = self._delete(repos_to_delete)
                for r in results:
                    print(r)
            break
