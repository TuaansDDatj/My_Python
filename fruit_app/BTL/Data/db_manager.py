import sqlite3
import os

class Database:
    def __init__(self, db_file=os.path.join(os.path.dirname(__file__), "..", "Data", "library1.db")):
        self.db_file = db_file
        self.conn = None
        self.create_connection()
        self.create_tables()
    
    def create_connection(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.conn.execute("PRAGMA foreign_keys = ON")
            return True
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return False
    
    def create_tables(self):
        try:
            cursor = self.conn.cursor()
            
            cursor.executescript("""
                -- Bảng Thể Loại Sách
                CREATE TABLE IF NOT EXISTS TheLoai (
                    MaTheLoai TEXT PRIMARY KEY,
                    TenTheLoai TEXT NULL
                );
                
                -- Bảng Sách
                CREATE TABLE IF NOT EXISTS Sach (
                    MaSach TEXT PRIMARY KEY,
                    MaTheLoai TEXT NULL,
                    TenSach TEXT NULL,
                    TacGia TEXT NULL,
                    SoLuong INTEGER NULL,
                    NhaXuatBan TEXT NULL,
                    GiaTri REAL NULL,
                    TinhTrang TEXT NULL,
                    FOREIGN KEY (MaTheLoai) REFERENCES TheLoai(MaTheLoai)
                );
                
                -- Bảng Người Dùng
                CREATE TABLE IF NOT EXISTS NguoiDung (
                    MaDocGia TEXT PRIMARY KEY,
                    HoVaTen TEXT NULL,
                    GioiTinh TEXT NULL,
                    NgaySinh DATE NULL,
                    DienThoai TEXT NULL,
                    MatKhau TEXT NULL,
                    PhanQuyen TEXT NULL,
                    CHECK (PhanQuyen IN ('Giảng viên', 'Sinh viên', 'Admin','Thủ Thư'))
                );
                
                -- Bảng Phiếu Mượn
                CREATE TABLE IF NOT EXISTS PhieuMuon (
                    MaPhieuMuon INTEGER PRIMARY KEY AUTOINCREMENT,
                    MaDocGia TEXT NULL,
                    NgayMuon DATE NULL,
                    NgayHenTra DATE NULL,
                    TrangThai TEXT NULL DEFAULT 'Đang mượn',
                    FOREIGN KEY (MaDocGia) REFERENCES NguoiDung(MaDocGia)
                );
                
                -- Bảng Chi Tiết Phiếu Mượn
                CREATE TABLE IF NOT EXISTS ChiTietPhieuMuon (
                    MaChiTiet INTEGER PRIMARY KEY AUTOINCREMENT,
                    MaPhieuMuon INTEGER NULL,
                    MaSach TEXT NULL,
                    SoLuong INTEGER NULL,
                    DaTra INTEGER NULL DEFAULT 0,
                    FOREIGN KEY (MaPhieuMuon) REFERENCES PhieuMuon(MaPhieuMuon),
                    FOREIGN KEY (MaSach) REFERENCES Sach(MaSach)
                );
                
                -- Bảng Phiếu Trả
                CREATE TABLE IF NOT EXISTS PhieuTra (
                    MaPhieuTra INTEGER PRIMARY KEY AUTOINCREMENT,
                    MaPhieuMuon INTEGER NULL,
                    NgayTra DATE NULL,
                    GhiChu TEXT,
                    FOREIGN KEY (MaPhieuMuon) REFERENCES PhieuMuon(MaPhieuMuon)
                );
                
                -- Bảng Chi Tiết Phiếu Trả
                CREATE TABLE IF NOT EXISTS ChiTietPhieuTra (
                    MaChiTietTra INTEGER PRIMARY KEY AUTOINCREMENT,
                    MaPhieuTra INTEGER NULL,
                    MaSach TEXT NULL,
                    SoLuong INTEGER NULL,
                    TinhTrangSach TEXT NULL,
                    FOREIGN KEY (MaPhieuTra) REFERENCES PhieuTra(MaPhieuTra),
                    FOREIGN KEY (MaSach) REFERENCES Sach(MaSach)
                );
            """)
            
            cursor.execute("SELECT COUNT(*) FROM TheLoai")
            if cursor.fetchone()[0] == 0:
                cursor.executescript("""
                    INSERT INTO TheLoai VALUES ('TL001', 'Tiểu thuyết tình cảm');
                    INSERT INTO TheLoai VALUES ('TL002', 'Tiểu thuyết trinh thám');
                    INSERT INTO TheLoai VALUES ('TL003', 'Tiểu thuyết khoa học viễn tưởng');
                    INSERT INTO TheLoai VALUES ('TL004', 'Tiểu thuyết kinh dị');
                    INSERT INTO TheLoai VALUES ('TL005', 'Văn học Việt Nam');
                    INSERT INTO TheLoai VALUES ('TL006', 'Văn học nước ngoài');
                    INSERT INTO TheLoai VALUES ('TL007', 'Văn học hiện đại');
                    INSERT INTO TheLoai VALUES ('TL008', 'Văn học cổ điển');
                    INSERT INTO TheLoai VALUES ('TL009', 'Sách tâm lý học');
                    INSERT INTO TheLoai VALUES ('TL010', 'Sách kinh tế học');
                    INSERT INTO TheLoai VALUES ('TL011', 'Sách trí tuệ nhân tạo (AI)');
                    INSERT INTO TheLoai VALUES ('TL012', 'Sách an ninh mạng');
                    INSERT INTO TheLoai VALUES ('TL013', 'Sách điện tử - Viễn thông');
                    INSERT INTO TheLoai VALUES ('TL014', 'Sách cơ khí - Ô tô');
                    INSERT INTO TheLoai VALUES ('TL015', 'Sách tài chính - Đầu tư');
                    INSERT INTO TheLoai VALUES ('TL016', 'Sách tư duy lãnh đạo');
                                     
                """)
            
            cursor.execute("SELECT COUNT(*) FROM NguoiDung WHERE PhanQuyen = 'Admin'")
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    INSERT INTO NguoiDung (MaDocGia, HoVaTen, GioiTinh, NgaySinh, DienThoai, MatKhau, PhanQuyen)
                    VALUES ('Admin', 'Quản trị viên', 'Nam', '1990-01-01', '0123456789', '1', 'Admin')
                """)
            
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")
            return False
    
    def close_connection(self):
        if self.conn:
            self.conn.close()