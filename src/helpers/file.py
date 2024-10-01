"""
A collection of helper functions relating to managing files
"""

import os.path
import re
from typing import Optional, Iterable


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


def get_path_collisions(
    target_dir: str, file_names: Iterable[str], file_extension: str
) -> list[str] | None:
    """
    For each file name, check if that name is taken within a target directory.

    :param target_dir: Absolute or relative path to directory to check
    :param file_names: An iterable collection of file names
    :param file_extension: The extension to save the file as
    :return: A list of names that are already taken. If no names are taken, None
    """

    if not isinstance(target_dir, str):
        raise TypeError("target_dir must be a path of type str!")

    if not isinstance(file_extension, str):
        raise TypeError("file_extension must be of type str!")

    true_dir = target_dir if target_dir.endswith("/") else target_dir + "/"

    if not os.path.isdir(target_dir):
        raise NotADirectoryError("target_dir must be a valid directory!")

    collisions = [
        f"{true_dir}{fname}{file_extension}"
        for fname in file_names
        if os.path.isfile(f"{true_dir}{fname}{file_extension}")
    ]

    return collisions if len(collisions) > 0 else None


def gather_files(
    path: str, allowed_extensions: list[str], pattern: Optional[str]
) -> list[str]:
    """
    For a given path, locate all valid files.

    :param path: Path to target directory. Absolute and relative both allowed.
    :param allowed_extensions: A list of allowed extensions. Must have len >= 1
    :param pattern: Optional regex to filter files names

    :returns: A list of paths to files with valid names and file extensions in
        the given directory
    """

    # Type enforcement
    if not isinstance(path, str):
        raise TypeError(f"path must be a str, not a {type(path)}")

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

    # Make sure that the path ends with a slash
    proper_path = path if path[-1] in ["/" or "\\"] else path + "/"

    # Compile the regex if it supplied
    regex: Optional[re.Pattern] = None
    if pattern:
        regex = re.compile(pattern)

    # Get all files in the dir
    all_file_names = os.listdir(path)

    # Filter by extension
    # Case-insensitive
    valid_names = [
        fname
        for fname in all_file_names
        if any((fname.lower().endswith(ext.lower()) for ext in allowed_extensions))
    ]

    # Filter by regex
    if regex:
        valid_names = [
            ".".join(fname.split(".")[:-1])
            for fname in valid_names
            if regex.fullmatch(".".join(fname.split(".")[:-1]))
        ]

    # Return a list of paths, not of names, to the files
    return [proper_path + fname for fname in valid_names]
