from typing import List

from github import Github
from github.Repository import Repository

from gh_repo_sweeper.models.delete_result import DeleteResult

from .delete_command import DeleteCommand


class RepoService:
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
        self._repos: List[Repository] = []

    def list(self) -> List[Repository]:
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

    def search(
        self, keyword: str | None = None, language: str | None = None
    ) -> List[Repository]:
        """
        Search for repositories by keyword and/or programming language.

        Args:
            keyword (str, optional): Keyword to filter repository names.
            language (str, optional): Main language to filter repositories.

        Returns:
            List[Repository]: List of GitHub repositories.
        """

        filtered_repos: List[Repository] = self.list()
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

        return filtered_repos

    def delete(self, repos: List[Repository]) -> DeleteResult | None:
        results = DeleteCommand(repos).run()
        if results:
            self._repos = [
                repo
                for repo in self._repos
                if repo.name not in [r.name for r in results["success"]]
            ]

        return results
