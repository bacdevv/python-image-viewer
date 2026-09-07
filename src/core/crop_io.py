import os

import cv2
import numpy as np

"""Cắt vùng ảnh từ tọa độ (x, y) với độ rộng w và chiều cao h."""


def load_image(
    file_path: str | os.PathLike, flags: int = cv2.IMREAD_UNCHANGED
) -> np.ndarray:
    """Read an image from a Unicode path on Windows and other platforms."""
    path = os.fspath(file_path)
    if not path:
        raise ValueError("Lỗi: Đường dẫn đọc ảnh không hợp lệ.")

    try:
        encoded = np.fromfile(path, dtype=np.uint8)
        image = cv2.imdecode(encoded, flags)
    except (OSError, cv2.error) as error:
        raise ValueError(f"Lỗi khi đọc ảnh: {error}") from error

    if image is None:
        raise ValueError(f"Lỗi: Không thể đọc ảnh từ đường dẫn: {path}")
    return image


def crop_image(image: np.ndarray, x: int, y: int, w: int, h: int) -> np.ndarray:
    # Kiểm tra tính hợp lệ của ảnh và các tham số đầu vào xem ảnh có phải là mảng numpy và có ít nhất 2 chiều và có none hay không.
    if image is None or not isinstance(image, np.ndarray) or image.ndim < 2:
        raise ValueError("Lỗi: Ảnh không hợp lệ hoặc không phải là mảng numpy.")

    if w <= 0 or h <= 0:
        raise ValueError("Lỗi: Chiều rộng và chiều cao phải lớn hơn 0.")

    img_h, img_w = image.shape[:2]

    # Kỹ thuật chặn biên (Clipping): Đảm bảo tọa độ không bị âm hoặc lố ra ngoài ảnh
    x_start = max(0, x)
    y_start = max(0, y)
    x_end = min(x + w, img_w)
    y_end = min(y + h, img_h)

    if x_start >= x_end or y_start >= y_end:
        raise ValueError("Lỗi: Khung cắt nằm ngoài phạm vi ảnh.")

    cropped_image = image[y_start:y_end, x_start:x_end]
    return cropped_image


def save_image(image: np.ndarray, file_path: str) -> bool:
    if image is None or not isinstance(image, np.ndarray):
        raise ValueError("Lỗi: Ảnh không hợp lệ hoặc không phải là mảng numpy.")
    if not file_path or not isinstance(file_path, (str, os.PathLike)):
        raise ValueError("Lỗi: Đường dẫn lưu ảnh không hợp lệ.")
    try:
        parent_dir = os.path.dirname(os.fspath(file_path))
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
        extension = os.path.splitext(os.fspath(file_path))[1]
        if not extension:
            raise ValueError("Lỗi: Đường dẫn lưu ảnh phải có phần mở rộng.")
        success, encoded = cv2.imencode(extension, image)
        if success:
            encoded.tofile(os.fspath(file_path))
        return bool(success)
    except Exception as e:
        raise ValueError(f"Lỗi khi lưu ảnh: {e}")


# hàm test
if __name__ == "__main__":
    current_dir = os.path.dirname(
        os.path.abspath(__file__)
    )  # Lấy đường dẫn tuyệt đối của thư mục chứa crop_io.py (src/core)
    project_root = os.path.abspath(
        os.path.join(current_dir, "..", "..")
    )  # Lùi lại 2 cấp để ra thư mục gốc python-image-viewer

    input_path = os.path.join(project_root, "data", "input", "baboon.png")
    output_dir = os.path.join(project_root, "data", "output")
    os.makedirs(output_dir, exist_ok=True)  # Tự tạo thư mục output nếu chưa có

    test_image = load_image(input_path)

    if test_image is not None:
        print("kích thước ảnh gốc: ", test_image.shape)
        result_img = crop_image(test_image, x=100, y=100, w=200, h=200)
        # không cần kiểm tra result_img có phải là None hay không vì crop_image đã kiểm tra và raise ValueError nếu ảnh không hợp lệ (nếu result_img là None thì sẽ raise ValueError và không đến được dòng này)
        try:
            print("kích thước ảnh sau khi crop: ", result_img.shape)
            # lưu ảnh crop vào thư mục output
            img_name = os.path.basename(input_path)
            name, extension = os.path.splitext(img_name)
            new_img_name = f"{name}_cropped{extension}"  # tên ảnh crop mới

            out_file_path = os.path.join(
                output_dir, new_img_name
            )  # os.path.join để tạo tên và đường dẫn lưu ảnh mới
            is_saved = save_image(
                result_img, out_file_path
            )  # kiểm tra xem ảnh đã lưu thành công chưa
            if is_saved:
                print(
                    f"Trạng thái: ảnh lưu {'Thành công' if is_saved else 'Thất bại'}  tại: {out_file_path}"
                )

            cv2.imshow("Ảnh gốc: ", test_image)
            cv2.imshow("Ảnh sau khi crop: ", result_img)
            cv2.waitKey(0)  # Dừng chương trình chờ người dùng bấm phím bất kỳ
            cv2.destroyAllWindows()  # đóng tất cả các cửa sổ hiển thị ảnh

        except ValueError as e:
            print(e)
    else:
        print("Lỗi: Không thể đọc ảnh từ đường dẫn:", input_path)
