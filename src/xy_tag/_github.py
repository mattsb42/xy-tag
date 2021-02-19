"""
Interacting with GitHub.
"""
from datetime import datetime, timezone
from typing import Sequence

import click
from agithub.GitHub import GitHub

__all__ = ("create_github_tags",)


def create_github_tags(
    *,
    github_token: str,
    github_owner: str,
    github_repository: str,
    tags: Sequence[str],
    commitish: str,
):
    """Create tags on GitHub project.

    :param github_token: GitHub authentication token
    :param github_owner: GitHub repo owner
    :param github_repository: GitHub repo name
    :param tags: Tags to create
    :param commitish: Commitish to target with tags
    """
    client = GitHub(token=github_token, paginate=True)
    repo = getattr(getattr(client.repos, github_owner), github_repository)
    create_time = datetime.now(timezone.utc).isoformat(timespec="seconds")
    for tag in tags:
        click.echo(f"Creating tag '{tag}'")
        repo.git.tags.post(
            tag=tag,
            message=tag,
            object=commitish,
            type="commit",
            tagger=dict(name="xy-tag", date=create_time),
        )
