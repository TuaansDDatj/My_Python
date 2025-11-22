"""
Module xử lý việc load và quản lý mô hình

Luồng load model:
1. Kiểm tra file tồn tại
2. Thử load với YOLO (ultralytics) trước
3. Nếu không được, thử load với PyTorch
4. Lưu model và model_type để sử dụng sau
"""
import torch
from pathlib import Path
from config import MODEL_PATH


class ModelLoader:
    """
    Class để load và quản lý mô hình nhận diện
    
    Quản lý:
    - model_path: Đường dẫn đến file mô hình (.pt)
    - model: Mô hình đã load (YOLO hoặc PyTorch)
    - model_type: Loại mô hình ("yolo" hoặc "torch")
    """
    
    def __init__(self, model_path=None):
        """
        Khởi tạo ModelLoader
        
        Input: model_path (str, optional) - Đường dẫn file mô hình
               Nếu None, dùng MODEL_PATH từ config
        """
        self.model_path = model_path or MODEL_PATH
        self.model = None
        self.model_type = None
    
    def load(self):
        """
        Load mô hình từ file
        
        Output: tuple (model, model_type) hoặc (None, None) nếu lỗi
        
        Luồng:
        1. Kiểm tra file tồn tại
        2. Thử load với YOLO (ưu tiên)
        3. Nếu không được, thử load với PyTorch
        4. Trả về model và loại model
        """
        try:
            # Kiểm tra file tồn tại
            if not Path(self.model_path).exists():
                raise FileNotFoundError(f"Không tìm thấy file mô hình: {self.model_path}")
            
            # Ưu tiên load với YOLO (ultralytics)
            try:
                from ultralytics import YOLO
                self.model = YOLO(str(self.model_path))
                self.model_type = "yolo"
                return self.model, self.model_type
            except ImportError:
                # Fallback: Load với PyTorch thông thường
                checkpoint = torch.load(self.model_path, map_location='cpu')
                if isinstance(checkpoint, dict) and 'model' in checkpoint:
                    self.model = checkpoint['model']
                else:
                    self.model = checkpoint
                
                # Đặt model về chế độ evaluation
                if hasattr(self.model, 'eval'):
                    self.model.eval()
                
                self.model_type = "torch"
                return self.model, self.model_type
                
        except Exception as e:
            print(f"Lỗi khi load mô hình: {e}")
            return None, None
    
    def is_loaded(self):
        """Kiểm tra xem mô hình đã được load chưa"""
        return self.model is not None
    
    def get_model(self):
        """Lấy mô hình đã load"""
        return self.model
    
    def get_model_type(self):
        """Lấy loại mô hình"""
        return self.model_type
