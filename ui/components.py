"""
Các component UI tái sử dụng được
"""
import tkinter as tk
from config import COLORS


class StyledButton(tk.Button):
    """Button với style mặc định"""
    
    def __init__(self, parent, text="", command=None, bg_color="#3498db", **kwargs):
        default_kwargs = {
            "font": ("Arial", 12, "bold"),
            "bg": bg_color,
            "fg": "white",
            "relief": tk.FLAT,
            "padx": 20,
            "pady": 10,
            "cursor": "hand2",
            "command": command
        }
        default_kwargs.update(kwargs)
        super().__init__(parent, text=text, **default_kwargs)


class StatusLabel(tk.Label):
    """Label hiển thị trạng thái"""
    
    def __init__(self, parent, **kwargs):
        default_kwargs = {
            "font": ("Arial", 9),
            "bg": "white",
            "fg": COLORS["success"],
            "anchor": "w"
        }
        default_kwargs.update(kwargs)
        super().__init__(parent, **default_kwargs)
    
    def update_status(self, message, color=None):
        """Cập nhật trạng thái"""
        if color is None:
            color = COLORS["success"]
        self.config(text=message, fg=color)


class ScrollableText(tk.Frame):
    """Text widget có scrollbar"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Text widget
        text_kwargs = {
            "font": ("Arial", 9),
            "bg": COLORS["light"],
            "fg": COLORS["text"],
            "wrap": tk.WORD,
            "yscrollcommand": scrollbar.set,
            "relief": tk.FLAT,
            "padx": 10,
            "pady": 10
        }
        text_kwargs.update(kwargs)
        
        self.text = tk.Text(self, **text_kwargs)
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text.yview)
    
    def clear(self):
        """Xóa nội dung"""
        self.text.delete(1.0, tk.END)
    
    def insert(self, *args, **kwargs):
        """Chèn text"""
        self.text.insert(*args, **kwargs)
    
    def get(self, *args, **kwargs):
        """Lấy nội dung"""
        return self.text.get(*args, **kwargs)
