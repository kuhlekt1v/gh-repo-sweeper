from typing import List

from github.Repository import Repository


class RepoSelector:
    def __init__(self, repos: List[Repository]):
        self.repos = repos

    def by_names(self, names_str: str) -> List[Repository]:
        if not names_str:
            raise ValueError("No repository names provided.")

        selected = []
        not_found = []
        name_list = [name.strip() for name in names_str.split(",")]

        for name in name_list:
            matching_repos = [
                repo for repo in self.repos if repo.full_name.lower() == name.lower()
            ]
            if matching_repos:
                selected.extend(matching_repos)
            else:
                not_found.append(name)

        if not selected:
            raise ValueError("No valid repositories found.")

        if not_found:
            print(f"Warning: Repositories not found: {', '.join(not_found)}")

        return selected

    def by_indices(self, index_str: str) -> List[Repository]:
        indices: set[int] = set()

        for item in index_str.split(","):
            item = item.strip()
            if not item:
                continue

            if "-" in item:
                start, end = map(int, item.split("-"))
                if start < 1 or end > len(self.repos):
                    raise ValueError(
                        f"Invalid range {start}-{end}. Indices must be between 1 and {len(self.repos)}."
                    )
                indices.update(range(start, end + 1))
            else:
                idx = int(item)
                if idx < 1 or idx > len(self.repos):
                    raise ValueError(
                        f"Invalid index {idx}. Must be between 1 and {len(self.repos)}."
                    )
                indices.add(idx)

        if not indices:
            raise ValueError("No valid indices provided.")

        # Convert indices to repositories (adjust for 0-based indexing)
        demo = [self.repos[i - 1] for i in sorted(indices)]
        return demo
