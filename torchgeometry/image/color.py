import torch
import torch.nn as nn


class RgbToHsV(nn.Module):

    """convert image from RGB to HSV.
    The image data is assumed to be in the range of (0, 1).

    args:
        image (torch.tensor): RGB image to be converted to HSV.

    returns:
        torch.tensor: HSV version of the image.

    shape:
        - image: :math:`(*, 3, h, w)`
        - output: :math:`(*, 3, h, w)`

    """

    def __init__(self) -> None:
        super(RgbToHsV, self).__init__()

    def forward(self, image: torch.Tensor) -> torch.Tensor:  # type: ignore
        return rgb_to_hsv(image)


def rgb_to_hsv(image):

    """Convert an RGB image to HSV

    Args:
        input (torch.Tensor): RGB Image to be converted to HSV.

    Returns:
        torch.Tensor: HSV version of the image.
    """

    if not torch.is_tensor(image):
        raise TypeError("Input type is not a torch.Tensor. Got {}".format(
            type(image)))

    if len(image.shape) < 3 or image.shape[-3] != 3:
        raise ValueError("Input size must have a shape of (*, 3, H, W). Got {}"
                         .format(image.shape))

    out = torch.empty_like(image)
    maxc = image.max(0)[0]
    minc = image.min(0)[0]

    delta = torch.tensor(image.numpy().ptp(0))

    r = image[..., 0, :, :]
    g = image[..., 1, :, :]
    b = image[..., 2, :, :]

    # brightness
    v = maxc

    # saturation
    s = delta / v
    s[delta == 0.] = 0.

    # red is max
    idx = r == maxc
    out[..., 0, idx] = (g[idx] - b[idx]) / delta[idx]

    # green is max
    idx = g == maxc
    out[..., 0, idx] = 2.0 + (b[idx] - r[idx]) / delta[idx]

    # blue is max
    idx = b == maxc
    out[..., 0, idx] = 4.0 + (r[idx] - g[idx]) / delta[idx]

    # hue
    h = (out[..., 0, :, :] / 6) % 1.
    h[delta == 0.] = 0.

    out[..., 0, :, :] = h
    out[..., 1, :, :] = s
    out[..., 2, :, :] = v

    return out


class BgrToRgb(nn.Module):

    """convert image from BGR to RGB.
    The image data is assumed to be in the range of (0, 1).

    args:
        image (torch.tensor): BGR image to be converted to RGB.

    returns:
        torch.tensor: RGB version of the image.

    shape:
        - image: :math:`(*, 3, h, w)`
        - output: :math:`(*, 3, h, w)`

    """

    def __init__(self) -> None:
        super(BgrToRgb, self).__init__()

    def forward(self, image: torch.Tensor) -> torch.Tensor:  # type: ignore
        return bgr_to_rgb(image)


def bgr_to_rgb(image: torch.Tensor) -> torch.Tensor:
    """Convert a BGR image to RGB.

    Args:
        input (torch.Tensor): BGR Image to be converted to RGB.

    Returns:
        torch.Tensor: RGB version of the image.
    """

    if not torch.is_tensor(image):
        raise TypeError("Input type is not a torch.Tensor. Got {}".format(
            type(image)))

    if len(image.shape) < 3 or image.shape[-3] != 3:
        raise ValueError("Input size must have a shape of (*, 3, H, W).Got {}"
                         .format(image.shape))

    out = image.flip(-3)

    return out


class RgbToGrayscale(nn.Module):
    r"""convert image to grayscale version of image.

    the image data is assumed to be in the range of (0, 1).

    args:
        input (torch.tensor): image to be converted to grayscale.

    returns:
        torch.tensor: grayscale version of the image.

    shape:
        - input: :math:`(*, 3, h, w)`
        - output: :math:`(*, 1, h, w)`

    Examples::

        >>> input = torch.rand(2, 3, 4, 5)
        >>> gray = tgm.image.RgbToGrayscale()
        >>> output = gray(input)  # 2x1x4x5
    """
    def __init__(self) -> None:
        super(RgbToGrayscale, self).__init__()

    def forward(self, input: torch.Tensor) -> torch.Tensor:  # type: ignore
        return rgb_to_grayscale(input)


def rgb_to_grayscale(input: torch.Tensor) -> torch.Tensor:
    r"""Convert an RGB image to grayscale.

    See :class:`~torchgeometry.image.RgbToGrayscale` for details.

    Args:
        input (torch.Tensor): Image to be converted to grayscale.

    Returns:
        torch.Tensor: Grayscale version of the image.
    """
    if not torch.is_tensor(input):
        raise TypeError("Input type is not a torch.Tensor. Got {}".format(
            type(input)))

    if len(input.shape) < 3 and input.shape[-3] != 3:
        raise ValueError("Input size must have a shape of (*, 3, H, W). Got {}"
                         .format(input.shape))

    # https://docs.opencv.org/4.0.1/de/d25/imgproc_color_conversions.html
    r, g, b = torch.chunk(input, chunks=3, dim=-3)
    gray: torch.Tensor = 0.299 * r + 0.587 * g + 0.110 * b
    return gray
