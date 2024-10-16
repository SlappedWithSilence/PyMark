# PyMark
_A Python utility to batch watermark images in a directory_

PyMark supports multiple watermarking modes. 

- Corner Watermarking
  - Overlay an image or arbitrary text in a specified corner of the image
- Cross Watermarking (TODO)
  - Overlay text diagonally across the image with adjustable transparency
- Center Watermarking
  - Overlay an image or arbitrary text centered on the image with adjustable transparency

# Usage
 
## `Mark`
The main watermarking command.

### Args & Options
-  `--corner` Which corner to overlay the image on.                                                                                                                                                                                                  │
- `--in-path` Path to image(s) to watermark.                                                                                                                                                                                                              │
- `--out-path` Path to save watermarked image(s)                                                                                                                                                                                                           │
- `--overwrite` If True, overwrite any existing files with the same name as the output files                                                                                                                                                         │
- `--pattern` A regex to use as a filter for which images to select for watermarking                                                                                                                                                                      │
- `--prefix` An optional string that is prepended to the file name of the output file(s)                                                                                                                                                                   │
- `--suffix` An optional string that is appended to the file name of the output files                                                                                                                                                                      │
- `--file-types` A comma-delineated list of file formats to read when searching a directory for images                                                                                                                                              │
- `--output-file-type` Which file format to write the output files in. See Pillow supported file formats for more info.                                                                                                                                              │
- `--preset` The name of a preset to use. Any supplied configuration values will take precedence over the existing preset values. 
- `--help` Print usage info

## Contributing

When contributing to PyMark, ensure that your code passes all tests and does not generate any new linter warnings. It is strongly suggested that you run both [PyLint](https://www.pylint.org/) and [Ruff](https://docs.astral.sh/ruff/installation/) before submitting a MR. 

To set up both linters, run the following commands from the root directory of the repo:
- `pip install pylint`
- `pip install ruff`

To use the linters:
- `pylint src`
- `ruff format && ruff check`

**TIP**: _You can also configure Ruff to [run as a pre-commit hook.](https://docs.astral.sh/ruff/integrations/#pre-commit)_
## Testing

TODO

## Known Issues

Project doesn't exist

## Acknowledgements

- Typer - Excellent CLI library
- Pillow - Python Imaging Library
- Ruff - Blazing Fast Linting and Formatting
- PyLint - Content-aware Linting
- PyTest - Testing Framework
- Coverage - Code Coverage Metrics
- [pathvalidate](https://pypi.org/project/pathvalidate/) - Cross-platform path sanitization
