"""
Utility functions.
"""
import itertools
from typing import Sequence

from click.types import StringParamType

__all__ = ("find_parent_versions", "StringLenRangeParamType", "RefPrefixRemover")


def find_parent_versions(*, xyz_version: str, version_separator: str) -> Sequence[str]:
    """Given an X.Y.Z version string, find the X and X.Y versions.

    :param xyz_version: X.Y.Z version string
    pre: len(xyz_version) > 0

    :param version_separator: Value that separates version markers
    pre: len(version_separator) > 0

    :returns: Sequence of parent versions
    post: len(__return__) == xyz_version.count(version_separator)
    """
    if version_separator not in xyz_version:
        return ()

    parent_members = xyz_version.split(version_separator)[:-1]
    return tuple(
        map(version_separator.join, itertools.accumulate(map(list, parent_members)),)
    )


class StringLenRangeParamType(StringParamType):
    """A parameter that works similar to :data:`click.types.StringParamType`
    but the length of the value fits in a range.
    """

    name = "string length range"

    def __init__(self, min_len=None, max_len=None):
        if min_len is not None and max_len is not None and min_len > max_len:
            self.fail("min_len MUST NOT be greater than max_len")

        self.min_len = min_len
        self.max_len = max_len

    def convert(self, value, param, ctx):
        rv = StringParamType.convert(self, value, param, ctx)
        value_length = len(rv)

        if self.min_len is not None and value_length < self.min_len:
            self.fail(
                f"Value length {value_length} less than required minimum length {self.min_len}"
            )

        if self.max_len is not None and value_length > self.max_len:
            self.fail(
                f"Value length {value_length} greater than required maximum length {self.max_len}"
            )

        return rv


class RefPrefixRemover(StringLenRangeParamType):
    """A parameter that works similar to :data:`StringLenRangeParamType`
    but removes the "refs/heads/" prefix.
    """

    name = "refs prefix remover"
    _remove_prefix = "refs/heads/"

    def convert(self, value, param, ctx):
        rv = StringParamType.convert(self, value, param, ctx)
        if rv.startswith(self._remove_prefix):
            rv = rv[len(self._remove_prefix) :]
        return StringLenRangeParamType.convert(self, rv, param, ctx)
