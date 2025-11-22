import sqlite3

class UserManager:
    def __init__(self, db):
        self.db = db
    
    def add_user(self, ma_doc_gia, ho_ten, gioi_tinh, ngay_sinh, dien_thoai, mat_khau, phan_quyen):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                INSERT INTO NguoiDung (MaDocGia, HoVaTen, GioiTinh, NgaySinh, DienThoai, MatKhau, PhanQuyen)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (ma_doc_gia, ho_ten, gioi_tinh, ngay_sinh, dien_thoai, mat_khau, phan_quyen))
            self.db.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding user: {e}")
            return False
    
    def update_user(self, ma_doc_gia, ho_ten, gioi_tinh, ngay_sinh, dien_thoai, mat_khau, phan_quyen):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                UPDATE NguoiDung
                SET HoVaTen = ?, GioiTinh = ?, NgaySinh = ?, DienThoai = ?, MatKhau = ?, PhanQuyen = ?
                WHERE MaDocGia = ?
            """, (ho_ten, gioi_tinh, ngay_sinh, dien_thoai, mat_khau, phan_quyen, ma_doc_gia))
            self.db.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating user: {e}")
            return False
    
    def delete_user(self, ma_doc_gia):
        try:
            cursor = self.db.conn.cursor()
            # Check if user has active borrows
            cursor.execute("""
                SELECT COUNT(*) FROM PhieuMuon
                WHERE MaDocGia = ? AND TrangThai = 'Đang mượn'
            """, (ma_doc_gia,))
            
            if cursor.fetchone()[0] > 0:
                return False  # User has active borrows
                
            cursor.execute("DELETE FROM NguoiDung WHERE MaDocGia = ?", (ma_doc_gia,))
            self.db.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting user: {e}")
            return False
    
    def search_users(self, search_term):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                SELECT * FROM NguoiDung
                WHERE MaDocGia LIKE ? OR HoVaTen LIKE ? OR DienThoai LIKE ?
            """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error searching users: {e}")
            return []
    
    def get_all_users(self):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("SELECT * FROM NguoiDung ORDER BY HoVaTen")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving users: {e}")
            return []
    
    def get_user_by_id(self, ma_doc_gia):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("SELECT * FROM NguoiDung WHERE MaDocGia = ?", (ma_doc_gia,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error retrieving user: {e}")
            return None
    
    def verify_login(self, ma_doc_gia, mat_khau):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("SELECT * FROM NguoiDung WHERE MaDocGia = ? AND MatKhau = ?", (ma_doc_gia, mat_khau))
            user = cursor.fetchone()
            return user
        except sqlite3.Error as e:
            print(f"Error verifying login: {e}")
            return None