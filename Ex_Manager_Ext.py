# nhận nút bấm, đọc dữ liệu từ ô nhập, gọi các hàm xử lý dữ liệu

from PyQt6.QtWidgets import QMainWindow, QDialog, QMessageBox, QTableWidgetItem, QInputDialog, QSizePolicy
from PyQt6 import uic
import json
from PyQt6.QtGui import QIcon
from pathlib import Path

from Ex_Manager_Process import Ex_Manager_Process
from Inter_MainWindow import Ui_MainWindow
from Inter_Expense import Ui_Dialog as ExpenseUI
from Inter_Income import Ui_Dialog as IncomeUI


BASE_DIR = Path(__file__).resolve().parent
ICON_PATH = BASE_DIR / "assets" / "LOGO.png"


class Income_dialog(QDialog, IncomeUI):
    def __init__(self, processer, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.processer = processer

        self.btnOK.clicked.connect(self.add_income)
        self.btnCancel.clicked.connect(self.reject)

        # Kết nối sự kiện định dạng tiền
        self.txtAmount.textChanged.connect(self.format_amount)

        # Kết nối sự kiện thay đổi ngày trên Calendar
        self.calendarWidget.clicked.connect(self.update_date_display)
        self.txtDate.setReadOnly(True)
        self.update_date_display() # Cập nhật lần đầu tiên

    # Cập nhật QLineEdit hiển thị ngày từ Calendar
    def update_date_display(self):
        selected_date = self.calendarWidget.selectedDate()
        date_str = selected_date.toString("dd/MM/yyyy")
        self.txtDate.setText(date_str)

    # Tự động thêm dấu phẩy khi nhập tiền"""
    def format_amount(self):
        text = self.txtAmount.text()
        text = text.replace(',', '')  # Xóa dấu phẩy cũ

        if text and text.isdigit():  # Nếu là số
            formatted = '{:,}'.format(int(text))
            self.txtAmount.setText(formatted)

    def add_income(self):
        tr_date = self.txtDate.text()
        tr_category = self.cbbCategory.currentText()
        tr_amount = self.txtAmount.text().replace(',', '')  # Xóa dấu phẩy trước gửi
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

        # Kết nối sự kiện định dạng tiền
        self.txtAmount.textChanged.connect(self.format_amount)

        # Kết nối sự kiện thay đổi ngày trên Calendar
        self.calendarWidget.clicked.connect(self.update_date_display)
        self.txtDate.setReadOnly(True)
        self.update_date_display()    # Cập nhật lần đầu tiên

        #  Cập nhật QLineEdit hiển thị ngày từ Calendar
    def update_date_display(self):
        selected_date = self.calendarWidget.selectedDate()
        date_str = selected_date.toString("dd/MM/yyyy")
        self.txtDate.setText(date_str)

    def format_amount(self):
        """Tự động thêm dấu phẩy khi nhập tiền"""
        text = self.txtAmount.text()
        text = text.replace(',', '')  # Xóa dấu phẩy cũ

        if text and text.isdigit():  # Nếu là số
            formatted = '{:,}'.format(int(text))
            self.txtAmount.setText(formatted)

    def add_expense(self):
        tr_category = self.cbbCategory.currentText()
        tr_amount = self.txtAmount.text().replace(',', '')
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

        # LOGO
        self.setWindowTitle("Expenditure App")
        self.setWindowIcon(QIcon(str(ICON_PATH)))

        # kết nối nút
        self.btnAdd_Income.clicked.connect(self.open_add_income)
        self.btnAdd_Expense.clicked.connect(self.open_add_expense)
        self.btnSummarize.clicked.connect(self.summarize)
        self.btnRefresh.clicked.connect(self.refresh)
        self.btnSearch.clicked.connect(self.tim_kiem_thang)
        self.btnCompare.clicked.connect(self.compare_months)
        self.btnEditSafetyBox.clicked.connect(self.edit_safety_box)

        # kết nối các lineEdit
        # self.hien_thi_tableInfor()  #Hiển thị dữ liệu ban đầu

        # Kéo giãn bảng
        self.tableInfor.horizontalHeader().setStretchLastSection(True)
        self.tableThisMonth.horizontalHeader().setStretchLastSection(True)
        self.tablePreviousMonths.horizontalHeader().setStretchLastSection(True)

        self.setup_ui_style()

    #deco giao diện
    def setup_ui_style(self):

        self.setStyleSheet("""
        
        QMainWindow{
            border-image: url(image/background2.png) 0 0 0 0 stretch stretch;
        }

        QLabel{
            font-size:16px;
        }                  


        /* ===== BUTTON ===== */

        QPushButton{
            background-color: #edc84c;
            color:white;
            border-radius:6px;
            padding:6px 10px;
            font-weight:bold;
        }

        QPushButton:hover{
            background-color: #f5e19f;
            border:2px solid #F57C00;
        }

        QPushButton:pressed{
            background-color:#ff6600;
            border:2px solid #ff6600;
        }

        /* ===== SEARCH BUTTON ===== */

        QPushButton#btnSearch{
            background-color:#4da6ff;
        }

        QPushButton#btnSearch:hover{
            background-color:#1E88E5;
        }

        /* ===== TABLE ===== */
        QTableWidget{
            background: white;
            border:1px solid #a6a600;
            gridline-color:green;
            selection-background-color:#1E88E5;
            font-size:11px;
        }

        QHeaderView::section{
            background-color:#e6e600;
            color:white;
            padding:4px;
            border-right:2px solid #a6a600;
            font-weight:bold;
        }

        /* ===== INPUT BOX ===== */

        QLineEdit{
            border:1px solid #ccc;
            border-radius:5px;
            padding:4px;
            background:white;
        }

        QLineEdit:focus{
            border:1px solid #4CAF50;
        }

        /* ===== COMMENT BOX ===== */

        QPlainTextEdit{
            border:1px solid #33cc33;
            border-radius:6px;
            background-color:white;
        }

        /* ===== TAB ===== */

        QTabWidget::pane{
            border:1px solid #ccc;
            background-color:white;
        }

        QTabBar::tab{
            background:#dcdde1;
            padding:8px 15px;
            border-top-left-radius:6px;
            border-top-right-radius:6px;
        }

        QTabBar::tab:selected{
            background:white;
            font-weight:bold;
        }

        """)

        

    def open_add_income(self):
        dialog = Income_dialog(self.processer, self)
        if dialog.exec():
            self.hien_thi_tableInfor()

    def open_add_expense(self):
        dialog = Expense_dialog(self.processer, self)
        if dialog.exec():
            self.hien_thi_tableInfor()

    def format_number(self, value):
        """Format số với dấu phẩy ở tableInfor"""
        return '{:,}'.format(int(float(value)))

    # Hiển thị các bảng
    def hien_thi_tableInfor(self):
        self.tableInfor.setRowCount(0)
        transactions = self.processer.get_transactions()
        for row, trans in enumerate(transactions):
            self.tableInfor.insertRow(row)
            self.tableInfor.setItem(row, 0, QTableWidgetItem(trans["date"]))
            self.tableInfor.setItem(row, 1, QTableWidgetItem(trans["type"]))
            self.tableInfor.setItem(row, 2, QTableWidgetItem(trans["category"]))
            self.tableInfor.setItem(row, 3, QTableWidgetItem(self.format_number(trans["amount"])))
            self.tableInfor.setItem(row, 4, QTableWidgetItem(trans["note"]))

    def hien_thi_table(self, table, data):
        row_map = {
            0: ("Income", "total"),
            1: ("Income", "Salary"),
            2: ("Income", "Allowance"),
            3: ("Income", "Full-time job"),
            4: ("Income", "Part-time job"),
            5: ("Income", "Other"),
            6: ("Expense", "total"),
            7: ("Expense", "Food"),
            8: ("Expense", "Transport"),
            9: ("Expense", "Education"),
            10: ("Expense", "Entertainment"),
            11: ("Expense", "Other"),
            12: ("Saving", "total")
        }

        # Đảm bảo table có đủ row và cột
        table.setRowCount(len(row_map)) # reset table, xóa toàn bộ row cũ, tọa đúng số row mới
        table.setColumnCount(1) # đảm bảo cột tồn tại và tạo 1 cột
        table.setHorizontalHeaderLabels(["Amount"])

        for row, (tr_type, ctg) in row_map.items():     #items dùng để lấy cả key và value
            amount = data[tr_type][ctg]         # chú ý xem có bị lỗi không
            table.setItem(row, 0, QTableWidgetItem(f"{self.format_number(amount)}"))

    def hien_thi_safety_box(self):
        data = self.processer.lay_du_lieu_tu_json()
        sb = data.get("Safety Box", 0)  #.get() lấy giá trị của key, nếu key không tồn tại thì trả về default value
        self.txtSafetyBox.setText(self.format_number(sb))

    def summarize(self):
        data = self.processer.tinh_tong()

        # kiểm tra tháng đã có dữ liệu chưa
        if data["Expense"]["total"] + data["Income"]["total"] == 0:
            QMessageBox.warning(self, "Error", "Vui lòng thêm một thu nhập hoặc chi tiêu!")
            return

        self.txtIncome.setText(self.format_number(data["Income"]["total"])); self.txtIncome.setReadOnly(True)
        self.txtExpense.setText(self.format_number(data["Expense"]["total"])); self.txtExpense.setReadOnly(True)
        self.txtSaving.setText(self.format_number(data["Saving"]["total"])); self.txtSaving.setReadOnly(True)
        
        #Hiển thị table This Month
        self.hien_thi_table(self.tableThisMonth, data)


    """"lệnh Refresh: lưu tháng và safety_box vào JSON; 
        clear transactions, các bảng và nút bấm; 
        hiển thị safety_box."""
    def refresh(self):
        month = self.processer.lay_thang_tu_transactions()

        self.processer.luu_vao_json(month)
        self.processer.reset_transactions()

        self.tableInfor.setRowCount(0)
        self.tableThisMonth.clearContents()

        self.txtIncome.clear()
        self.txtSaving.clear()
        self.txtExpense.clear()
        self.txtComment.clear()

        self.hien_thi_safety_box()

    def tim_kiem_thang(self, month):
        month = self.txtSearch.text().strip()
        if not month:
            QMessageBox.warning(self, "Error", "Vui lòng nhập tháng!")
            return

        # Kiểm tra tháng có tồn tại trong JSON không
        if self.processer.kiem_tra_thang_tu_json(month):
            json_data = self.processer.lay_du_lieu_tu_json()
            data = json_data["Months"][month]
            self.hien_thi_table(self.tablePreviousMonths, data)
        else:
            QMessageBox.warning(self, "Error", "Tháng chưa được lưu!")
    
    def edit_safety_box(self):
        value, ok = QInputDialog.getInt(self, "Edit Safety Box", "Nhập số tiền:", 0, 0)
        if ok:
            data = self.processer.lay_du_lieu_tu_json()
            data["Safety Box"] = value

            with open("data.json", "w", encoding="utf8") as f:
                json.dump(data, f, ensure_ascii=False, indent=3)

            self.txtSafetyBox.setText(self.format_number(value))
    
    # So sánh 2 tháng gần nhất
    def compare_months(self):
        result = self.processer.compare_month()
        
        if not result["status"]:
            QMessageBox.warning(self, "Thông báo", result["message"])
            return
        
        # Tạo tin nhắn so sánh
        comp = result["comparison"]
        message = f" === Compare: {comp['Income']['last_month']} vs {comp['Income']['this_month']} === \n\n"
        
        for section, data in comp.items():
            message += f"{section}:\n"
            message += f"  Last Month: {self.format_number(data['last_value'])}\n"
            message += f"  This Month:  {self.format_number(data['this_value'])}\n"
            message += f"  Difference:   {self.format_number(data['change_value'])}\n"
            message += f"  {data['change_type']}: {abs(data['percent_change']):.2f}%\n\n"
        
        self.txtComment.setPlainText(message)


