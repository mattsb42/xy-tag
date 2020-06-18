"""
Utility functions.
"""
import itertools
from typing import Iterator

from click.types import StringParamType

__all__ = ("find_parent_versions", "StringLenRangeParamType")


def find_parent_versions(*, xyz_version: str, version_separator: str) -> Iterator[str]:
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
    return map(
        lambda x: version_separator.join(x),
        itertools.accumulate(map(list, parent_members)),
    )


class StringLenRangeParamType(StringParamType):
    """A parameter that works similar to :data:`click.types.StringParamType`
    but the length of the value fits in a range.
    """

    name = "string length range"

    def __init__(self, min=None, max=None):
        if min is not None and max is not None and min > max:
            self.fail("min MUST NOT be greater than max")

        self.min = min
        self.max = max

    def convert(self, value, param, ctx):
        rv = StringParamType.convert(self, value, param, ctx)
        value_length = len(rv)

        if self.min is not None and value_length < self.min:
            self.fail(
                f"Value length {value_length} less than required minimum length {self.min}"
            )

        if self.max is not None and value_length > self.max:
            self.fail(
                f"Value length {value_length} greater than required maximum length {self.max}"
            )

        return rv
