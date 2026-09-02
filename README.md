# ĐỒ ÁN HỌC PHẦN: XỬ LÝ ẢNH SỐ

## PROJECT 1: IMAGE VIEWER

Ứng dụng xử lý và biến đổi hình học cơ bản trên ảnh số (Zoom, Rotate, Crop), hiển thị so sánh trực quan trước/sau xử lý và hỗ trợ lưu kết quả thông qua giao diện đồ họa người dùng (GUI).

---

## 1. Phân công nhiệm vụ

| Thành viên | Nhiệm vụ chính                         | Chi tiết công việc thực hiện                                                                                                                                                                                                                                                                                                        |
| :--------- | :------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Khôi**   | Biến đổi hình học (Zoom & Rotate)      | - Cài đặt thuật toán Zoom ảnh theo tỉ lệ scale.<br>- Cài đặt thuật toán Rotate ảnh theo góc xoay tùy ý.<br>- Xử lý nhận tham số biến đổi và trả về ma trận ảnh sau xử lý.                                                                                                                                                           |
| **Kỳ**     | Cắt ảnh & Quản lý dữ liệu (Crop & I/O) | - Cài đặt thuật toán Crop ảnh theo vùng chọn/tọa độ (x, y, w, h).<br>- Viết chức năng lưu ảnh kết quả xuống ổ cứng.<br>- Chuẩn bị bộ dữ liệu thử nghiệm tối thiểu 10 ảnh test đa dạng kích thước, định dạng.                                                                                                                        |
| **Bắc**    | Giao diện & Tích hợp hệ thống (GUI)    | - Xây dựng giao diện chính: Khung hiển thị song song ảnh gốc (Before) và ảnh kết quả (After).<br>- Tạo các widget điều khiển: Nút mở ảnh, thanh trượt/ô nhập tham số Zoom, Rotate, Crop, nút lưu ảnh.<br>- Ghép nối mã nguồn của Khôi và Kỳ thành chương trình hoàn chỉnh.<br>- Quản lý luồng tương tác và xử lý ngoại lệ trên GUI. |

---

## 2. Cấu trúc thư mục

```text
image_viewer_project/
│
├── data/                           # Dữ liệu thử nghiệm
│   ├── input/                      # Chứa ít nhất 10 ảnh gốc phục vụ kiểm thử
│   └── output/                     # Nơi lưu ảnh sau khi xử lý từ GUI
│
├── src/                            # Mã nguồn ứng dụng
│   ├── __init__.py
│   ├── main.py                     # Điểm khởi chạy chương trình (Entry point)
│   │
│   ├── core/                       # Thuật toán xử lý ảnh thuần túy
│   │   ├── __init__.py
│   │   ├── transform.py            # Module phóng to/thu nhỏ và xoay ảnh
│   │   └── crop_io.py              # Module cắt ảnh và xuất file ảnh
│   │
│   ├── gui/                        # Giao diện người dùng
│   │   ├── __init__.py
│   │   ├── main_window.py          # Cửa sổ chính, bố cục hiển thị Trước/Sau
│   │   └── widgets.py              # Thanh trượt, nút bấm, ô nhập tham số
│   │
│   └── utils/                      # Tiện ích bổ trợ
│       ├── __init__.py
│       └── helpers.py              # Chuyển đổi định dạng ma trận ảnh sang định dạng GUI
│
├── docs/                           # Hồ sơ báo cáo
│   ├── bao_cao_thuat_toan.docx     # Báo cáo kỹ thuật và phân tích kết quả
│   └── demo_link.txt               # Đường dẫn video demo (5 - 15 phút)
│
├── .gitignore                      # Danh sách file/thư mục bỏ qua khi commit
├── README.md                       # Tài liệu hướng dẫn dự án
└── requirements.txt                # Thư viện phụ thuộc cần cài đặt
```

---

## 3. Vai trò chi tiết từng thư mục và tệp tin

### Thư mục dữ liệu: `data/`

