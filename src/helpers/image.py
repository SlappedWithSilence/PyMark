from helpers.file import FileSpec


def apply_watermark(
    file_spec_in: FileSpec, file_spec_out: FileSpec, watermark_path: str, output_path: str, corner: str, padding: float
) -> None:
    """
    Perform the watermarking logic and save result.

    No path checking is performed. All of that should have happened before calling this function.

    :param file_spec_out:
    :param file_spec_in:
    :param watermark_path: Path to the watermark
    :param output_path: Path to write the modified image to
    :param corner: Which corner to anchor the watermark to
    :param padding: The size of the gap between the watermark and the edge of the image
    :return: None
    """

