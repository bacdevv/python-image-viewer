import cv2
import numpy as np


def zoom_image(image: np.ndarray, scale: float) -> np.ndarray:
    if image is None or not isinstance(image, np.ndarray) or image.ndim < 2:
        raise ValueError("image must be a valid numpy array")

    scale = float(scale)
    if scale <= 0:
        raise ValueError("scale must be greater than 0")

    if scale == 1:
        return image

    height, width = image.shape[:2]

    new_width = max(1, int(round(width * scale)))
    new_height = max(1, int(round(height * scale)))

    if scale > 1:
        interpolation = cv2.INTER_LINEAR
    else:
        interpolation = cv2.INTER_AREA

    new_image = cv2.resize(image, (new_width, new_height), interpolation=interpolation)
    return new_image


def rotate_image(image: np.ndarray, angle: float) -> np.ndarray:
    if image is None or not isinstance(image, np.ndarray) or image.ndim < 2:
        raise ValueError("image must be a valid numpy array")

    angle = float(angle)
    if angle == 0:
        return image

    height, width = image.shape[:2]

    center = (width / 2, height / 2)

    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1)

    rotated_image = cv2.warpAffine(
        image,
        rotation_matrix,
        (width, height),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_REPLICATE,
    )
    return rotated_image
