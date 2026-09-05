import cv2
import numpy as np
def zoom_image(image: np.ndarray, scale: float) -> np.ndarray:
    if scale <= 0:
        raise ValueError("scale must be greater than 0")
    
    if scale == 1:
        return image
    
    height, width = image.shape[:2]
    
    new_width = int(width * scale)
    new_height = int(height * scale)

    if scale > 1:
        interpolation = cv2.INTER_LINEAR
    else:
        interpolation = cv2.INTER_AREA

    new_image = cv2.resize(image, (new_width, new_height), interpolation=interpolation)
    return new_image

def rotate_image(image: np.ndarray, angle: float) -> np.ndarray:
    if angle == 0:
        return image
    
    height, width = image.shape[:2]

    center = (width / 2, height / 2)

    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1)

    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))
    return rotated_image