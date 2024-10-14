# PyMark
_A Python utility to batch watermark images in a directory_

PyMark supports multiple watermarking modes. 

- Corner Watermarking
  - Overlay an image or arbitrary text in a specified corner of the image
- Cross Watermarking
  - Overlay text diagonally across the image with adjustable transparency
- Center Watermarking
  - Overlay an image or arbitrary text centered on the image with adjustable transparency

# Usage
 
## Mark
The main watermarking command.

### Args & Options
- `mark`: File path to the image to use as the watermark
- `--in-path`, `-i`: Path to the file or directory for which to watermark files
- `--out-path`, `-o`: Path to the directory in which to write the watermarked images
- `--corner`: The corner of the image in which to anchor the watermark
- 

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
