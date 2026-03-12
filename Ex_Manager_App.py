#Khởi tạo giao diện

import sys
from Ex_Manager_Ext import MainWindow, BASE_DIR
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

app = QApplication(sys.argv)
app.setWindowIcon(QIcon(str(BASE_DIR)))

w = MainWindow()
w.show()

sys.exit(app.exec())