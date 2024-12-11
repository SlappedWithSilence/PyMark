from pathlib import PurePath

from PIL import Image
from PIL.Image import Resampling
from loguru import logger

ALLOWED_CORNERS: list[str] = ["bottom_left", "bottom_right", "top_left", "top_right"]


def get_watermark_size(image: Image.Image, watermark: Image.Image, ratio: float) -> tuple[int, int] | None:
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

    image_w, image_h = image.size  # Original dims of image
    wm_w, wm_h = watermark.size  # Original dims of watermark
    wm_max_w: int = round(image_w * ratio)  # Max allowed length of watermark width
    wm_max_h: int = round(image_h * ratio)  # Max allowed length of watermark height

    # Determine which dimension of the image is the shortest to avoid clipping in extreme situations
    image_shortest_side: str = "h" if image_w >= image_h else "w"
    wm_calc_side: int = wm_max_w if image_shortest_side == "w" else wm_max_h

    # Using the shortest side of the image, determine how much the watermark needs to be resized
    resize_factor: float = wm_calc_side / (wm_h if image_shortest_side == "h" else wm_w)

    if round(wm_h * resize_factor) > wm_max_h or round(wm_w * resize_factor) > wm_max_w or 0 in [wm_max_w, wm_max_h]:
        logger.error("Failed to calculate a resize plan for watermark!")
        logger.debug(f"Image: {image}")
        logger.debug(f"Watermark: {watermark}")
        logger.debug(f"h: {wm_h * resize_factor}, max_h: {wm_max_h}")
        logger.debug(f"w: {wm_w * resize_factor}, max_w: {wm_max_w}")
        logger.debug(f"resize_by: {resize_factor}")
        return None

    return round(wm_h * resize_factor), round(wm_w * resize_factor)


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
    logger.info("Watermarking...")

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

    if padding >= 1.0 or padding < 0.0:
        raise ValueError(
            f"Invalid padding value. Must be a float less than 1.0. Got {padding}"
        )

    if relative_size >= 1.0 or relative_size <= 0.0:
        raise ValueError(
            f"Invalid relative_size value. Must be a float less than 1.0. Got {relative_size}"
        )

    with Image.open(path_in) as image:
        with Image.open(watermark_path) as watermark:
            watermark_dims = get_watermark_size(image, watermark, relative_size)

            if not watermark_dims:
                exit(-1)

            resized_watermark = watermark.resize(watermark_dims, Resampling.LANCZOS)
            padding_size = min(image.size) * padding  # Num pixels to pad. Used as a pos offset later

            new_image = Image.new("RGB", image.size, (250, 250, 250))
            new_image.paste(image, (0, 0))

            corner_pos_map = {
                "bottom_left": (padding_size, image.size[1] - padding_size),
                "bottom_right": (image.size[0] - padding_size, image.size[1] - padding_size),
                "top_left": (padding_size, padding_size),
                "top_right": (image.size[0] - padding_size, padding_size)
            }

            new_image.paste(resized_watermark, corner_pos_map[corner])
            new_image.save(path_out)
