"""
Module xử lý ảnh và vẽ kết quả nhận diện

Luồng xử lý ảnh:
1. read_image: Đọc file ảnh -> numpy array (BGR format) để xử lý với OpenCV
2. process_yolo_results: Kết quả YOLO -> Danh sách detections chuẩn hóa
3. draw_detections: Vẽ bounding boxes lên ảnh BGR
4. resize_image_for_display: Chuyển BGR->RGB và resize để hiển thị trong UI
"""
import cv2
from PIL import Image
from typing import List, Dict, Tuple, Any


class ImageProcessor:
    """
    Class xử lý ảnh và vẽ kết quả
    
    Tất cả các method đều là static vì không cần lưu trữ state
    """
    
    @staticmethod
    def read_image(image_path: str) -> Any:
        """
        Đọc ảnh từ file và trả về numpy array
        
        Input: image_path (str) - Đường dẫn file ảnh
        Output: numpy array (BGR format) - Ảnh để xử lý với OpenCV
        
        Lưu ý: OpenCV đọc ảnh theo format BGR (khác RGB thông thường)
        """
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Không thể đọc ảnh từ: {image_path}")
        return image
    
    @staticmethod
    def resize_image_for_display(image: Any, max_size: Tuple[int, int] = (600, 500)) -> Image.Image:
        """
        Chuyển đổi và resize ảnh để hiển thị trong giao diện
        
        Input: 
        - image: numpy array (BGR format từ OpenCV)
        - max_size: (width, height) - Kích thước tối đa
        
        Output: PIL Image (RGB format) đã resize
        
        Luồng: BGR numpy array -> RGB numpy array -> PIL Image -> Resize
        """
        # Chuyển từ BGR (OpenCV) sang RGB (PIL)
        if len(image.shape) == 3 and image.shape[2] == 3:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            image_rgb = image
        
        # Chuyển sang PIL Image và resize
        img_pil = Image.fromarray(image_rgb)
        img_pil.thumbnail(max_size, Image.Resampling.LANCZOS)
        return img_pil
    
    @staticmethod
    def draw_detections(image_bgr: Any, detections: List[Dict]) -> Any:
        """
        Vẽ bounding boxes và labels lên ảnh
        
        Input:
        - image_bgr: numpy array (BGR format) - Ảnh gốc
        - detections: List[Dict] - Danh sách các đối tượng được phát hiện
          Format: [{'name': str, 'confidence': float, 'bbox': (x1,y1,x2,y2)}, ...]
        
        Output: numpy array (BGR format) - Ảnh đã vẽ boxes và labels
        
        Luồng: Copy ảnh -> Vẽ box cho mỗi detection -> Vẽ label -> Trả về
        """
        # Copy ảnh để không thay đổi ảnh gốc
        annotated_image = image_bgr.copy()
        
        # Vẽ box và label cho mỗi đối tượng được phát hiện
        for detection in detections:
            # Lấy tọa độ bounding box
            x1, y1, x2, y2 = detection['bbox']
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            
            # Màu xanh lá (BGR format)
            color = (0, 255, 0)
            
            # Vẽ hình chữ nhật bounding box
            cv2.rectangle(annotated_image, (x1, y1), (x2, y2), color, 2)
            
            # Chuẩn bị text label (tên + độ tin cậy)
            label = f"{detection['name']} {detection['confidence']:.2f}"
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            
            # Vẽ background cho label (hình chữ nhật màu xanh)
            cv2.rectangle(
                annotated_image,
                (x1, y1 - label_size[1] - 10),
                (x1 + label_size[0], y1),
                color,
                -1
            )
            
            # Vẽ text label (màu đen)
            cv2.putText(
                annotated_image,
                label,
                (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 0),
                2
            )
        
        return annotated_image
    
    @staticmethod
    def process_yolo_results(yolo_results) -> List[Dict]:
        """
        Xử lý kết quả từ YOLO model thành format chuẩn
        
        Input: yolo_results - Kết quả từ YOLO model (ultralytics format)
        Output: List[Dict] - Danh sách các đối tượng được phát hiện
          Format: [{'name': str, 'confidence': float, 'bbox': (x1,y1,x2,y2)}, ...]
        
        Luồng: YOLO results -> Lặp qua các box -> Trích xuất thông tin -> Chuẩn hóa format
        """
        detected_objects = []
        
        # YOLO trả về list các result (mỗi result cho một ảnh)
        for result in yolo_results:
            boxes = result.boxes
            
            # Lặp qua từng bounding box được phát hiện
            for box in boxes:
                # Trích xuất thông tin: class ID, confidence, tọa độ
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                
                # Lấy tên class từ model
                class_name = result.names[class_id] if hasattr(result, 'names') else f"Class {class_id}"
                
                # Thêm vào danh sách với format chuẩn
                detected_objects.append({
                    'name': class_name,
                    'confidence': confidence,
                    'bbox': (x1, y1, x2, y2)
                })
        
        return detected_objects
