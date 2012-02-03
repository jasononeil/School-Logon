from gui.forms.Ui_MainWindow import Ui_MainWindow
from PySide import QtCore, QtGui
import Logon;

class MainWindow(QtGui.QMainWindow):
    def attemptLogin(self):
	    print "Stand back! We're going to attempt a login.\n"

	    username = self.ui.username.text()
	    password = self.ui.password.text()
	    
	    Logon.connectToPWSDrives(username,password)

    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.connect(self.ui.loginButton, QtCore.SIGNAL("clicked()"),self.attemptLogin)
        
        
        # Connect the pushButton to a message method.
        #self.connect(self.ui.pushButton, QtCore.SIGNAL("clicked()"),message)
    
	