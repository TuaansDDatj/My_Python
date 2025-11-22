import sqlite3
from datetime import datetime

class ReportManager:
    def __init__(self, db):
        self.db = db
    
    def get_book_statistics(self):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) as TotalBooks, 
                       SUM(SoLuong) as TotalCopies, 
                       SUM(GiaTri * SoLuong) as TotalValue
                FROM Sach
            """)
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error getting book statistics: {e}")
            return None
    
    def get_user_statistics(self):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                SELECT PhanQuyen, COUNT(*) as Total
                FROM NguoiDung
                GROUP BY PhanQuyen
            """)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting user statistics: {e}")
            return []
    
    def get_borrow_statistics(self, start_date=None, end_date=None):
        try:
            cursor = self.db.conn.cursor()
            if start_date and end_date:
                cursor.execute("""
                    SELECT COUNT(*) as TotalBorrows, 
                           COUNT(DISTINCT MaDocGia) as TotalUsers,
                           SUM(
                               (SELECT SUM(SoLuong) 
                                FROM ChiTietPhieuMuon 
                                WHERE MaPhieuMuon = PhieuMuon.MaPhieuMuon)
                           ) as TotalBooks
                    FROM PhieuMuon
                    WHERE NgayMuon BETWEEN ? AND ?
                """, (start_date, end_date))
            else:
                cursor.execute("""
                    SELECT COUNT(*) as TotalBorrows, 
                           COUNT(DISTINCT MaDocGia) as TotalUsers,
                           SUM(
                               (SELECT SUM(SoLuong) 
                                FROM ChiTietPhieuMuon 
                                WHERE MaPhieuMuon = PhieuMuon.MaPhieuMuon)
                           ) as TotalBooks
                    FROM PhieuMuon
                """)
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error getting borrow statistics: {e}")
            return None
    
    def get_popular_books(self, limit=10):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                SELECT s.MaSach, s.TenSach, s.TacGia, t.TenTheLoai, SUM(c.SoLuong) as TimesIssued
                FROM ChiTietPhieuMuon c
                JOIN Sach s ON c.MaSach = s.MaSach
                JOIN TheLoai t ON s.MaTheLoai = t.MaTheLoai
                GROUP BY s.MaSach
                ORDER BY TimesIssued DESC
                LIMIT ?
            """, (limit,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting popular books: {e}")
            return []
    
    def get_overdue_books(self):
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            cursor = self.db.conn.cursor()
            cursor.execute("""
                SELECT p.MaPhieuMuon, p.MaDocGia, u.HoVaTen, p.NgayMuon, p.NgayHenTra,
                       c.MaSach, s.TenSach, c.SoLuong, c.DaTra,
                       ROUND(JULIANDAY(?) - JULIANDAY(p.NgayHenTra)) as DaysOverdue
                FROM PhieuMuon p
                JOIN ChiTietPhieuMuon c ON p.MaPhieuMuon = c.MaPhieuMuon
                JOIN Sach s ON c.MaSach = s.MaSach
                JOIN NguoiDung u ON p.MaDocGia = u.MaDocGia
                WHERE p.TrangThai = 'Đang mượn' 
                  AND c.SoLuong > c.DaTra
                  AND p.NgayHenTra < ?
                ORDER BY DaysOverdue DESC
            """, (today, today))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting overdue books: {e}")
            return []
            
    def get_monthly_statistics(self, year):
        try:
            cursor = self.db.conn.cursor()
            months = []
            borrows = []
            returns = []
            
            for month in range(1, 13):
                month_name = datetime(year, month, 1).strftime("%B")
                start_date = f"{year}-{month:02d}-01"
                
                if month == 12:
                    end_date = f"{year+1}-01-01"
                else:
                    end_date = f"{year}-{month+1:02d}-01"
                
                # Get borrow count
                cursor.execute("""
                    SELECT COUNT(*) FROM PhieuMuon 
                    WHERE NgayMuon >= ? AND NgayMuon < ?
                """, (start_date, end_date))
                borrow_count = cursor.fetchone()[0]
                
                # Get return count
                cursor.execute("""
                    SELECT COUNT(*) FROM PhieuTra 
                    WHERE NgayTra >= ? AND NgayTra < ?
                """, (start_date, end_date))
                return_count = cursor.fetchone()[0]
                
                months.append(month_name)
                borrows.append(borrow_count)
                returns.append(return_count)
            
            return months, borrows, returns
        except sqlite3.Error as e:
            print(f"Error getting monthly statistics: {e}")
            return [], [], []