# Ứng dụng Nhận diện Hoa quả

Ứng dụng desktop đơn giản sử dụng Tkinter để nhận diện các loại hoa quả từ ảnh.

## Cấu trúc thư mục

```
fruit_app/
├── models/
│   └── best.pt          # Mô hình nhận diện hoa quả
├── ui/
│   ├── __init__.py
│   ├── components.py    # Các component UI tái sử dụng
│   └── main_window.py   # Cửa sổ chính
├── utils/
│   ├── __init__.py
│   ├── model_loader.py  # Xử lý load mô hình
│   └── image_processor.py # Xử lý ảnh và vẽ kết quả
├── config.py            # File cấu hình
├── main.py              # Entry point
├── requirements.txt     # Các thư viện cần thiết
└── README.md
```

## Cài đặt

1. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

2. Đảm bảo file `best.pt` (mô hình nhận diện hoa quả) có trong thư mục `models/`.

## Sử dụng

Chạy ứng dụng:
```bash
python main.py
```

### Các chức năng:
- **Chọn ảnh**: Chọn ảnh hoa quả từ máy tính
- **Nhận diện**: Phát hiện và nhận diện các loại hoa quả trong ảnh
- **Xóa**: Xóa ảnh và kết quả hiện tại

## Yêu cầu hệ thống

- Python 3.8 trở lên
- Mô hình `best.pt` (YOLO format) trong thư mục `models/`

## Cấu trúc code

- **config.py**: Chứa tất cả các cấu hình (đường dẫn, màu sắc, kích thước)
- **utils/model_loader.py**: Xử lý việc load và quản lý mô hình
- **utils/image_processor.py**: Xử lý ảnh, vẽ bounding boxes
- **ui/components.py**: Các component UI tái sử dụng (StyledButton, StatusLabel, etc.)
- **ui/main_window.py**: Logic chính của cửa sổ ứng dụng
- **main.py**: Entry point để chạy ứng dụng

