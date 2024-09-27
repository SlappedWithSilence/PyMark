# PyMark
## A Python utility to batch watermark images in a directory

PyMark supports multiple watermarking modes. 

- Corner Watermarking
  - Overlay an image or arbitrary text in a specified corner of the image
- Cross Watermarking
  - Overlay text diagonally across the image with adjustable transparency
- Center Watermarking
  - Overlay an image or arbitrary text centered on the image with adjustable transparency

## Usage
 
TODO

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

