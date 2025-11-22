import sqlite3

class BorrowManager:
    def __init__(self, db):
        self.db = db
    
    def create_borrow_slip(self, ma_doc_gia, ngay_muon, ngay_hen_tra):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                INSERT INTO PhieuMuon (MaDocGia, NgayMuon, NgayHenTra, TrangThai)
                VALUES (?, ?, ?, 'Đang mượn')
            """, (ma_doc_gia, ngay_muon, ngay_hen_tra))
            self.db.conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error creating borrow slip: {e}")
            return None
# đã sửa
    def add_borrow_detail(self, ma_phieu_muon, ma_sach, so_luong):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("SELECT SoLuong FROM Sach WHERE MaSach = ?", (ma_sach,))
            available = cursor.fetchone()

            # Kiểm tra xem sách có tồn tại không và số lượng yêu cầu có hợp lệ không
            if available is None:
                print(f"Không tìm thấy sách có mã {ma_sach}")
                return False

            available_quantity = available[0]

            # Đảm bảo số lượng mượn không vượt quá số lượng có sẵn
            if so_luong <= available_quantity:
                cursor.execute("""
                    INSERT INTO ChiTietPhieuMuon (MaPhieuMuon, MaSach, SoLuong, DaTra)
                    VALUES (?, ?, ?, 0)
                """, (ma_phieu_muon, ma_sach, so_luong))

                cursor.execute("""
                    UPDATE Sach
                    SET SoLuong = SoLuong - ?
                    WHERE MaSach = ?
                """, (so_luong, ma_sach))

                self.db.conn.commit()
                return True
            else:
                print(f"Số lượng yêu cầu ({so_luong}) vượt quá số lượng có sẵn ({available_quantity})")
                return False
        except sqlite3.Error as e:
            print(f"Lỗi khi thêm chi tiết phiếu mượn: {e}")
            self.db.conn.rollback()  # Hoàn tác các thay đổi khi có lỗi
            return False

    def check_book_availability(self, ma_sach, so_luong):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("SELECT SoLuong FROM Sach WHERE MaSach = ?", (ma_sach,))
            available = cursor.fetchone()

            if available is None:
                return False, "Không tìm thấy sách có mã này"

            available_quantity = available[0]

            if available_quantity <= 0:
                return False, "Sách này hiện đã hết"
            elif so_luong > available_quantity:
                return False, f"Số lượng sách không đủ. Hiện chỉ còn {available_quantity} cuốn"
            else:
                return True, "Có thể mượn sách"
        except sqlite3.Error as e:
            print(f"Lỗi khi kiểm tra số lượng sách: {e}")
            return False, f"Lỗi hệ thống: {str(e)}"

    def get_borrow_slips(self, ma_doc_gia=None):
        try:
            cursor = self.db.conn.cursor()
            if ma_doc_gia:
                cursor.execute("""
                    SELECT p.MaPhieuMuon, p.MaDocGia, i.TenSach, i.TacGia, i.SoLuong, p.NgayMuon, p.NgayHenTra, p.TrangThai
                    FROM PhieuMuon p
                    JOIN ChiTietPhieuMuon u ON p.MaPhieuMuon = u.MaPhieuMuon
                    JOIN Sach i ON u.MaSach = i.MaSach
                    WHERE p.MaPhieuMuon LIKE ? OR p.MaDocGia LIKE ? OR u.MaSach LIKE ?
                    ORDER BY p.NgayMuon DESC
                """, (f"%{ma_doc_gia}%", f"%{ma_doc_gia}%", f"%{ma_doc_gia}%"))
            else:
                cursor.execute("""
                    SELECT p.*, u.HoVaTen
                    FROM PhieuMuon p
                    JOIN NguoiDung u ON p.MaDocGia = u.MaDocGia
                    ORDER BY p.NgayMuon DESC
                """)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving borrow slips: {e}")
            return []
        
    def get_borrow_by_id(self, ma_phieu_muon):
        query = """
        SELECT pm.MaPhieuMuon, pm.MaDocGia, pm.NgayMuon, pm.NgayHenTra, pm.TrangThai, nd.HoVaTen
        FROM PhieuMuon pm
        JOIN NguoiDung nd ON pm.MaDocGia = nd.MaDocGia
        WHERE pm.MaPhieuMuon = ?
        """
        cursor = self.db.conn.cursor()
        cursor.execute(query, (ma_phieu_muon,))
        return cursor.fetchone()
    
    def get_borrow_details(self, ma_phieu_muon):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                SELECT c.*, s.TenSach
                FROM ChiTietPhieuMuon c
                JOIN Sach s ON c.MaSach = s.MaSach
                WHERE c.MaPhieuMuon = ?
            """, (ma_phieu_muon,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving borrow details: {e}")
            return []
    
    def search_borrow_slips(self, search_term):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                SELECT p.*, u.HoVaTen
                FROM PhieuMuon p
                JOIN NguoiDung u ON p.MaDocGia = u.MaDocGia
                WHERE p.MaPhieuMuon LIKE ? OR p.MaDocGia LIKE ? OR u.HoVaTen LIKE ?
                ORDER BY p.NgayMuon DESC
            """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error searching borrow slips: {e}")
            return []

    def delete_borrow_slip(self, ma_phieu_muon):
        try:
            query_delete_details = "DELETE FROM CHITIETPHIEUMUON WHERE MaPhieuMuon = ?"
            self.db.execute_query(query_delete_details, (ma_phieu_muon,))
            query_delete_slip = "DELETE FROM PHIEUMUON WHERE MaPhieuMuon = ?"
            self.db.execute_query(query_delete_slip, (ma_phieu_muon,))
            return True
        except Exception as e:
            print(f"Lỗi khi xóa phiếu mượn: {str(e)}")
            return False

    # Thêm phương thức này vào class BorrowManager
    def get_borrow_info(self, ma_phieu_muon):
        """Lấy thông tin cơ bản của phiếu mượn"""
        try:
            query = """
            SELECT MaPhieuMuon, MaDocGia, NgayMuon, NgayHenTra, TrangThai
            FROM PhieuMuon
            WHERE MaPhieuMuon = ?
            """
            self.cursor.execute(query, (ma_phieu_muon,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Lỗi khi lấy thông tin phiếu mượn: {str(e)}")
            return None