from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore   import pyqtSlot, pyqtSignal,QTimer, QDateTime,Qt, QObject
from DialogScreen.WaitToSaveDialogUi    import Ui_Dialog

class WaitToSaveDialog(QObject, Ui_Dialog):

    def __init__(self):
        QObject.__init__(self)
        Ui_Dialog.__init__(self)
        
        
    def ShowDialog(self):
        self.dialog = QtWidgets.QDialog()
        self.dialog.setWindowModality(QtCore.Qt.WindowModal)
        self.dialog.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setupUi(self.dialog)
        self.label.setPixmap(QtGui.QPixmap("icon/saveIcon100.png"))
        self.dialog.show()
        self.dialog.raise_()
        # self.dialog.startTimer(2000)
        # self.dialog.timerEvent = lambda event: self.CloseDialog()
        self.dialog.exec()

    def CloseDialog(self):
        self.dialog.close()
        #self.dialog.killTimer(0)
