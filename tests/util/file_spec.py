import random

from helpers.file import FileSpec


def test_file_spec_trivial():
    fs = FileSpec("./", "a", "png")


def test_exists():
    fname = f"{random.random()}"
    fs = FileSpec("./", fname, "coors")
    assert not fs.exists
