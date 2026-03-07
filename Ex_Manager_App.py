#Khởi tạo giao diện

import sys
from Ex_Manager_Ext import MainWindow
from PyQt6.QtWidgets import QApplication

app = QApplication(sys.argv)

w = MainWindow()
w.show()

sys.exit(app.exec())