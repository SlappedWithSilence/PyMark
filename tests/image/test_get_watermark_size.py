import PIL.Image
import pytest

from helpers.image import get_watermark_size

cases = [
    ((100, 100), (100, 100), 0.5, (50, 50))
]


@pytest.mark.parametrize("i_dims, wm_dims, ratio, expected_dims", cases)
def test_resize_logic(i_dims, wm_dims, ratio, expected_dims):
    """

    :param i_dims:
    :param wm_dims:
    :param ratio:
    :param expected_dims:
    :return:
    """

    image = PIL.Image.new("RGB", i_dims)
    wm = PIL.Image.new("RGB", wm_dims)

    assert get_watermark_size(image, wm, ratio) == expected_dims
