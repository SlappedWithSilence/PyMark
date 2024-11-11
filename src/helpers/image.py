from pathlib import PurePath

from PIL import Image
from PIL.Image import Resampling

ALLOWED_CORNERS: list[str] = ["bottom_left", "bottom_right", "top_left", "top_right"]


def get_watermark_size(image: Image.Image, watermark: Image.Image, ratio: float) -> tuple[int, int]:
    """
    A small helper function that determines what size the watermark should be based on watermark original size, image
    size, and watermark ratio.
    :param ratio: The ratio of watermark size to image size. Ratio refers to relative size of the shortest image
        dimension to the corresponding dimension on the watermark.
    :param watermark: PILLOW Image file for watermark
    :param image: PILLOW Image file for image
    :return: A pair of ints representing the watermark's resized dimensions
    """

    if not isinstance(image, Image.Image):
        raise TypeError(f"image must be of type Image! Got {type(image)} instead.")
    if not isinstance(watermark, Image.Image):
        raise TypeError(f"watermark must be of type Image! Got {type(watermark)} instead.")

    # See: https://stackoverflow.com/questions/3971841/how-to-resize-images-proportionally-keeping-the-aspect-ratio
    image_w, image_h = image.size
    watermark_max_w = image_w * ratio
    watermark_max_h = image_h * ratio
    watermark_w, watermark_h = watermark.size
    watermark_dims_ratio = min(watermark_max_w / watermark_w, watermark_max_h / watermark_h)

    return round(watermark_w * watermark_dims_ratio), round(watermark_max_h * watermark_dims_ratio)


def apply_watermark(
        path_in: PurePath,
        path_out: PurePath,
        watermark_path: PurePath,
        corner: str,
        padding: float,
        relative_size: float,
) -> None:
    """
    Perform the watermarking logic and save result.

    No path checking is performed. All of that should have happened before calling this function.

    :param path_in: Path to the input file
    :param path_out: Path to the save the new file to
    :param watermark_path: Path to the watermark
    :param corner: Which corner to anchor the watermark to
    :param padding: The size of the gap between the watermark and the edge of the image
    :param relative_size: The size of the watermark relative to the image
    :return: None
    """

    # Type Checking
    if not isinstance(path_in, PurePath):
        raise TypeError(
            f"file_spec_in must be a PurePath. Got a {type(path_in)} instead."
        )

    if not isinstance(path_out, PurePath):
        raise TypeError(
            f"file_spec_out must be a PurePath. Got a {type(path_out)} instead."
        )

    if not isinstance(watermark_path, str):
        raise TypeError(
            f"watermark_path must be a PurePath. Got a {type(watermark_path)} instead."
        )

    if not isinstance(corner, str):
        raise TypeError(f"corner must be a str. Got a {type(corner)} instead.")

    if not isinstance(padding, float):
        raise TypeError(f"padding must be a float. Got a {type(padding)} instead.")

    if not isinstance(relative_size, float):
        raise TypeError(
            f"relative_size must be a float. Got {type(relative_size)} instead."
        )

    # Value checking
    if corner.lower() not in ALLOWED_CORNERS:
        raise ValueError(f"Invalid corner value. Allowed values are: {ALLOWED_CORNERS}")

    if padding >= 1.0 or padding <= 0.0:
        raise ValueError(
            f"Invalid padding value. Must be a float less than 1.0. Got {padding}"
        )

    if relative_size >= 1.0 or padding <= 0.0:
        raise ValueError(
            f"Invalid relative_size value. Must be a float less than 1.0. Got {relative_size}"
        )

    with Image.open(path_in) as image:
        with Image.open(watermark_path) as watermark:
            im_length, im_width = image.size
            watermark_length, watermark_width = watermark.size

            # Determine which side of the image is shortest
            shortest_side: str = "l" if im_length <= im_width else "w"

            # Calculate the projected size of the corresponding side of the watermark
            watermark_adjusted_len: float = (
                                                im_length if shortest_side == "l" else im_width
                                            ) * relative_size

            # Determine ratio of current watermark size to expected watermark size
            watermark_scalar: float = (
                                          watermark_length if shortest_side == "l" else watermark_width
                                      ) / watermark_adjusted_len

            # Calculate expected dimensions of post-scaled watermark
            watermark_dims: tuple[int, int] = (
                round(watermark_length / watermark_scalar),
                round(watermark_width / watermark_scalar),
            )

            # Calculate size of padding based on shortest side of image
            padding_size: int = round(
                (im_length if shortest_side == "l" else im_width) * padding
            )

            watermark.resize(watermark_dims, Resampling.LANCZOS)
