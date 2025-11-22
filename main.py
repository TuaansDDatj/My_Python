"""
Entry point của ứng dụng nhận diện hoa quả
"""
import tkinter as tk
from ui.main_window import MainWindow


def main():
    """Hàm main để chạy ứng dụng"""
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
