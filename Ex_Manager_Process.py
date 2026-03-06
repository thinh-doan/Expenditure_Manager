# danh sách chi tiêu, thêm, xoá, tính tổng tiền, lưu file

from Inter_MainWindow import Ui_MainWindow
from Inter_Expense import Ui_MainWindow as ExpenseUI
from Inter_Income import Ui_MainWindow as IncomeUI
from Inter_Saving import Ui_MainWindow as SavingUI
from PyQt6.QtWidgets import QMainWindow

class Ex_Manager(QMainWindow, Ui_MainWindow):
    ds = []

    def __init__(self, tr_category, tr_amount, tr_date, tr_note, parent= None):
        self.tr_category = tr_category
        self.tr_amount = tr_amount
        self.tr_date = tr_date
        self.tr_note = tr_note


    def 

    