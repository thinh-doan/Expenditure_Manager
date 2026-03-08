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
        self.btnSummarize.clicked.connect(self.summarize)

        # kết nối các lineEdit
        self.hien_thi_tableInfor()  #Hiển thị dữ liệu ban đầu

    def open_add_income(self):
        while True:
            if self.kiem_tra_thang():
                dialog = Income_dialog(self.processer, self)
                if dialog.exec():
                    self.hien_thi_tableInfor()


    def open_add_saving(self):
        if self.kiem_tra_thang():
            dialog = Saving_dialog(self.processer, self)
            if dialog.exec():
                self.hien_thi_tableInfor()

    def open_add_expense(self):
        if self.kiem_tra_thang():
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

    #Thiếu safety box
    def summarize(self):
        data = self.processer.tinh_tong()

        self.txtIncome.setText(str(data['Income']['total'])); self.txtIncome.setReadOnly(True)
        self.txtSaving.setText(str(data['Saving']['total'])); self.txtSaving.setReadOnly(True)
        self.txtExpense.setText(str(data['Expense']['total'])); self.txtExpense.setReadOnly(True)

        self.hien_thi_tableThisMonth()

    def hien_thi_tableThisMonth(self):
        data = self.processer.tinh_tong()
        
        row_map = {
            0: ('Income', 'total'),
            1: ('Income', 'Salary'),
            2: ('Income', 'Allowance'),
            3: ('Income', 'Full-time job'),
            4: ('Income', 'Part-time job'),
            5: ('Income', 'Other'),
            6: ('Saving', 'total'),
            7: ('Saving', 'Emergency'),
            8: ('Saving', 'Goal'),
            9: ('Saving', 'General'),
            10: ('Saving', 'Other'),
            11: ('Expense', 'total'),
            12: ('Expense', 'Food'),
            13: ('Expense', 'Transport'),
            14: ('Expense', 'Education'),
            15: ('Expense', 'Entertainment'),
            16: ('Expense', 'Other')
        }

        for row, (tr_type, ctg) in row_map.items():     #items dùng để lấy cả key và value
                amount = data[tr_type][ctg]
                self.tableThisMonth.setItem(row, 0, QTableWidgetItem(f"{amount:.2f}"))


    def kiem_tra_thang(self):
        data = self.processer.lay_du_lieu_tu_json()
        saved_months = data['Months']

        month = self.txtMonth.text().strip()

        # kiểm tra người dùng đã nhập đủ chưa
        if "-" not in month or len(month) != 7:
            QMessageBox.warning(self, "Error", "Vui lòng nhập đúng định dạng MM-YYYY!")
            return False, None

        try:
            m, y = month.split("-")
            m = int(m)
            y = int(y)
        except ValueError:
            QMessageBox.warning(self, "Error", "Tháng không hợp lệ!")
            return False, None

        # kiểm tra tháng 1–12
        if m < 1 or m > 12:
            QMessageBox.warning(self, "Error", "Vui lòng nhập tháng từ 01 đến 12!")
            return False, None

        # kiểm tra tháng đã tồn tại
        if month in saved_months:
            QMessageBox.warning(self, "Error", "Tháng đã tồn tại, vui lòng nhập tháng khác!")
            return False, "Existed"

        return True, month


    # refresh table và lưu dữ liệu vào json
    def refresh(self):
        pass