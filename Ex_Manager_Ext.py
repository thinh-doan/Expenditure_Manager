# nhận nút bấm, đọc dữ liệu từ ô nhập, gọi các hàm xử lý dữ liệu

from PyQt6.QtWidgets import QMainWindow, QDialog, QMessageBox, QTableWidgetItem

from Ex_Manager_Process import Ex_Manager_Process
from Inter_MainWindow import Ui_MainWindow
from Inter_Expense import Ui_Dialog as ExpenseUI
from Inter_Income import Ui_Dialog as IncomeUI
from Inter_Saving import Ui_Dialog as SavingUI


class Income_dialog(QDialog, IncomeUI):
    def __init__(self, processer, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.processer = processer
        self.btnOK.clicked.connect(self.add_income)
        self.btnCancel.clicked.connect(self.reject)

    def add_income(self):
        tr_date = self.txtDate.text()
        tr_category = self.cbbCategory.currentText()
        tr_amount = self.txtAmount.text()
        tr_note = self.txtNote.text()

        success, message = self.processer.add_transaction("Income", tr_category, tr_amount, tr_date, tr_note)
        if success:
            self.accept()
        else:
            QMessageBox.warning(self, "Error", message)

class Saving_dialog(QDialog, SavingUI):
    def __init__(self, processer, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.processer = processer

        self.btnOK.clicked.connect(self.add_saving)
        self.btnCancel.clicked.connect(self.reject)

    def add_saving(self):
        tr_date = self.txtDate.text()
        tr_category = self.cbbCategory.currentText()
        tr_amount = self.txtAmount.text()
        tr_note = self.txtNote.text()
        
        success, message = self.processer.add_transaction("Saving", tr_category,tr_amount, tr_date, tr_note)
        if success:
            self.accept()   # gửi signal tới exec() để đóng chương trình
        else:
            QMessageBox.warning(self, "Error", message)
        

class Expense_dialog(QDialog, ExpenseUI):

    def __init__(self, processer, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.processer = processer

        self.btnOK.clicked.connect(self.add_expense)
        self.btnCancel.clicked.connect(self.reject)

    def add_expense(self):

        tr_category = self.cbbCategory.currentText()
        tr_amount = self.txtAmount.text()
        tr_date = self.txtDate.text()
        tr_note = self.txtNote.text()

        success, message = self.processer.add_transaction("Expense", tr_category, tr_amount, tr_date, tr_note)

        if success:
            self.accept()
        else:
            QMessageBox.warning(self, "Error", message)

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.processer = Ex_Manager_Process()

        # kết nối nút
        self.btnAdd_Income.clicked.connect(self.open_add_income)
        self.btnAdd_Saving.clicked.connect(self.open_add_saving)
        self.btnAdd_Expense.clicked.connect(self.open_add_expense)
        
        self.hien_thi_tableInfor()  #Hiển thị dữ liệu ban đầu

    def open_add_income(self):
        dialog = Income_dialog(self.processer, self)
        if dialog.exec():
            self.hien_thi_tableInfor()

    def open_add_saving(self):
        dialog = Saving_dialog(self.processer, self)
        if dialog.exec():
            self.hien_thi_tableInfor()

    def open_add_expense(self):
        dialog = Expense_dialog(self.processer, self)
        if dialog.exec():
            self.hien_thi_tableInfor()

    def hien_thi_tableInfor(self):
        self.tableInfor.setRowCount(0)
        transactions = self.processer.get_transactions()
        for row, trans in enumerate(transactions):
            self.tableInfor.insertRow(row)
            self.tableInfor.setItem(row, 0, QTableWidgetItem(trans['date']))
            self.tableInfor.setItem(row, 1, QTableWidgetItem(trans['type']))
            self.tableInfor.setItem(row, 2, QTableWidgetItem(trans['category']))
            self.tableInfor.setItem(row, 3, QTableWidgetItem(str(trans['amount'])))
            self.tableInfor.setItem(row, 4, QTableWidgetItem(trans['note']))