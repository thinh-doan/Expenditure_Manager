#Khởi tạo giao diện

import sys
from Ex_Manager_Ext import Ex_Manager_Ext
from PyQt6.QtWidgets import QApplication

app = QApplication(sys.argv)

w = Ex_Manager_Ext()
w.show()

sys.exit(app.exec())