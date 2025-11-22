"""
Cửa sổ chính của ứng dụng

Luồng dữ liệu:
1. Khởi tạo -> Load model -> Hiển thị giao diện
2. User chọn ảnh -> Lưu đường dẫn -> Hiển thị ảnh preview
3. User nhấn nhận diện -> Đọc ảnh -> Chạy model -> Xử lý kết quả -> Vẽ boxes -> Hiển thị
4. User nhấn xóa -> Reset tất cả về trạng thái ban đầu
"""
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

from config import (
    WINDOW_TITLE, WINDOW_SIZE, WINDOW_BG, COLORS,
    IMAGE_DISPLAY_SIZE, SUPPORTED_IMAGE_FORMATS
)
from utils.model_loader import ModelLoader
from utils.image_processor import ImageProcessor
from ui.components import StyledButton, StatusLabel, ScrollableText


class MainWindow:
    """
    Cửa sổ chính của ứng dụng
    
    Quản lý:
    - model_loader: Load và quản lý mô hình AI
    - image_processor: Xử lý ảnh và vẽ kết quả
    - current_image_path: Đường dẫn ảnh hiện tại
    - current_image: Ảnh đang hiển thị (PhotoImage object)
    """
    
    def __init__(self, root):
        # Khởi tạo cửa sổ
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.configure(bg=WINDOW_BG)
        
        # Khởi tạo các component xử lý
        self.model_loader = ModelLoader()
        self.image_processor = ImageProcessor()
        
        # State: Lưu trữ dữ liệu hiện tại
        self.current_image = None
        self.current_image_path = None
        
        # Tạo giao diện và load model
        self.create_widgets()
        self.load_model()
    
    def create_widgets(self):
        self.create_header()
        
        main_frame = tk.Frame(self.root, bg=WINDOW_BG)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.create_image_panel(main_frame)
        self.create_control_panel(main_frame)
    
    def create_header(self):
        """Tạo header"""
        header_frame = tk.Frame(self.root, bg=COLORS["primary"], height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🍎 Nhận diện Hoa quả 🍌",
            font=("Arial", 24, "bold"),
            bg=COLORS["primary"],
            fg="white"
        )
        title_label.pack(pady=20)
    
    def create_image_panel(self, parent):
        """Tạo panel hiển thị ảnh"""
        left_frame = tk.Frame(parent, bg="white", relief=tk.RAISED, bd=2)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.image_label = tk.Label(
            left_frame,
            text="Chưa có ảnh",
            font=("Arial", 14),
            bg="white",
            fg=COLORS["text_light"]
        )
        self.image_label.pack(expand=True)
    
    def create_control_panel(self, parent):
        """Tạo panel điều khiển và kết quả"""
        right_frame = tk.Frame(parent, bg="white", relief=tk.RAISED, bd=2, width=300)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        right_frame.pack_propagate(False)
        
        self.create_control_buttons(right_frame)
        self.create_status_section(right_frame)
        self.create_results_section(right_frame)
    
    def create_control_buttons(self, parent):
        """Tạo các nút điều khiển"""
        control_frame = tk.Frame(parent, bg="white")
        control_frame.pack(fill=tk.X, padx=15, pady=15)
        
        StyledButton(
            control_frame,
            text="📁 Chọn ảnh",
            bg_color=COLORS["info"],
            command=self.select_image
        ).pack(fill=tk.X, pady=(0, 10))
        
        StyledButton(
            control_frame,
            text="🔍 Nhận diện",
            bg_color=COLORS["success"],
            command=self.detect_fruits
        ).pack(fill=tk.X, pady=(0, 10))
        
        StyledButton(
            control_frame,
            text="🗑️ Xóa",
            bg_color=COLORS["danger"],
            command=self.clear_image
        ).pack(fill=tk.X)
    
    def create_status_section(self, parent):
        """Tạo phần hiển thị trạng thái"""
        status_frame = tk.Frame(parent, bg="white")
        status_frame.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(
            status_frame,
            text="Trạng thái:",
            font=("Arial", 10, "bold"),
            bg="white",
            anchor="w"
        ).pack(fill=tk.X)
        
        self.status_label = StatusLabel(status_frame)
        self.status_label.pack(fill=tk.X)
    
    def create_results_section(self, parent):
        """Tạo phần hiển thị kết quả"""
        results_frame = tk.Frame(parent, bg="white")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        tk.Label(
            results_frame,
            text="Kết quả nhận diện:",
            font=("Arial", 10, "bold"),
            bg="white",
            anchor="w"
        ).pack(fill=tk.X, pady=(0, 10))
        
        results_container = tk.Frame(results_frame, bg="white")
        results_container.pack(fill=tk.BOTH, expand=True)
        
        self.results_text = ScrollableText(results_container)
        self.results_text.pack(fill=tk.BOTH, expand=True)
    
    def load_model(self):
        """
        Bước 1: Load mô hình AI khi khởi động ứng dụng
        
        Luồng: Hiển thị trạng thái -> Load model -> Cập nhật trạng thái
        """
        self.status_label.update_status("Đang tải mô hình...", COLORS["warning"])
        self.root.update()
        
        model, model_type = self.model_loader.load()
        
        if model:
            self.status_label.update_status("Mô hình đã tải thành công!", COLORS["success"])
        else:
            self.status_label.update_status("Lỗi khi tải mô hình", COLORS["danger"])
            messagebox.showerror("Lỗi", "Không thể tải mô hình!")
    
    def select_image(self):
        """
        Bước 2: User chọn ảnh từ máy tính
        
        Luồng: Mở dialog chọn file -> Lưu đường dẫn -> Hiển thị preview
        """
        file_path = filedialog.askopenfilename(
            title="Chọn ảnh hoa quả",
            filetypes=SUPPORTED_IMAGE_FORMATS
        )
        
        if file_path:
            self.current_image_path = file_path
            self.display_image(file_path)
            self.status_label.update_status("Đã chọn ảnh", COLORS["info"])
    
    def display_image(self, image_path):
        """
        Hiển thị ảnh preview trong giao diện
        
        Input: image_path (str) - Đường dẫn đến file ảnh
        Output: Cập nhật image_label với ảnh đã resize
        """
        try:
            img = Image.open(image_path)
            img.thumbnail(IMAGE_DISPLAY_SIZE, Image.Resampling.LANCZOS)
            
            self.current_image = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.current_image, text="")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể hiển thị ảnh:\n{str(e)}")
    
    def detect_fruits(self):
        """
        Bước 3: Nhận diện hoa quả trong ảnh
        
        Luồng dữ liệu:
        1. Kiểm tra có ảnh và model không
        2. Đọc ảnh từ đường dẫn (BGR format)
        3. Chạy model YOLO để nhận diện
        4. Xử lý kết quả thành danh sách detections
        5. Vẽ bounding boxes lên ảnh
        6. Hiển thị kết quả và ảnh đã đánh dấu
        """
        # Kiểm tra điều kiện
        if not self.current_image_path:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn ảnh trước!")
            return
        
        if not self.model_loader.is_loaded():
            messagebox.showerror("Lỗi", "Mô hình chưa được tải!")
            return
        
        try:
            # Cập nhật trạng thái
            self.status_label.update_status("Đang nhận diện...", COLORS["warning"])
            self.root.update()
            
            # Bước 1: Đọc ảnh (trả về numpy array BGR format)
            image_bgr = self.image_processor.read_image(self.current_image_path)
            
            # Bước 2: Lấy model và chạy nhận diện
            model = self.model_loader.get_model()
            model_type = self.model_loader.get_model_type()
            
            if model_type == "yolo":
                # Chạy model YOLO (input: đường dẫn ảnh)
                yolo_results = model(self.current_image_path)
                
                # Bước 3: Xử lý kết quả YOLO thành danh sách detections
                detections = self.image_processor.process_yolo_results(yolo_results)
                
                # Bước 4: Hiển thị kết quả và vẽ boxes
                self.display_results(detections, image_bgr)
            else:
                messagebox.showwarning(
                    "Cảnh báo", 
                    "Mô hình không phải YOLO. Cần cấu hình thêm."
                )
            
        except Exception as e:
            self.status_label.update_status(f"Lỗi: {str(e)}", COLORS["danger"])
            messagebox.showerror("Lỗi", f"Lỗi khi nhận diện:\n{str(e)}")
    
    def display_results(self, detections, image_bgr):
        """
        Hiển thị kết quả nhận diện
        
        Input:
        - detections: List[Dict] - Danh sách các đối tượng được phát hiện
          Format: [{'name': str, 'confidence': float, 'bbox': (x1,y1,x2,y2)}, ...]
        - image_bgr: numpy array - Ảnh gốc (BGR format)
        
        Luồng:
        1. Xóa kết quả cũ
        2. Hiển thị danh sách detections trong text widget
        3. Vẽ bounding boxes lên ảnh
        4. Hiển thị ảnh đã đánh dấu
        5. Cập nhật trạng thái
        """
        # Xóa kết quả cũ
        self.results_text.clear()
        
        if detections:
            # Hiển thị danh sách kết quả
            self.results_text.insert(
                tk.END, 
                f"Đã phát hiện {len(detections)} đối tượng:\n\n"
            )
            
            for i, detection in enumerate(detections, 1):
                confidence_percent = detection['confidence'] * 100
                self.results_text.insert(
                    tk.END,
                    f"{i}. {detection['name']}\n"
                    f"   Độ tin cậy: {confidence_percent:.1f}%\n\n"
                )
            
            # Vẽ bounding boxes lên ảnh (input: ảnh BGR, output: ảnh BGR đã vẽ)
            annotated_image_bgr = self.image_processor.draw_detections(
                image_bgr.copy(), 
                detections
            )
            
            # Hiển thị ảnh đã đánh dấu
            self.display_annotated_image(annotated_image_bgr)
            
            # Cập nhật trạng thái
            self.status_label.update_status(
                f"Đã phát hiện {len(detections)} đối tượng", 
                COLORS["success"]
            )
        else:
            self.results_text.insert(
                tk.END, 
                "Không phát hiện hoa quả nào trong ảnh."
            )
            self.status_label.update_status(
                "Không phát hiện đối tượng", 
                COLORS["danger"]
            )
    
    def display_annotated_image(self, annotated_image_bgr):
        """
        Hiển thị ảnh đã được đánh dấu bounding boxes
        
        Input: annotated_image_bgr (numpy array) - Ảnh BGR đã vẽ boxes
        Luồng: BGR -> RGB -> PIL Image -> Resize -> PhotoImage -> Hiển thị
        """
        # Chuyển BGR sang RGB và resize để hiển thị
        img_pil = self.image_processor.resize_image_for_display(
            annotated_image_bgr, 
            IMAGE_DISPLAY_SIZE
        )
        
        # Chuyển sang PhotoImage để hiển thị trong Tkinter
        self.current_image = ImageTk.PhotoImage(img_pil)
        self.image_label.config(image=self.current_image, text="")
    
    def clear_image(self):
        """
        Bước 4: Xóa ảnh và reset về trạng thái ban đầu
        
        Luồng: Xóa đường dẫn -> Xóa ảnh -> Xóa kết quả -> Reset trạng thái
        """
        self.current_image = None
        self.current_image_path = None
        self.image_label.config(image="", text="Chưa có ảnh")
        self.results_text.clear()
        self.status_label.update_status("Sẵn sàng", COLORS["success"])
