"""
A collection of helper functions relating to managing files
"""
import os.path
import re
from typing import Optional


def gather_files(path: str,
                 allowed_extensions: list[str],
                 pattern: Optional[str]) -> list[str]:
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
        raise TypeError(f"allowed_extensions must be a list, not a "
                        f"{type(allowed_extensions)}")

    if pattern and not isinstance(pattern, str):
        raise TypeError(f"pattern must be a str or None! Got {type(pattern)} "
                        f"instead!")

    # Value validation
    if not os.path.isdir(path):
        raise NotADirectoryError(f"Path must point to an existing directory! "
                                 f"{path} doesn't exist or is a file!")

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
        fname for fname in all_file_names if any(
            [fname.lower().endswith(ext.lower()) for ext in allowed_extensions]
        )
    ]

    # Filter by regex
    if regex:
        valid_names = [
            ".".join(
                fname.split(".")[:-1]
            ) for fname in valid_names if regex.fullmatch(
                ".".join(fname.split(".")[:-1])
            )
        ]

    # Return a list of paths, not of names, to the files
    return [proper_path + fname for fname in valid_names]
