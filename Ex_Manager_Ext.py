# nhận nút bấm, đọc dữ liệu từ ô nhập, gọi các hàm xử lý dữ liệu

from PyQt6.QtWidgets import QMainWindow, QDialog, QMessageBox, QTableWidgetItem

from Ex_Manager_Process import Ex_Manager_Process
from Inter_MainWindow import Ui_MainWindow
from Inter_Expense import Ui_MainWindow as ExpenseUI
from Inter_Income import Ui_MainWindow as IncomeUI
from Inter_Saving import Ui_MainWindow as SavingUI

class Add_Expense(QDialog):
    def __init__(self, process, parent= None):
        super().__init__(parent)
        self.ui = ExpenseUI()
        self.ui.setupUi(self)
        self.process = process
        self.ui.btnOK.clicked.connect(self.add_expense)
        self.ui.btnCancel.clicked.connect(self.reject)

    def add_expense(self):
        tr_category = self.ui.cbbCategory.currentText()
        tr_amount = self.ui.txtAmount.text()
        tr_date = self.ui.txtDate.text()
        tr_note = self.ui.txtNote.text()

        success, message = self.process.add_transaction("Expense", tr_category, tr_amount, tr_date, tr_note)
        if success is True:
            self.accept()
        else:
            QMessageBox.warning(self, "Error", message)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent= None):
        super().__init__(parent)
        self.setupUi(self)
        self.process = Ex_Manager_Process()

        #kết nối với nút bấm
        self.btnAdd_Expense.clicked.connect(self.open_add_expense)

    def open_add_expense(self):
        dialog = Add_Expense(self.process, self)
        if dialog.exec():
            self.hien_thi_tableInfor()

    def hien_thi_tableInfor(self):

        self.tableInfor.setRowCount(0)

        transactions = self.process.get_transactions()

        for row, trans in enumerate(transactions):

            self.tableInfor.insertRow(row)

            self.tableInfor.setItem(row, 0, QTableWidgetItem(trans['date']))
            self.tableInfor.setItem(row, 1, QTableWidgetItem(trans['type']))
            self.tableInfor.setItem(row, 2, QTableWidgetItem(trans['category']))
            self.tableInfor.setItem(row, 3, QTableWidgetItem(str(trans['amount'])))
            self.tableInfor.setItem(row, 4, QTableWidgetItem(trans['note']))