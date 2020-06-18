"""
Interacting with GitHub.
"""
from typing import Iterator

__all__ = ("create_github_tags",)


def create_github_tags(
    *, github_token: str, github_repository: str, tags: Iterator[str], commitish: str
):
    pass
