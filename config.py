"""
File cấu hình cho ứng dụng nhận diện hoa quả
"""
from pathlib import Path

# Đường dẫn thư mục gốc
BASE_DIR = Path(__file__).parent

# Đường dẫn mô hình
MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "best.pt"

# Cấu hình giao diện
WINDOW_TITLE = "Ứng dụng Nhận diện Hoa quả"
WINDOW_SIZE = "900x700"
WINDOW_BG = "#f0f0f0"

# Màu sắc
COLORS = {
    "primary": "#2c3e50",
    "success": "#27ae60",
    "warning": "#f39c12",
    "danger": "#e74c3c",
    "info": "#3498db",
    "light": "#ecf0f1",
    "text": "#2c3e50",
    "text_light": "#7f8c8d"
}

# Kích thước ảnh hiển thị
IMAGE_DISPLAY_SIZE = (600, 500)

# Định dạng ảnh được hỗ trợ
SUPPORTED_IMAGE_FORMATS = [
    ("Ảnh", "*.jpg *.jpeg *.png *.bmp *.gif"),
    ("Tất cả", "*.*")
]
