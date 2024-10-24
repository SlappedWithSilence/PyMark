from file import FileSpec

from PIL import Image

ALLOWED_CORNERS: list[str] = ["bottom_left", "bottom_right", "top_left", "top_right"]


def apply_watermark(
        file_spec_in: FileSpec, file_spec_out: FileSpec, watermark_path: str, corner: str, padding: float,
        relative_size: float
) -> None:
    """
    Perform the watermarking logic and save result.

    No path checking is performed. All of that should have happened before calling this function.

    :param file_spec_out:
    :param file_spec_in:
    :param watermark_path: Path to the watermark
    :param corner: Which corner to anchor the watermark to
    :param padding: The size of the gap between the watermark and the edge of the image
    :param relative_size: The size of the watermark relative to the image
    :return: None
    """

    if not isinstance(file_spec_in, FileSpec):
        raise TypeError(f"file_spec_in must be a FileSpec. Got a {type(file_spec_in)} instead.")

    if not isinstance(file_spec_out, FileSpec):
        raise TypeError(f"file_spec_out must be a FileSpec. Got a {type(file_spec_out)} instead.")

    if not isinstance(watermark_path, str):
        raise TypeError(f"watermark_path must be a str. Got a {type(watermark_path)} instead.")

    if not isinstance(corner, str):
        raise TypeError(f"corner must be a str. Got a {type(corner)} instead.")

    if not isinstance(padding, float):
        raise TypeError(f"padding must be a float. Got a {type(padding)} instead.")

    if not isinstance(relative_size, float):
        raise TypeError(f"relative_size must be a float. Got {type(relative_size)} instead.")

    if corner.lower() not in ALLOWED_CORNERS:
        raise ValueError(f"Invalid corner value. Allowed values are: {ALLOWED_CORNERS}")

    if padding >= 1.0 or padding <= 0.0:
        raise ValueError(f"Invalid padding value. Must be a float less than 1.0. Got {padding}")

    if relative_size >= 1.0 or padding <= 0.0:
        raise ValueError(f"Invalid relative_size value. Must be a float less than 1.0. Got {relative_size}")

    with Image.open(str(file_spec_in)) as image:
        with Image.open(watermark_path) as watermark:

            im_length, im_width = image.size
            watermark_length, watermark_width = watermark.size

            # Determine which side of the image is shortest
            shortest_side: str = "l" if im_length <= im_width else "w"

            # Calculate the projected size of the corresponding side of the watermark
            watermark_adjusted_len: float = (im_length if shortest_side == "l" else im_width) * relative_size

            # Determine ratio of current watermark size to expected watermark size
            watermark_scalar: float = (watermark_length if shortest_side == "l" else watermark_width) / watermark_adjusted_len

            # Calculate expected dimensions of post-scaled watermark
            watermark_dims: tuple[int, int] = (
                round(watermark_length / watermark_scalar),
                round(watermark_width / watermark_scalar)
            )

            # Calculate size of padding based on shortest side of image
            padding_size: int = round((im_length if shortest_side == "l" else im_width) * padding)





