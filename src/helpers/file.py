"""
A collection of helper functions relating to managing files
"""
import dataclasses
import os.path
import re
from typing import Optional, Iterable

from pathvalidate import validate_filepath


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


@dataclasses.dataclass
class FileSpec:
    """
    Struct for storing distinct file properties.
    """
    dir: str  # Path to the directory that contains the file
    name: str  # Name of the file (no extension)
    extension: str  # Extension of the file (without .)

    def __post_init__(self):
        if not isinstance(self.dir, str):
            raise TypeError

        if not isinstance(self.name, str):
            raise TypeError

        if not isinstance(self.extension, str):
            raise TypeError

    def __str__(self):
        return (self.dir if self.dir[-1] in ["/", "\\"] else self.dir + "/") + self.name + "." + self.extension

    @property
    def exists(self) -> bool:
        """
        Return True if a file already exists at the given path

        :return: True if file already exists
        """

        return self.valid and os.path.exists(self.__str__())

    @property
    def valid(self) -> bool:
        """
        Check if full file path is valid

        :return: True if the full file path is valid

        """
        try:
            validate_filepath(self.__str__())
            return True

        except ValueError:
            return False

    @classmethod
    def from_path(cls, path: str) -> "FileSpec":
        """
        Factory method that takes a path and returns a FileSpec object

        :param path: Path to ingest
        :return: A new FileSpec object built from the path
        """
        ext = ""
        name = None
        dir_ = "./"

        # If the path to the file has an extension
        if "." in path:
            ext = path.split(".")[-1]

        # If the path to the file does contain a subdir
        if "/" in path or "\\" in path:

            # Clean path
            clean_path = path.replace("\\", "/")

            # Split string by dir
            parts = clean_path.split("/")

            # Extract name from final entry assuming an ext
            name = parts[-1].split(".")[0]

            # Re-assemble split parts by joining with a slash and excluding final entry (which contains name and ext)
            dir_ = "/".join(parts[:-1])

        # If no subdirs, just split the name away from the ext and assign it
        else:
            name = path.split(".")[0]

        return FileSpec(dir_, name, ext)


def gather_files(
        path: str, allowed_extensions: list[str], pattern: Optional[str]
) -> list[FileSpec]:
    """
    For a given path, locate all valid files and return .

    :param path: Path to target directory. Absolute and relative both allowed.
    :param allowed_extensions: A list of allowed extensions. Must have len >= 1
    :param pattern: Optional regex to filter files names

    :returns: A list of FileSpecs to files with valid names and file extensions in
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
    proper_path = path if path[-1] in [r"/" or "\\"] else path + "/"

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
    return [FileSpec.from_path(proper_path + fname) for fname in valid_names]


def to_output_path(file_spec: FileSpec, out_path, prefix: str, suffix: str, ext: str) -> FileSpec:
    """
    Converts an input FileSpec to an output FileSpec based on cli args
    :param file_spec: The input FileSpec
    :param out_path: The outpath specified in the CLI
    :param prefix: file name prefix
    :param suffix: file name suffix
    :param ext: file extension
    :return: A modified FileSpec
    """

    return FileSpec(
        out_path,
        f"{prefix}{file_spec.name}{suffix}",
        ext
    )
