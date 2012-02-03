#!/usr/bin/python
import sys
import Logon

from PySide import QtCore, QtGui
from gui.MainWindow import MainWindow

if __name__ == "__main__":
    # Basic initialising of the application, loading our main widget templates
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    
    window.show()
    Logon.disconnectDrives()

    sys.exit(app.exec_())