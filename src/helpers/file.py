"""
A collection of helper functions relating to managing files
"""

import os.path
import re
from pathlib import PurePath
from typing import Optional


def update_file_name(original_name: str, prefix: str | None, suffix: str | None) -> str:
    """
    For some arbitrary file name, modify it according to the supplied prefix
    and suffix values.

    :param original_name: Original file name
    :param prefix: Prefix to prepend to file name
    :param suffix: Suffix to append to file name
    :return: Modified file name
    """

    return (prefix or "") + original_name + (suffix or "")


def gather_files(
    path: PurePath, allowed_extensions: list[str], pattern: Optional[str]
) -> list[PurePath]:
    """
    For a given path, locate all valid files and return .

    :param path: Path to target directory. Absolute and relative both allowed.
    :param allowed_extensions: A list of allowed extensions. Must have len >= 1
    :param pattern: Optional regex to filter files names

    :returns: A list of FileSpecs to files with valid names and file extensions in
        the given directory
    """

    # Type enforcement
    if not isinstance(path, PurePath):
        raise TypeError(f"path must be a PurePath, not a {type(path)}")

    if not isinstance(allowed_extensions, list):
        raise TypeError(
            f"allowed_extensions must be a list, not a " f"{type(allowed_extensions)}"
        )

    if pattern and not isinstance(pattern, str):
        raise TypeError(
            f"pattern must be a str or None! Got {type(pattern)} " f"instead!"
        )

    # Value validation
    if not os.path.isdir(path):
        raise NotADirectoryError(
            f"Path must point to an existing directory! "
            f"{path} doesn't exist or is a file!"
        )

    if len(allowed_extensions) < 1:
        raise IndexError("allowed_extensions must be of length > 0")

    # Compile the regex if it supplied
    regex: Optional[re.Pattern] = None
    if pattern:
        regex = re.compile(pattern)

    # Get all files in the dir
    all_file_paths: list[PurePath] = [PurePath(s) for s in os.listdir(path)]
    print(all_file_paths)