- **`data/input/`**: Nơi **Kỳ** lưu trữ tối thiểu 10 ảnh kiểm thử đa dạng định dạng (`.jpg`, `.png`) và độ phân giải khác nhau để phục vụ việc test tính năng.
- **`data/output/`**: Thư mục đích dùng để lưu ảnh sau khi người dùng thực hiện thao tác xử lý và nhấn lưu trên giao diện.

### Thư mục mã nguồn: `src/`

- **`src/main.py`**: Do **Bắc** phụ trách. Điểm khởi chạy ứng dụng, khởi tạo vòng lặp giao diện và liên kết các thành phần hệ thống.

### Phân tầng xử lý lõi: `src/core/`

Chứa toàn bộ thuật toán xử lý ảnh số, tách biệt hoàn toàn khỏi giao diện người dùng:

- **`src/core/transform.py`**: Do **Khôi** phụ trách.
  - Thuật toán Zoom ảnh theo tỉ lệ (phóng to/thu nhỏ nội suy).
  - Thuật toán Rotate ảnh theo góc xoay quanh tâm.
- **`src/core/crop_io.py`**: Do **Kỳ** phụ trách.
  - Thuật toán Crop ảnh trích xuất vùng quan tâm dựa trên tọa độ và kích thước.
  - Hàm lưu ảnh an toàn xuống đĩa cứng.

### Phân tầng giao diện: `src/gui/`

Chứa mã nguồn đồ họa do **Bắc** phụ trách:

- **`src/gui/main_window.py`**: Bố cục cửa sổ chính, quản lý hai khung hiển thị song song (ảnh gốc và ảnh sau khi biến đổi), điều hướng luồng dữ liệu.
- **`src/gui/widgets.py`**: Xây dựng các khối điều khiển: Sliders góc xoay/tỉ lệ phóng to, ô nhập tọa độ crop, nút Open/Save/Reset.

### Phân tầng tiện ích: `src/utils/`

- **`src/utils/helpers.py`**: Chứa hàm tiện ích hỗ trợ chuyển đổi mảng `numpy.ndarray` (chuẩn OpenCV) sang định dạng tương thích để hiển thị trực tiếp lên canvas/khung hình của GUI toolkit.

### Thư mục tài liệu: `docs/`

- **`docs/bao_cao_thuat_toan.docx`**: Tài liệu trình bày giải thuật, cơ sở lý thuyết, phân tích kết quả thực nghiệm và bảng đánh giá đóng góp.
- **`docs/demo_link.txt`**: Tệp văn bản lưu đường dẫn video quay trực tiếp quá trình thao tác phần mềm (thời lượng 5 – 15 phút).

### Cấu hình dự án

- **`.gitignore`**: Loại trừ các thư mục không cần thiết (`venv/`, `__pycache__/`, tệp tạm OS) khi đẩy lên GitHub.
- **`requirements.txt`**: Khai báo phiên bản các thư viện như `opencv-python`, `numpy`, `pillow`.
- **`README.md`**: Bản mô tả toàn diện về cấu trúc, phân công và cách vận hành dự án.

---

## 4. Quy chuẩn giao tiếp hàm (Interface)

Tất cả các hàm xử lý ảnh thống nhất nhận và trả về ma trận dữ liệu ảnh dạng `numpy.ndarray`:

```python
# src/core/transform.py (Khôi)
def zoom_image(image: np.ndarray, scale: float) -> np.ndarray:
    """Phóng to/thu nhỏ ảnh theo tỉ lệ scale."""
    pass

def rotate_image(image: np.ndarray, angle: float) -> np.ndarray:
    """Xoay ảnh một góc angle (độ)."""
    pass


# src/core/crop_io.py (Kỳ)
def crop_image(image: np.ndarray, x: int, y: int, w: int, h: int) -> np.ndarray:
    """Cắt vùng ảnh từ tọa độ (x, y) với độ rộng w và chiều cao h."""
    pass

def save_image(image: np.ndarray, file_path: str) -> bool:
    """Ghi dữ liệu ảnh xuống file_path chỉ định."""
    pass
```

---

## 5. Cài đặt và vận hành

```bash
# 1. Cài đặt thư viện
pip install -r requirements.txt

# 2. Khởi chạy giao diện
python src/main.py
```
