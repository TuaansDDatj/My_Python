import tkinter as tk
from Data.db_manager import Database
from Managers.book_manager import BookManager
from Managers.user_manager import UserManager
from Managers.borrow_manager import BorrowManager
from Managers.return_manager import ReturnManager
from Managers.report_manager import ReportManager
from GUI.login_view import LoginView

def main():
    db = Database()
    book_manager = BookManager(db)
    user_manager = UserManager(db)
    borrow_manager = BorrowManager(db)
    return_manager = ReturnManager(db)
    report_manager = ReportManager(db)
    
    root = tk.Tk()
    login_view = LoginView(root, db, book_manager, user_manager, borrow_manager, return_manager, report_manager)
    
    root.mainloop()
    
if __name__ == "__main__":
    main()