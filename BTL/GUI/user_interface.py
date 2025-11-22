import sqlite3
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from datetime import datetime

class UserInterface:
    def __init__(self, root, user_data, db, book_manager, borrow_manager, return_manager):
        self.root = root
        self.user_data = user_data
        self.db = db
        self.book_manager = book_manager
        self.borrow_manager = borrow_manager
        self.return_manager = return_manager
        
        self.setup_ui()
    
    def setup_ui(self):
        # Thiết lập cấu hình cơ bản cho giao diện
        self.root.title(f"THƯ VIỆN ĐẠI HỌC - {self.user_data[1]}")
        self.root.geometry("1000x600")
        self.root.configure(bg="#f8f9fa")
        
        # Set theme for ttk widgets
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles
        style.configure('TButton', font=('Arial', 10), borderwidth=1)
        style.configure('Primary.TButton', background='#1abc9c', foreground='white')
        style.configure('Secondary.TButton', background='#3498db', foreground='white')
        
        # Configure treeview style
        style.configure('Treeview', font=('Arial', 9), rowheight=25)
        style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
        
        # Create frames
        self.create_menu_frame()
        self.content_frame = tk.Frame(self.root, bg="#f8f9fa")
        self.content_frame.pack(side="right", expand=True, fill="both")

        # Show default screen (book search)
        self.show_book_search()
    
    def create_menu_frame(self):
        menu_frame = tk.Frame(self.root, bg="#2c3e50", width=220)
        menu_frame.pack(side="left", fill="y")
        
        # Ensure menu frame maintains its width
        menu_frame.pack_propagate(False)
        
        # Add app title and greeting
        app_title = tk.Label(menu_frame, text="Thư Viện Đại Học", font=("Arial", 14, "bold"), 
                             bg="#2c3e50", fg="white", justify="center")
        app_title.pack(pady=(20, 5))
        
        welcome_text = f"Xin chào, {self.user_data[1]}!"
        welcome_label = tk.Label(menu_frame, text=welcome_text, font=("Arial", 11), 
                                 bg="#2c3e50", fg="white", justify="center", wraplength=200)
        welcome_label.pack(pady=(0, 5))
        
        user_type_text = f"Quyền: {self.user_data[6]}"
        user_type_label = tk.Label(menu_frame, text=user_type_text, font=("Arial", 10), 
                                   bg="#2c3e50", fg="#bdc3c7", justify="center")
        user_type_label.pack(pady=(0, 20))
        
        # Create separator
        separator = ttk.Separator(menu_frame, orient='horizontal')
        separator.pack(fill='x', padx=10, pady=10)
        
        # Menu buttons
        self.create_menu_button(menu_frame, "🔍 Tra cứu sách", self.show_book_search)
        self.create_menu_button(menu_frame, "📚 Sách đang mượn", self.show_current_borrows)
        self.create_menu_button(menu_frame, "📋 Lịch sử mượn trả", self.show_borrow_history)
        self.create_menu_button(menu_frame, "👤 Thông tin cá nhân", self.show_profile)
        
        # Create separator
        separator = ttk.Separator(menu_frame, orient='horizontal')
        separator.pack(fill='x', padx=10, pady=10)
        
        # Logout button at bottom
        logout_btn = tk.Button(menu_frame, text="🚪 Đăng Xuất", font=("Arial", 12), 
                               bg="#e74c3c", fg="white", relief="flat", 
                               padx=10, pady=7, width=20, anchor="w", 
                               activebackground="#c0392b", command=self.logout)
        logout_btn.pack(side="bottom", pady=20)
    
    def create_menu_button(self, parent, text, command):
        btn = tk.Button(parent, text=text, font=("Arial", 12), 
                        bg="#34495e", fg="white", relief="flat", 
                        padx=10, pady=7, width=20, anchor="w", 
                        activebackground="#1abc9c", command=command)
        btn.pack(pady=5)
        return btn
    
    def show_book_search(self):
        # Xóa nội dung cũ trong frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Tạo tiêu đề
        lbl_title = tk.Label(self.content_frame, text="Tra cứu sách", font=("Arial", 16, "bold"), bg="#f8f9fa")
        lbl_title.pack(pady=10)
        
        # Frame tìm kiếm
        search_frame = tk.Frame(self.content_frame, bg="#f8f9fa")
        search_frame.pack(fill="x", padx=20, pady=10)
        
        lbl_search = tk.Label(search_frame, text="Từ khóa:", font=("Arial", 11), bg="#f8f9fa")
        lbl_search.pack(side="left", padx=5)
        
        self.search_entry = tk.Entry(search_frame, width=40, font=("Arial", 11))
        self.search_entry.pack(side="left", padx=5)
        
        search_btn = tk.Button(search_frame, text="Tìm kiếm", bg="#3498db", fg="white", 
                               font=("Arial", 10), width=10, command=self.search_books)
        search_btn.pack(side="left", padx=5)
        
        reset_btn = tk.Button(search_frame, text="Làm mới", bg="#95a5a6", fg="white", 
                              font=("Arial", 10), width=10, command=self.refresh_book_list)
        reset_btn.pack(side="left", padx=5)
        
        # Bảng hiển thị sách
        table_frame = tk.Frame(self.content_frame, bg="#f8f9fa")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Định nghĩa cột
        columns = ["Mã Sách", "Tên Sách", "Tác Giả", "Thể Loại", "Số Lượng", "Nhà Xuất Bản", "Tình Trạng"]
        self.book_list = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        
        # Thiết lập tiêu đề và độ rộng cột
        for col in columns:
            self.book_list.heading(col, text=col)
            if col in ["Mã Sách"]:
                self.book_list.column(col, width=80, anchor="center")
            elif col in ["Số Lượng", "Tác Giả"]:
                self.book_list.column(col, width=70, anchor="center")
            elif col in ["Thể Loại", "Tình Trạng"]:
                self.book_list.column(col, width=100, anchor="center")
            elif col in ["Tên Sách"]:
                self.book_list.column(col, width=200)
            else:
                self.book_list.column(col, width=150)
        
        # Tạo scrollbar
        y_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.book_list.yview)
        self.book_list.configure(yscrollcommand=y_scrollbar.set)
        
        self.book_list.pack(side="left", fill="both", expand=True)
        y_scrollbar.pack(side="right", fill="y")
        
        # Bind event double-click để xem chi tiết sách
        self.book_list.bind("<Double-1>", self.show_book_details)
        
        # Load danh sách sách ban đầu
        self.refresh_book_list()
    
    def refresh_book_list(self):
    # Xóa dữ liệu cũ trong bảng
        for item in self.book_list.get_children():
            self.book_list.delete(item)
    
    # Lấy danh sách sách
        books = self.book_manager.get_all_books()
        for book in books:
            self.book_list.insert("", "end", values=(
                book[0],         # MaSach
                book[2],         # TenSach
                book[3],         # TacGia
                book[4],         # TenTheLoai - Thay đổi từ book[9] thành book[4]
                book[5],         # SoLuong
                book[6],         # NhaXuatBan
                book[8]          # TinhTrang
            ))
    def search_books(self):
        search_term = self.search_entry.get().strip()
        if not search_term:
            self.refresh_book_list()
            return

        print(f"Đang tìm kiếm: {search_term}")

        for item in self.book_list.get_children():
            self.book_list.delete(item)

        books = self.book_manager.search_books(search_term)
        print(f"Kết quả tìm kiếm: {books}")

        if not books:
            no_results_label = tk.Label(self.content_frame, text="Không tìm thấy sách nào!", font=("Arial", 12),
                                        bg="#f8f9fa")
            no_results_label.pack(pady=10)
            return

        for book in books:
            self.book_list.insert("", "end", values=(
                book[0],  # MaSach
                book[2],  # TenSach
                book[3],  # TacGia
                book[4],  # TenTheLoai
                book[5],  # SoLuong
                book[6],  # NhaXuatBan
                book[8]  # TinhTrang (đúng chỉ số cho TinhTrang)
            ))
    
    def show_book_details(self, event):
        # Lấy sách được chọn
        selected_items = self.book_list.selection()
        if not selected_items:
            return
        
        selected_item = selected_items[0]
        values = self.book_list.item(selected_item, "values")
        ma_sach = values[0]
        
        # Lấy thông tin chi tiết từ cơ sở dữ liệu
        book = self.book_manager.get_book_by_id(ma_sach)
        if not book:
            return
        
        # Tạo cửa sổ chi tiết
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Chi tiết sách: {book[2]}")
        details_window.geometry("600x500")
        details_window.configure(bg="#f8f9fa")
        
        # Hiển thị thông tin
        frame = tk.Frame(details_window, bg="#f8f9fa", padx=20, pady=20)
        frame.pack(fill="both", expand=True)
        
        # Tiêu đề
        title_label = tk.Label(frame, text=book[2], font=("Arial", 16, "bold"), bg="#f8f9fa")
        title_label.pack(pady=(0, 20))
        
        # Thông tin sách
        info_frame = tk.Frame(frame, bg="#f8f9fa")
        info_frame.pack(fill="x", pady=10)
        
        # Tạo grid hiển thị thông tin
        labels = [
            ("Mã sách:", book[0]),
            ("Thể loại:", book[9]),
            ("Tác giả:", book[3]),
            ("Nhà xuất bản:", book[5]),
            ("Số lượng hiện có:", str(book[4])),
            ("Tình trạng:", book[7]),
            ("Giá trị:", f"{book[6]:,.0f} VND")
        ]
        
        for i, (label, value) in enumerate(labels):
            row = i // 2
            col = i % 2 * 2
            
            # Label
            label_widget = tk.Label(info_frame, text=label, font=("Arial", 11, "bold"), 
                                    bg="#f8f9fa", anchor="e")
            label_widget.grid(row=row, column=col, padx=10, pady=8, sticky="e")
            
            # Value
            value_widget = tk.Label(info_frame, text=value, font=("Arial", 11), 
                                    bg="#f8f9fa", anchor="w")
            value_widget.grid(row=row, column=col+1, padx=10, pady=8, sticky="w")
        
        # Nút đóng và đặt mượn
        button_frame = tk.Frame(frame, bg="#f8f9fa")
        button_frame.pack(pady=30)
        
        close_btn = tk.Button(button_frame, text="Đóng", font=("Arial", 11), 
                              width=10, command=details_window.destroy)
        close_btn.pack(side="left", padx=10)
        
        # Chỉ hiển thị nút "Đặt mượn" nếu còn sách
        if book[4] > 0:
            borrow_btn = tk.Button(button_frame, text="Đặt mượn", font=("Arial", 11), 
                                   bg="#3498db", fg="white", width=10,
                                   command=lambda: self.request_borrow(book))
            borrow_btn.pack(side="left", padx=10)
    
    def request_borrow(self, book):
        # Chức năng này sẽ gửi yêu cầu mượn sách
        # Trong phiên bản đơn giản này, chỉ hiển thị thông báo
        messagebox.showinfo("Thông báo", 
                           f"Đã gửi yêu cầu mượn sách '{book[2]}'\n"
                           f"Vui lòng đến thư viện để hoàn tất thủ tục mượn sách.")
    
    def show_current_borrows(self):
        # Xóa nội dung cũ trong frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Tạo tiêu đề
        lbl_title = tk.Label(self.content_frame, text="Sách đang mượn", font=("Arial", 16, "bold"), bg="#f8f9fa")
        lbl_title.pack(pady=10)
        
        # Bảng hiển thị sách đang mượn
        table_frame = tk.Frame(self.content_frame, bg="#f8f9fa")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Định nghĩa cột
        columns = ["Mã Phiếu", "Mã Sách", "Tên Sách", "Ngày Mượn", "Ngày Hẹn Trả", "Số Lượng", "Còn Lại"]
        self.borrow_list = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        
        # Thiết lập tiêu đề và độ rộng cột
        for col in columns:
            self.borrow_list.heading(col, text=col)
            if col in ["Mã Phiếu", "Mã Sách", "Số Lượng", "Còn Lại"]:
                self.borrow_list.column(col, width=80, anchor="center")
            elif col in ["Ngày Mượn", "Ngày Hẹn Trả"]:
                self.borrow_list.column(col, width=120, anchor="center")
            else:
                self.borrow_list.column(col, width=250)
        
        # Tạo scrollbar
        y_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.borrow_list.yview)
        self.borrow_list.configure(yscrollcommand=y_scrollbar.set)
        
        self.borrow_list.pack(side="left", fill="both", expand=True)
        y_scrollbar.pack(side="right", fill="y")
        
        # Load dữ liệu
        self.load_current_borrows()
        
        # Thêm nút làm mới
        refresh_btn = tk.Button(self.content_frame, text="Làm mới", bg="#3498db", fg="white", 
                               font=("Arial", 10), width=10, command=self.load_current_borrows)
        refresh_btn.pack(pady=10)
    
    def load_current_borrows(self):
        # Xóa dữ liệu cũ trong bảng
        for item in self.borrow_list.get_children():
            self.borrow_list.delete(item)
        
        # Lấy danh sách sách đang mượn
        active_borrows = self.return_manager.get_active_borrows(self.user_data[0])
        
        today = datetime.now().date()
        
        for borrow in active_borrows:
            # Kiểm tra nếu quá hạn
            due_date = datetime.strptime(borrow[4], "%Y-%m-%d").date()
            is_overdue = due_date < today
            
            tag = "overdue" if is_overdue else ""
            
            self.borrow_list.insert("", "end", values=(
                borrow[0],        # MaPhieuMuon
                borrow[5],        # MaSach
                borrow[6],        # TenSach
                borrow[3],        # NgayMuon
                borrow[4],        # NgayHenTra
                borrow[7],        # SoLuong
                borrow[9]         # ConLai (SoLuong - DaTra)
            ), tags=(tag,))
        
        # Thêm style cho các mục quá hạn
        self.borrow_list.tag_configure("overdue", background="#ffcccc")
    
    def show_borrow_history(self):
        # Xóa nội dung cũ trong frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Tạo tiêu đề
        lbl_title = tk.Label(self.content_frame, text="Lịch sử mượn trả", font=("Arial", 16, "bold"), bg="#f8f9fa")
        lbl_title.pack(pady=10)
        
        # Tạo notebook với tabs
        tab_control = ttk.Notebook(self.content_frame)
        borrow_tab = ttk.Frame(tab_control)
        return_tab = ttk.Frame(tab_control)
        
        tab_control.add(borrow_tab, text='Phiếu mượn')
        tab_control.add(return_tab, text='Phiếu trả')
        tab_control.pack(expand=1, fill='both', padx=10, pady=5)
        
        # === TAB PHIẾU MƯỢN ===
        borrow_frame = tk.Frame(borrow_tab, bg="#f8f9fa")
        borrow_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Bảng hiển thị phiếu mượn
        columns = ["Mã Phiếu", "Tên Sách", "Tác Giả", "Số Lượng", "Ngày Mượn", "Ngày Hẹn Trả", "Trạng Thái"]
        self.borrow_history_list = ttk.Treeview(borrow_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.borrow_history_list.heading(col, text=col)
            if col == "Mã Phiếu":
                self.borrow_history_list.column(col, width=80, anchor="center")
            elif col in ["Ngày Mượn", "Ngày Hẹn Trả"]:
                self.borrow_history_list.column(col, width=120, anchor="center")
            else:
                self.borrow_history_list.column(col, width=100, anchor="center")
        
        # Scrollbar cho bảng phiếu mượn
        y_scrollbar = ttk.Scrollbar(borrow_frame, orient="vertical", command=self.borrow_history_list.yview)
        self.borrow_history_list.configure(yscrollcommand=y_scrollbar.set)
        
        self.borrow_history_list.pack(side="left", fill="both", expand=True)
        y_scrollbar.pack(side="right", fill="y")
        
        # Bind event double-click để xem chi tiết phiếu mượn
        self.borrow_history_list.bind("<Double-1>", self.show_borrow_details)
        
        # === TAB PHIẾU TRẢ ===
        return_frame = tk.Frame(return_tab, bg="#f8f9fa")
        return_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Bảng hiển thị phiếu trả
        columns = ["Mã Phiếu Trả", "Mã Phiếu Mượn", "Ngày Trả", "Quá Hạn"]
        self.return_history_list = ttk.Treeview(return_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.return_history_list.heading(col, text=col)
            if col in ["Mã Phiếu Trả", "Mã Phiếu Mượn"]:
                self.return_history_list.column(col, width=100, anchor="center")
            elif col == "Ngày Trả":
                self.return_history_list.column(col, width=120, anchor="center")
            else:
                self.return_history_list.column(col, width=100, anchor="center")
        
        # Scrollbar cho bảng phiếu trả
        y_scrollbar = ttk.Scrollbar(return_frame, orient="vertical", command=self.return_history_list.yview)
        self.return_history_list.configure(yscrollcommand=y_scrollbar.set)
        
        self.return_history_list.pack(side="left", fill="both", expand=True)
        y_scrollbar.pack(side="right", fill="y")
        
        # Bind event double-click để xem chi tiết phiếu trả
        self.return_history_list.bind("<Double-1>", self.show_return_details)
        self.load_borrow_history()
    
    def load_borrow_history(self):
        # Xóa dữ liệu cũ trong bảng
        for item in self.borrow_history_list.get_children():
            self.borrow_history_list.delete(item)
        
        for item in self.return_history_list.get_children():
            self.return_history_list.delete(item)
        
        # Lấy danh sách phiếu mượn
        borrow_history = self.borrow_manager.get_borrow_slips(self.user_data[0])
        for borrow in borrow_history:
            self.borrow_history_list.insert("", "end", values=(
                borrow[0],        # MaPhieuMuon
                borrow[2],        # TenSach
                borrow[3],        # TacGia
                borrow[4],        # SoLuong
                borrow[5],        # NgayMuon
                borrow[6],
                borrow[7]
            ))
        
        return_history = self.get_user_return_history()
        for ret in return_history:
            days_overdue = ret[7] if ret[7] and ret[7] > 0 else 0
            self.return_history_list.insert("", "end", values=(
                ret[0],        # MaPhieuTra
                ret[1],        # MaPhieuMuon
                ret[2],        # NgayTra
                f"{days_overdue:.0f} ngày" if days_overdue > 0 else "0 ngày"  # DaysOverdue
            ))
    
    def get_user_return_history(self):
        # Phương thức này lấy lịch sử trả sách của người dùng hiện tại
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                SELECT r.MaPhieuTra, r.MaPhieuMuon, r.NgayTra, 
                       p.MaDocGia, u.HoVaTen,
                       p.NgayMuon, p.NgayHenTra,
                       JULIANDAY(r.NgayTra) - JULIANDAY(p.NgayHenTra) as DaysOverdue
                FROM PhieuTra r
                JOIN PhieuMuon p ON r.MaPhieuMuon = p.MaPhieuMuon
                JOIN NguoiDung u ON p.MaDocGia = u.MaDocGia
                WHERE p.MaDocGia = ?
                ORDER BY r.NgayTra DESC
            """, (self.user_data[0],))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving user return history: {e}")
            return []
    
    def show_borrow_details(self, event):
        # Hiển thị chi tiết phiếu mượn khi double-click
        selected_items = self.borrow_history_list.selection()
        if not selected_items:
            return
        
        selected_item = selected_items[0]
        values = self.borrow_history_list.item(selected_item, "values")
        ma_phieu_muon = values[0]
        
        # Tạo cửa sổ hiển thị chi tiết
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Chi tiết phiếu mượn #{ma_phieu_muon}")
        details_window.geometry("700x500")
        details_window.configure(bg="#f8f9fa")
        
        # Lấy thông tin chi tiết phiếu mượn
        details = self.borrow_manager.get_borrow_details(ma_phieu_muon)
        
        # Hiển thị thông tin
        header_frame = tk.Frame(details_window, bg="#f8f9fa")
        header_frame.pack(pady=10, fill="x", padx=20)
        
        lbl_title = tk.Label(header_frame, text=f"Chi tiết phiếu mượn #{ma_phieu_muon}", 
                            font=("Arial", 14, "bold"), bg="#f8f9fa")
        lbl_title.pack(side="left", pady=10)
        
        date_frame = tk.Frame(details_window, bg="#f8f9fa")
        date_frame.pack(fill="x", padx=20)
        
        borrow_date = tk.Label(date_frame, text=f"Ngày mượn: {values[1]}", 
                              font=("Arial", 10), bg="#f8f9fa")
        borrow_date.pack(side="left", padx=5)
        
        return_date = tk.Label(date_frame, text=f"Ngày hẹn trả: {values[2]}", 
                              font=("Arial", 10), bg="#f8f9fa")
        return_date.pack(side="left", padx=20)
        
        status = tk.Label(date_frame, text=f"Trạng thái: {values[3]}", 
                         font=("Arial", 10), bg="#f8f9fa")
        status.pack(side="left", padx=5)
        
        # Bảng chi tiết
        columns = ["Mã Chi Tiết", "Mã Sách", "Tên Sách", "Số Lượng", "Đã Trả", "Còn Lại"]
        detail_list = ttk.Treeview(details_window, columns=columns, show="headings", height=15)
        
        for col in columns:
            detail_list.heading(col, text=col)
            if col in ["Mã Chi Tiết", "Mã Sách", "Số Lượng", "Đã Trả", "Còn Lại"]:
                detail_list.column(col, width=80, anchor="center")
            else:
                detail_list.column(col, width=250)
        
        # Thêm dữ liệu vào bảng
        for detail in details:
            remaining = detail[3] - detail[4]  # SoLuong - DaTra
            detail_list.insert("", "end", values=(
                detail[0],        # MaChiTiet
                detail[2],        # MaSach
                detail[5],        # TenSach (from JOIN)
                detail[3],        # SoLuong
                detail[4],        # DaTra
                remaining         # ConLai
            ))
        
        # Thêm scrollbar
        detail_frame = tk.Frame(details_window)
        detail_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        detail_y_scrollbar = ttk.Scrollbar(detail_frame, orient="vertical", command=detail_list.yview)
        detail_list.configure(yscrollcommand=detail_y_scrollbar.set)
        
        detail_list.pack(side="left", fill="both", expand=True)
        detail_y_scrollbar.pack(side="right", fill="y")
        
        # Nút đóng
        btn_close = tk.Button(details_window, text="Đóng", command=details_window.destroy, 
                           bg="#3498db", fg="white", font=("Arial", 10), width=10)
        btn_close.pack(pady=15)
    
    def show_return_details(self, event):
        # Hiển thị chi tiết phiếu trả khi double-click
        selected_items = self.return_history_list.selection()
        if not selected_items:
            return
        
        selected_item = selected_items[0]
        values = self.return_history_list.item(selected_item, "values")
        ma_phieu_tra = values[0]
        
        # Tạo cửa sổ hiển thị chi tiết
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Chi tiết phiếu trả #{ma_phieu_tra}")
        details_window.geometry("700x500")
        details_window.configure(bg="#f8f9fa")
        
        # Lấy thông tin chi tiết phiếu trả
        details = self.return_manager.get_return_details(ma_phieu_tra)
        
        # Hiển thị thông tin
        header_frame = tk.Frame(details_window, bg="#f8f9fa")
        header_frame.pack(pady=10, fill="x", padx=20)
        
        lbl_title = tk.Label(header_frame, text=f"Chi tiết phiếu trả #{ma_phieu_tra}", 
                            font=("Arial", 14, "bold"), bg="#f8f9fa")
        lbl_title.pack(side="left", pady=10)
        
        borrow_info = tk.Label(header_frame, text=f"Phiếu mượn: #{values[1]}", 
                              font=("Arial", 10), bg="#f8f9fa")
        borrow_info.pack(side="right", pady=10)
        
        date_frame = tk.Frame(details_window, bg="#f8f9fa")
        date_frame.pack(fill="x", padx=20)
        
        return_date = tk.Label(date_frame, text=f"Ngày trả: {values[2]}", 
                              font=("Arial", 10), bg="#f8f9fa")
        return_date.pack(side="left", padx=5)
        
        # Bảng chi tiết
        columns = ["Mã Chi Tiết", "Mã Sách", "Tên Sách", "Số Lượng", "Tình Trạng"]
        detail_list = ttk.Treeview(details_window, columns=columns, show="headings", height=15)
        
        for col in columns:
            detail_list.heading(col, text=col)
            if col in ["Mã Chi Tiết", "Mã Sách", "Số Lượng"]:
                detail_list.column(col, width=80, anchor="center")
            elif col == "Tình Trạng":
                detail_list.column(col, width=120)
            else:
                detail_list.column(col, width=250)
        
        # Thêm dữ liệu vào bảng
        for detail in details:
            detail_list.insert("", "end", values=(
                detail[0],        # MaChiTietTra
                detail[2],        # MaSach
                detail[5],        # TenSach (from JOIN)
                detail[3],        # SoLuong
                detail[4]         # TinhTrangSach
            ))
        
        # Thêm scrollbar
        detail_frame = tk.Frame(details_window)
        detail_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        detail_y_scrollbar = ttk.Scrollbar(detail_frame, orient="vertical", command=detail_list.yview)
        detail_list.configure(yscrollcommand=detail_y_scrollbar.set)
        
        detail_list.pack(side="left", fill="both", expand=True)
        detail_y_scrollbar.pack(side="right", fill="y")
        
        # Nút đóng
        btn_close = tk.Button(details_window, text="Đóng", command=details_window.destroy, 
                           bg="#3498db", fg="white", font=("Arial", 10), width=10)
        btn_close.pack(pady=15)
    
    def show_profile(self):
        # Xóa nội dung cũ trong frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Tạo tiêu đề
        lbl_title = tk.Label(self.content_frame, text="Thông tin cá nhân", font=("Arial", 16, "bold"), bg="#f8f9fa")
        lbl_title.pack(pady=10)
        
        # Frame thông tin
        info_frame = tk.Frame(self.content_frame, bg="#f8f9fa", padx=50, pady=20)
        info_frame.pack(fill="x")
        
        # Thông tin người dùng
        fields = [
            ("Mã độc giả:", self.user_data[0]),
            ("Họ và tên:", self.user_data[1]),
            ("Giới tính:", self.user_data[2]),
            ("Ngày sinh:", self.user_data[3]),
            ("Điện thoại:", self.user_data[4]),
            ("Phân quyền:", self.user_data[6])
        ]
        
        for i, (label, value) in enumerate(fields):
            label_widget = tk.Label(info_frame, text=label, font=("Arial", 12, "bold"), 
                                   bg="#f8f9fa", anchor="e", width=15)
            label_widget.grid(row=i, column=0, padx=10, pady=12, sticky="e")
            
            value_widget = tk.Label(info_frame, text=value, font=("Arial", 12), 
                                   bg="#f8f9fa", anchor="w")
            value_widget.grid(row=i, column=1, padx=10, pady=12, sticky="w")
        
        # Frame đổi mật khẩu
        password_frame = tk.LabelFrame(self.content_frame, text="Đổi mật khẩu", 
                                      font=("Arial", 12, "bold"), bg="#f8f9fa", padx=20, pady=20)
        password_frame.pack(fill="x", padx=50, pady=20)
        
        # Field mật khẩu hiện tại
        current_pwd_frame = tk.Frame(password_frame, bg="#f8f9fa")
        current_pwd_frame.pack(fill="x", pady=5)
        
        current_pwd_label = tk.Label(current_pwd_frame, text="Mật khẩu hiện tại:", 
                                    font=("Arial", 11), bg="#f8f9fa", width=15)
        current_pwd_label.pack(side="left", padx=5)
        
        self.current_pwd_entry = tk.Entry(current_pwd_frame, show="•", width=30)
        self.current_pwd_entry.pack(side="left", padx=5)
        
        # Field mật khẩu mới
        new_pwd_frame = tk.Frame(password_frame, bg="#f8f9fa")
        new_pwd_frame.pack(fill="x", pady=5)
        
        new_pwd_label = tk.Label(new_pwd_frame, text="Mật khẩu mới:", 
                               font=("Arial", 11), bg="#f8f9fa", width=15)
        new_pwd_label.pack(side="left", padx=5)
        
        self.new_pwd_entry = tk.Entry(new_pwd_frame, show="•", width=30)
        self.new_pwd_entry.pack(side="left", padx=5)
        
        # Field xác nhận mật khẩu
        confirm_pwd_frame = tk.Frame(password_frame, bg="#f8f9fa")
        confirm_pwd_frame.pack(fill="x", pady=5)
        
        confirm_pwd_label = tk.Label(confirm_pwd_frame, text="Xác nhận mật khẩu:", 
                                   font=("Arial", 11), bg="#f8f9fa", width=15)
        confirm_pwd_label.pack(side="left", padx=5)
        
        self.confirm_pwd_entry = tk.Entry(confirm_pwd_frame, show="•", width=30)
        self.confirm_pwd_entry.pack(side="left", padx=5)
        
        # Nút đổi mật khẩu
        btn_frame = tk.Frame(password_frame, bg="#f8f9fa")
        btn_frame.pack(pady=15)
        
        change_pwd_btn = tk.Button(btn_frame, text="Đổi mật khẩu", bg="#3498db", fg="white", 
                                 font=("Arial", 11), width=15, command=self.change_password)
        change_pwd_btn.pack()
    
    def change_password(self):
        # Lấy dữ liệu từ form
        current_pwd = self.current_pwd_entry.get()
        new_pwd = self.new_pwd_entry.get()
        confirm_pwd = self.confirm_pwd_entry.get()
        
        # Kiểm tra dữ liệu
        if not current_pwd or not new_pwd or not confirm_pwd:
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin!")
            return
        
        if new_pwd != confirm_pwd:
            messagebox.showwarning("Cảnh báo", "Mật khẩu mới và xác nhận mật khẩu không khớp!")
            return
        
        # Kiểm tra mật khẩu hiện tại
        if current_pwd != self.user_data[5]:
            messagebox.showwarning("Cảnh báo", "Mật khẩu hiện tại không đúng!")
            return
        
        # Cập nhật mật khẩu
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                UPDATE NguoiDung
                SET MatKhau = ?
                WHERE MaDocGia = ?
            """, (new_pwd, self.user_data[0]))
            self.db.conn.commit()
            
            # Cập nhật thông tin người dùng hiện tại
            self.user_data = list(self.user_data)
            self.user_data[5] = new_pwd
            self.user_data = tuple(self.user_data)
            
            # Xóa dữ liệu trong form
            self.current_pwd_entry.delete(0, tk.END)
            self.new_pwd_entry.delete(0, tk.END)
            self.confirm_pwd_entry.delete(0, tk.END)
            
            messagebox.showinfo("Thành công", "Đổi mật khẩu thành công!")
        except sqlite3.Error as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")

    def logout(self):
        if messagebox.askyesno("Đăng xuất", "Bạn có chắc chắn muốn đăng xuất?"):
            self.root.destroy()
        import os
        import sys
        os.execl(sys.executable, sys.executable, *sys.argv)