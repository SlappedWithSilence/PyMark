"""
Main driver code for the Typer implementation.
"""

import os.path
import sys
import threading
from typing import Optional, Annotated

import typer
from loguru import logger
from pathvalidate.click import validate_filepath_arg

from helpers.file import gather_files, get_path_collisions
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
    ] = None,
    suffix: Annotated[
        Optional[str],
        typer.Option(
            help="An optional string that is appended to the file name of the "
            "output files"
        ),
    ] = None,
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

    # Validate output path
    if os.path.isdir(out_path) and not is_input_dir:
        raise IsADirectoryError(
            "Input path was a file and output path was a "
            "directory. User must supply a path that points"
            " to a file."
        )

    if os.path.isfile(out_path) and is_input_dir:
        raise NotADirectoryError(
            "Input path was a directory and output path "
            "was a file. User must supply a path that "
            "points to a directory."
        )

    files: list[str] = None  # A list of all files that need to be processed

    # If the input path points to a file handle as if it was dir with one file
    if not is_input_dir:
        parts: list[str] = in_path.split("/")
        files = [parts[-1]]  # Names of files
    else:
        files = gather_files(in_path, file_types.split(","), pattern)

    # Pre-compute output file names to check for name collisions before doing
    # any work.
    if not overwrite:
        output_file_names: list[str] = get_path_collisions(
            out_path, files, output_file_type
        )

        if output_file_names:
            logger.error("Name collision detected. The following files already exist:")
            for name in output_file_names:
                logger.error(name)
            logger.error("To ignore file name collisions, run with --overwrite " "true")
            sys.exit(-1)

        for file_path in files:
            threading.Thread(
                target=apply_watermark,
                name=f"Watermark: {file_path}",
                args=(file_path, mark_path, corner, 0.05),
            )

        # For each file, open

        # Add watermark

        # Check for naming collisions

        # Save new file


if __name__ == "__main__":
    app()
