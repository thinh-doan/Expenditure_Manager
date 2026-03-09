# nhận nút bấm, đọc dữ liệu từ ô nhập, gọi các hàm xử lý dữ liệu

from PyQt6.QtWidgets import QMainWindow, QDialog, QMessageBox, QTableWidgetItem

from Ex_Manager_Process import Ex_Manager_Process
from Inter_MainWindow import Ui_MainWindow
from Inter_Expense import Ui_Dialog as ExpenseUI
from Inter_Income import Ui_Dialog as IncomeUI

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
        self.btnAdd_Expense.clicked.connect(self.open_add_expense)
        self.btnSummarize.clicked.connect(self.summarize)
        self.btnRefresh.clicked.connect(self.refresh)

        # kết nối các lineEdit
        self.hien_thi_tableInfor()  #Hiển thị dữ liệu ban đầu

    def open_add_income(self):
        dialog = Income_dialog(self.processer, self)
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
            self.tableInfor.setItem(row, 0, QTableWidgetItem(trans["date"]))
            self.tableInfor.setItem(row, 1, QTableWidgetItem(trans["type"]))
            self.tableInfor.setItem(row, 2, QTableWidgetItem(trans["category"]))
            self.tableInfor.setItem(row, 3, QTableWidgetItem(str(trans["amount"])))
            self.tableInfor.setItem(row, 4, QTableWidgetItem(trans["note"]))

    #Thiếu safety box
    def summarize(self):
        data = self.processer.tinh_tong()

        self.txtIncome.setText(str(data["Income"]["total"])); self.txtIncome.setReadOnly(True)
        self.txtExpense.setText(str(data["Expense"]["total"])); self.txtExpense.setReadOnly(True)

        self.hien_thi_tableThisMonth()

    def hien_thi_tableThisMonth(self):
        data = self.processer.tinh_tong()
        
        row_map = {
            0: ("Income", "total"),
            1: ("Income", "Salary"),
            2: ("Income", "Allowance"),
            3: ("Income", "Full-time job"),
            4: ("Income", "Part-time job"),
            5: ("Income", "Other"),
            6: ("Saving", "total"),
            7: ("Saving", "Emergency"),
            8: ("Saving", "Goal"),
            9: ("Saving", "General"),
            10: ("Saving", "Other"),
            11: ("Expense", "total"),
            12: ("Expense", "Food"),
            13: ("Expense", "Transport"),
            14: ("Expense", "Education"),
            15: ("Expense", "Entertainment"),
            16: ("Expense", "Other")
        }

        for row, (tr_type, ctg) in row_map.items():     #items dùng để lấy cả key và value
            amount = data.get(tr_type, {}).get(ctg, 0)
            self.tableThisMonth.setItem(row, 0, QTableWidgetItem(f"{amount:.2f}"))


    # def kiem_tra_thang(self):
    #     month = self.txtMonth.text().strip()    # strip để loại bỏ khoảng trống


    #     try:
    #         m, y = month.split("-")
    #         m = int(m)
    #         y = int(y)
    #     except:
    #         QMessageBox.warning(self, "Error", "Định dạng phải là MM-YYYY!")
    #         return False

    #     if m < 1 or m > 12:
    #         QMessageBox.warning(self, "Error", "Tháng phải từ 01 đến 12!")
    #         return False

    #     data = self.processer.lay_du_lieu_tu_json()

    #     if month in data["Months"]:
    #         QMessageBox.warning(self, "Error", "Tháng đã tồn tại!")
    #         return False

    #     return True     # nghĩa là tháng chưa có trong danh sách


    # refresh table và lưu dữ liệu vào json
    def refresh(self):
        month = "02-2026"

        self.processer.luu_thang(month)
        self.processer.luu_safety_box()

        self.processer.reset_transactions()

        # reset table & summarize
        self.tableInfor.setRowCount(0)
        self.tableThisMonth.clearContents()
        self.txtIncome.clear()
        self.txtSaving.clear()
        self.txtExpense.clear()



        self.hien_thi_safety_box()

    def hien_thi_safety_box(self):
        data = self.processer.lay_du_lieu_tu_json()
        sb = data.get("Safety Box", 0)  #.get() lấy giá trị của key, nếu key không tồn tại thì trả về default value
        self.txtSafetyBox.setText(str(sb))