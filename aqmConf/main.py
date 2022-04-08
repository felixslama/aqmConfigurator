from sys import argv as sysargv, exit as sysex
from PyQt5.QtWidgets import QApplication
from .views import Window

def main():
    app = QApplication(sysargv)
    win = Window()
    win.setStyleSheet("background-color: #333333; color: #dddddd")
    win.show()
    sysex(app.exec_())
