import sqlite3
from datetime import datetime

class ReturnManager:
    def __init__(self, db):
        self.db = db
    
    def create_return_slip(self, ma_phieu_muon, ngay_tra, ghi_chu=""):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                INSERT INTO PhieuTra (MaPhieuMuon, NgayTra, GhiChu)
                VALUES (?, ?, ?)
            """, (ma_phieu_muon, ngay_tra, ghi_chu))
            self.db.conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error creating return slip: {e}")
            return None
    
    def add_return_detail(self, ma_phieu_tra, ma_sach, so_luong, tinh_trang_sach):
        try:
            cursor = self.db.conn.cursor()
            
            cursor.execute("""
                INSERT INTO ChiTietPhieuTra (MaPhieuTra, MaSach, SoLuong, TinhTrangSach)
                VALUES (?, ?, ?, ?)
            """, (ma_phieu_tra, ma_sach, so_luong, tinh_trang_sach))
            
            cursor.execute("""
                UPDATE Sach
                SET SoLuong = SoLuong + ?
                WHERE MaSach = ?
            """, (so_luong, ma_sach))
            
            cursor.execute("""
                SELECT MaPhieuMuon FROM PhieuTra WHERE MaPhieuTra = ?
            """, (ma_phieu_tra,))
            ma_phieu_muon = cursor.fetchone()[0]
            
            cursor.execute("""
                UPDATE ChiTietPhieuMuon
                SET DaTra = DaTra + ?
                WHERE MaPhieuMuon = ? AND MaSach = ?
            """, (so_luong, ma_phieu_muon, ma_sach))
            
            cursor.execute("""
                SELECT SUM(SoLuong), SUM(DaTra) 
                FROM ChiTietPhieuMuon 
                WHERE MaPhieuMuon = ?
            """, (ma_phieu_muon,))
            
            total_borrowed, total_returned = cursor.fetchone()
            
            if total_borrowed == total_returned:
                cursor.execute("""
                    UPDATE PhieuMuon
                    SET TrangThai = 'Đã trả'
                    WHERE MaPhieuMuon = ?
                """, (ma_phieu_muon,))
            
            self.db.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding return detail: {e}")
            return False
    
    def get_active_borrows(self, ma_doc_gia=None):
        try:
            cursor = self.db.conn.cursor()
            if ma_doc_gia:
                cursor.execute("""
                    SELECT p.MaPhieuMuon, p.MaDocGia, u.HoVaTen, p.NgayMuon, p.NgayHenTra, 
                           c.MaSach, s.TenSach, c.SoLuong, c.DaTra, (c.SoLuong - c.DaTra) AS ConLai
                    FROM PhieuMuon p
                    JOIN ChiTietPhieuMuon c ON p.MaPhieuMuon = c.MaPhieuMuon
                    JOIN Sach s ON c.MaSach = s.MaSach
                    JOIN NguoiDung u ON p.MaDocGia = u.MaDocGia
                    WHERE p.TrangThai = 'Đang mượn' AND p.MaDocGia = ? AND c.SoLuong > c.DaTra
                    ORDER BY p.NgayHenTra ASC
                """, (ma_doc_gia,))
            else:
                cursor.execute("""
                    SELECT p.MaPhieuMuon, p.MaDocGia, u.HoVaTen, p.NgayMuon, p.NgayHenTra, 
                           c.MaSach, s.TenSach, c.SoLuong, c.DaTra, (c.SoLuong - c.DaTra) AS ConLai
                    FROM PhieuMuon p
                    JOIN ChiTietPhieuMuon c ON p.MaPhieuMuon = c.MaPhieuMuon
                    JOIN Sach s ON c.MaSach = s.MaSach
                    JOIN NguoiDung u ON p.MaDocGia = u.MaDocGia
                    WHERE p.TrangThai = 'Đang mượn' AND c.SoLuong > c.DaTra
                    ORDER BY p.NgayHenTra ASC
                """)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving active borrows: {e}")
            return []
            
    def get_return_history(self):
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
                ORDER BY r.NgayTra DESC
            """)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving return history: {e}")
            return []
            
    def get_return_details(self, ma_phieu_tra):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                SELECT c.*, s.TenSach
                FROM ChiTietPhieuTra c
                JOIN Sach s ON c.MaSach = s.MaSach
                WHERE c.MaPhieuTra = ?
            """, (ma_phieu_tra,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving return details: {e}")
            return []
    
    def get_user_return_history(self, ma_doc_gia):
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
            """, (ma_doc_gia,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving user return history: {e}")
            return []