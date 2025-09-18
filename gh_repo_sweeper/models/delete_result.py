from typing import List, Tuple, TypedDict

from github.Repository import Repository


class DeleteResult(TypedDict):
    success: List[Repository]
    fail: List[Tuple[Repository, Exception]]
