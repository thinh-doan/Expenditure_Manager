#Khởi tạo giao diện
from PyQt6.QtGui import QIcon
import sys
from Ex_Manager_Ext import MainWindow, ICON_PATH
from PyQt6.QtWidgets import QApplication

app = QApplication(sys.argv)
app.setWindowIcon(QIcon(str(ICON_PATH)))

w = MainWindow()
w.show()

sys.exit(app.exec())