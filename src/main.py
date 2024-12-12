"""
Main driver code for the Typer implementation.
"""

import os.path
import sys
import threading
from pathlib import PurePath
from typing import Optional, Annotated

import typer
from loguru import logger
from pathvalidate.click import validate_filepath_arg

from helpers.file import gather_files
from helpers.image import apply_watermark

app = typer.Typer()

is_input_dir: bool = None


@app.command()
def mark(
    mark_path: Annotated[
        str,
        typer.Argument(
            help="mark_path: Path to the image to use as a watermark",
            callback=validate_filepath_arg,
        ),
    ],
    corner: Annotated[
        str,
        typer.Option(
            "--corner",
            "-c",
            help="Which corner to overlay the image on.",
        ),
    ] = "bottom_right",
    in_path: Annotated[
        str,
        typer.Option(
            "--in-path",
            "-i",
            help="Path to image(s) to watermark.",
            callback=validate_filepath_arg,
        ),
    ] = "./",
    out_path: Annotated[
        str,
        typer.Option(
            "--out-path",
            "-o",
            help="Path to save watermarked image(s)",
            callback=validate_filepath_arg,
        ),
    ] = "./",
    overwrite: Annotated[
        bool,
        typer.Option(
            help="If True, overwrite any existing files with the same name "
            "as the output files"
        ),
    ] = False,
    pattern: Annotated[
        Optional[str],
        typer.Option(
            help="A regex to use as a filter for which images to select for"
            " watermarking"
        ),
    ] = None,
    prefix: Annotated[
        Optional[str],
        typer.Option(
            help="An optional string that is prepended to the file name of "
            "the output file(s)"
        ),
    ] = "",
    suffix: Annotated[
        Optional[str],
        typer.Option(
            help="An optional string that is appended to the file name of the "
            "output files"
        ),
    ] = "",
    file_types: Annotated[
        str,
        typer.Option(
            help="A comma-delineated list of file formats to read when "
            "searching a directory for images"
        ),
    ] = ".png,.jpg,.jpeg",
    output_file_type: Annotated[
        str,
        typer.Option(
            help="Which file format to write the output files in. See Pillow "
            "supported file formats for more info."
        ),
    ] = ".jpg",
    preset: Annotated[
        Optional[str],
        typer.Option(
            "--preset",
            "-p",
            help="The name of a preset to use. Any supplied configuration "
            "values will take precedence over the existing preset "
            "values.",
        ),
    ] = None,
) -> None:
    """
    Watermark one or more images.
    """
    global is_input_dir

    # Load watermark image
    if os.path.isfile(mark_path):
        pass

    # Handle invalid path
    else:
        raise FileNotFoundError(f"Unable to locate file with path {mark_path}")

    # Load input images
    if os.path.isfile(in_path):
        # If supplied path is a file, load it
        is_input_dir = False

    elif os.path.isdir(in_path):
        # If supplied path is a directory, load all images inside
        is_input_dir = True

    else:
        raise FileNotFoundError(
            f"Input path supplied is not a valid file or " f"directory: {in_path}"
        )

    input_file_paths: list[PurePath] = []  # A list of all files that need to be processed

    # If the input path points to a file handle as if it was dir with one file
    if not is_input_dir:
        input_file_paths.append(PurePath(in_path))
    else:
        files = gather_files(PurePath(in_path), file_types.split(","), pattern)

    # Pre-compute output file names to check for name collisions before doing
    # any work.
    output_file_paths = [PurePath(out_path) / (f.stem + suffix + f.suffix) for f in input_file_paths]

    if not overwrite:
        collisions: list[PurePath] = [fs for fs in output_file_paths if os.path.exists(fs)]

        if len(collisions) > 0:
            logger.error("Name collision detected. The following files already exist:")
            for fs in collisions:
                logger.error(fs)
            logger.error("To ignore file name collisions, run with --overwrite " "true")
            sys.exit(-1)

    for path_in, path_out in zip(input_file_paths, output_file_paths):
        logger.info("Dispatching job...")

        """
        threading.Thread(
            target=apply_watermark,
            name=f"Watermark: {path_in}",
            args=(path_in, path_out, mark_path, corner, 0.05),
        )
        """

        apply_watermark(path_in, path_out, PurePath(mark_path), corner, 0.05, 0.10)


if __name__ == "__main__":
    app()
