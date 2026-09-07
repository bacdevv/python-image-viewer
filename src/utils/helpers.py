from __future__ import annotations

import cv2
import numpy as np
from PIL import Image, ImageTk


def cv_image_to_pil(image: np.ndarray) -> Image.Image:
    """Convert an OpenCV BGR/BGRA image to a Pillow image."""
    if image is None or not isinstance(image, np.ndarray) or image.ndim not in (2, 3):
        raise ValueError("image must be a valid 2D or 3D numpy array")

    if image.ndim == 2:
        return Image.fromarray(image)
    if image.shape[2] == 4:
        return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA))
    if image.shape[2] == 3:
        return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    raise ValueError("image must have 1, 3, or 4 channels")


def cv_image_to_tk(image: np.ndarray, size: tuple[int, int]) -> ImageTk.PhotoImage:
    """Convert an OpenCV image to a Tk image fitted inside size."""
    pil_image = cv_image_to_pil(image)
    pil_image.thumbnail(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(pil_image)
