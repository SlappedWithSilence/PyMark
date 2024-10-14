"""
A collection of helper methods with general utility.
"""

import os.path
import sys

from loguru import logger

from PIL import Image


def make_debug_image(
    name: str, path: str, width: int = 100, height: int = 100, extension: str = ".png"
) -> None:
    """
    Generate a blank white debug image at the specified path with the specified dimensions.

    Args:
        name: Name of the file
        path: Path in which to save the file
        width: Width of the image
        height: Height of the image
        extension: Format extension to save the image to

    Returns: None
    """

    # Validate inputs
    if not isinstance(name, str):
        raise TypeError()

    if not isinstance(path, str):
        raise TypeError()

    if not isinstance(width, int):
        raise TypeError()

    if not isinstance(height, int):
        raise TypeError()

    if not isinstance(extension, str):
        raise TypeError()

    if extension.replace(".", "").lower() not in ["png", "jpeg"]:
        raise ValueError(f"extension must be png or jpeg! Got {extension} instead!")

    # Clean inputs
    true_path: str = path if path.endswith("/") else path + "/"
    true_extension: str = extension if extension.startswith(".") else "." + extension

    full_path = true_path + name + true_extension

    # Check if file already exists
    if os.path.isfile(full_path):
        logger.error(
            f"Failed to generate debug image at path: {full_path}. File already exists"
        )
        sys.exit(1)

    # Generate a white image and save it
    im = Image.new("RGB", (width, height), (255, 255, 255))
    im.save(full_path, true_extension[1:])


if __name__ == "__main__":
    os.makedirs("../../debug/", exist_ok=True)
    for i in range(10):
        make_debug_image(str(i), "../../debug", extension="jpeg")
