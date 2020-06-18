"""xy-tag."""
import click

from ._github import create_github_tags
from ._util import StringLenRangeParamType, find_parent_versions, RefPrefixRemover

__all__ = ("__version__", "cli")

__version__ = "0.0.1"

_NON_ZERO_STRING_TYPE = StringLenRangeParamType(min=1)


@click.command()
@click.option(
    "--github-token",
    required=True,
    envvar=("INPUT_GITHUB-TOKEN",),
    type=_NON_ZERO_STRING_TYPE,
)
@click.option(
    "--xyz-version",
    required=True,
    envvar=("INPUT_XYZ-VERSION", "GITHUB_REF",),
    type=RefPrefixRemover(min=1),
)
@click.option(
    "--commitish",
    required=True,
    envvar=("INPUT_COMMITISH", "GITHUB_SHA",),
    type=_NON_ZERO_STRING_TYPE,
)
@click.option(
    "--github-repository",
    required=True,
    envvar=("INPUT_GITHUB-REPOSITORY", "GITHUB_REPOSITORY",),
    type=_NON_ZERO_STRING_TYPE,
)
@click.option(
    "--dry-run",
    envvar=("INPUT_DRY-RUN",),
    default="false",
    type=click.types.BOOL,
    is_flag=True,
)
@click.option(
    "--version-separator",
    envvar=("INPUT_VERSION-SEPARATOR",),
    default=".",
    type=_NON_ZERO_STRING_TYPE,
)
@click.option(
    "--beta-separator",
    envvar=("INPUT_BETA-SEPARATOR",),
    default="-",
    type=_NON_ZERO_STRING_TYPE,
)
def cli(
    github_token: str,
    xyz_version: str,
    commitish: str,
    github_repository: str,
    dry_run: bool,
    version_separator: str,
    beta_separator: str,
):
    if beta_separator in xyz_version:
        click.echo("Skipping beta version!")
        return

    version_tags = find_parent_versions(
        xyz_version=xyz_version, version_separator=version_separator
    )
    if dry_run:
        for tag in version_tags:
            click.echo(tag)
        return

    create_github_tags(
        github_token=github_token,
        github_repository=github_repository,
        tags=version_tags,
        commitish=commitish,
    )
