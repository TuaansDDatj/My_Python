import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from PIL import Image, ImageTk  # Import Pillow

from GUI.user_interface import UserInterface
from GUI.admin_interface import LibraryApp
from GUI.thuthu_interface import ThuthuApp

class LoginView:
    def __init__(self, root, db, book_manager, user_manager, borrow_manager, return_manager, report_manager):
        self.root = root
        self.db = db
        self.book_manager = book_manager
        self.user_manager = user_manager
        self.borrow_manager = borrow_manager
        self.return_manager = return_manager
        self.report_manager = report_manager

        self.setup_ui()

    def setup_ui(self):
        self.root.title("ĐĂNG NHẬP - THƯ VIỆN ĐẠI HỌC CÔNG NGHỆ ĐÔNG Á")
        self.root.geometry("400x450")
        self.root.configure(bg="#f8f9fa")
        self.root.resizable(False, False)

        # Căn giữa màn hình
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 460) // 2
        y = (screen_height - 450) // 2
        self.root.geometry(f"460x450+{x}+{y}")

        # Main frame
        main_frame = tk.Frame(self.root, bg="#f8f9fa", padx=40, pady=30)
        main_frame.pack(fill="both", expand=True)

        #Logo
        # image_path = "C:\\Users\\Admin\\Pictures\\Icon\\logoEAUT.png"
        # self.logo_image = Image.open(image_path)
        # self.logo_image = self.logo_image.resize((120, 120), Image.LANCZOS)
        # self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        
        # logo_label = tk.Label(main_frame, image=self.logo_photo, bg="#f8f9fa")
        # logo_label.pack(pady=(0, 30))

        # Username field
        username_frame = tk.Frame(main_frame, bg="#f8f9fa")
        username_frame.pack(fill="x", pady=5)

        username_label = tk.Label(username_frame, text="Mã độc giả:", font=("Arial", 11), bg="#f8f9fa", width=12, anchor="e")
        username_label.pack(side="left", padx=5)

        self.username_entry = tk.Entry(username_frame, font=("Arial", 11), width=20, bd=2, relief="groove")
        self.username_entry.pack(side="left", padx=5)

        # Password field
        password_frame = tk.Frame(main_frame, bg="#f8f9fa")
        password_frame.pack(fill="x", pady=5)

        password_label = tk.Label(password_frame, text="Mật khẩu:", font=("Arial", 11), bg="#f8f9fa", width=12, anchor="e")
        password_label.pack(side="left", padx=5)

        self.password_entry = tk.Entry(password_frame, font=("Arial", 11), width=20, show="•", bd=2, relief="groove")
        self.password_entry.pack(side="left", padx=5)


        # Login button
        button_frame = tk.Frame(main_frame, bg="#f8f9fa")
        button_frame.pack(pady=25)

        login_button = tk.Button(button_frame, text="ĐĂNG NHẬP", bg="#3498db", fg="white",
        font=("Arial", 12), width=18, relief="flat", command=self.login)
        login_button.pack()

        # Bind Enter key to login
        self.root.bind("<Return>", lambda event: self.login())

        # Footer
        footer_label = tk.Label(main_frame, text="Phát triển bởi Nhóm 23_IT13.10.9 \u00A9 2025",
                                font=("Arial", 10), bg="#f8f9fa", fg="#7f8c8d")
        footer_label.pack(side="bottom", pady=10)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập mã độc giả và mật khẩu!")
            return

        # Xác thực đăng nhập
        user = self.user_manager.verify_login(username, password)

        if user:
            self.root.withdraw()

            # Tạo cửa sổ mới cho ứng dụng chính
            app_window = tk.Toplevel(self.root)
            app_window.protocol("WM_DELETE_WINDOW", self.on_closing)

            print(f"Đăng nhập với quyền: '{user[6]}'")
            if user[6].strip() == "Admin":
                LibraryApp(app_window, self.db, self.book_manager, self.user_manager,
                           self.borrow_manager, self.return_manager, self.report_manager)
            elif user[6].strip() == "Thủ Thư":
                ThuthuApp(app_window, self.db, self.book_manager, self.user_manager,
                          self.borrow_manager, self.return_manager, self.report_manager)
            else:
                UserInterface(app_window, user, self.db, self.book_manager,
                              self.borrow_manager, self.return_manager)

            # Thiết lập kích thước và vị trí
            app_window.state('zoomed')  # Maximize window
        else:
            messagebox.showerror("Lỗi đăng nhập", "Mã độc giả hoặc mật khẩu không đúng!")

    def on_closing(self):
        if messagebox.askyesno("Thoát", "Bạn có chắc chắn muốn thoát khỏi ứng dụng?"):
            self.db.close_connection()
            self.root.destroy()
