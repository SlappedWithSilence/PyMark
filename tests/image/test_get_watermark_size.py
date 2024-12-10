import PIL.Image
import pytest

from src.helpers.image import get_watermark_size

cases = [
    ((100, 100), (100, 100), 0.5, (50, 50))
]


@pytest.mark.parametrize("i_dims, wm_dims, ratio, expected_dims", cases)
def test_resize_logic(i_dims, wm_dims, ratio, expected_dims):
    """

    :param i_dims: Dimensions of the image
    :param wm_dims: Dimensions of the watermark
    :param ratio: Size ratio between the image and watermark where ratio = (w_widith * w_height) / (i_widith * i_height)
    :param expected_dims: Human-calculated, correct result
    :return:
    """

    image = PIL.Image.new("RGB", i_dims)
    wm = PIL.Image.new("RGB", wm_dims)

    assert get_watermark_size(image, wm, ratio) == expected_dims
