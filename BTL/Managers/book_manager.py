import sqlite3

class BookManager:
    def __init__(self, db):
        self.db = db
    
    def add_book(self, ma_sach, ma_the_loai, ten_sach, tac_gia, so_luong, nha_xuat_ban, gia_tri, tinh_trang):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                INSERT INTO Sach (MaSach, MaTheLoai, TenSach, TacGia, SoLuong, NhaXuatBan, GiaTri, TinhTrang)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (ma_sach, ma_the_loai, ten_sach, tac_gia, so_luong, nha_xuat_ban, gia_tri, tinh_trang))
            self.db.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding book: {e}")
            return False
    
    def update_book(self, ma_sach, ma_the_loai, ten_sach, tac_gia, so_luong, nha_xuat_ban, gia_tri, tinh_trang):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                UPDATE Sach
                SET MaTheLoai = ?, TenSach = ?, TacGia = ?, SoLuong = ?, NhaXuatBan = ?, GiaTri = ?, TinhTrang = ?
                WHERE MaSach = ?
            """, (ma_the_loai, ten_sach, tac_gia, so_luong, nha_xuat_ban, gia_tri, tinh_trang, ma_sach))
            self.db.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating book: {e}")
            return False
    
    def delete_book(self, ma_sach):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM ChiTietPhieuMuon c
                JOIN PhieuMuon p ON c.MaPhieuMuon = p.MaPhieuMuon
                WHERE c.MaSach = ? AND p.TrangThai = 'Đang mượn' AND c.SoLuong > c.DaTra
            """, (ma_sach,))
            
            if cursor.fetchone()[0] > 0:
                return False  # Book is being borrowed
                
            cursor.execute("DELETE FROM Sach WHERE MaSach = ?", (ma_sach,))
            self.db.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting book: {e}")
            return False

    def search_books(self, search_term):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                SELECT s.MaSach, s.MaTheLoai, s.TenSach, s.TacGia, t.TenTheLoai, s.SoLuong, s.NhaXuatBan, s.GiaTri, s.TinhTrang
                FROM Sach s
                LEFT JOIN TheLoai t ON s.MaTheLoai = t.MaTheLoai
                WHERE s.MaSach LIKE ? OR s.TenSach LIKE ? OR s.TacGia LIKE ? OR t.TenTheLoai LIKE ?
            """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Lỗi khi tìm kiếm sách: {e}")
            return []

    def get_all_books(self):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                SELECT s.MaSach, s.MaTheLoai, s.TenSach, s.TacGia, t.TenTheLoai, s.SoLuong, s.NhaXuatBan, s.GiaTri, s.TinhTrang
                FROM Sach s
                LEFT JOIN TheLoai t ON s.MaTheLoai = t.MaTheLoai
            """)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving books: {e}")
            return []

    def get_book_by_id(self, ma_sach):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                SELECT s.MaSach, s.TenSach, s.TacGia, s.SoLuong, s.NhaXuatBan, s.GiaTri, s.TinhTrang, 
                       COALESCE(t.TenTheLoai, 'Không có thể loại')
                FROM Sach s
                LEFT JOIN TheLoai t ON s.MaTheLoai = t.MaTheLoai
                WHERE s.MaSach = ?
            """, (ma_sach,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error retrieving book: {e}")
            return None
    
    def get_all_categories(self):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("SELECT * FROM TheLoai ORDER BY TenTheLoai")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving categories: {e}")
            return []
            
    def add_category(self, ma_the_loai, ten_the_loai):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                INSERT INTO TheLoai (MaTheLoai, TenTheLoai)
                VALUES (?, ?)
            """, (ma_the_loai, ten_the_loai))
            self.db.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding category: {e}")
            return False


