from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore   import pyqtSlot, pyqtSignal,QTimer, QDateTime,Qt, QObject
from DialogScreen.WaitToSaveDialogUi    import Ui_Dialog

class WaitToSaveDialog(QObject, Ui_Dialog):

    def __init__(self):
        QObject.__init__(self)
        Ui_Dialog.__init__(self)
        self.dialog = QtWidgets.QDialog()
        self.dialog.setWindowModality(QtCore.Qt.WindowModal)
        self.dialog.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setupUi(self.dialog)
        self.label_forShowFaceIcon.setPixmap(QtGui.QPixmap("icon/faceIcon40.png"))
        self.label_forShowFGPicon.setPixmap(QtGui.QPixmap("icon/fingerIcon40.png"))
        self.label_forShowCardIcon.setPixmap(QtGui.QPixmap("icon/cardIcon40.png"))
        self.pushButton_ok.clicked.connect(self.CloseDialog)
    def ShowDialog(self):

        self.dialog.show()
        self.dialog.raise_()
        # self.dialog.startTimer(2000)
        # self.dialog.timerEvent = lambda event: self.CloseDialog()
        self.dialog.exec()
    def ShowResult(self, resultObject):
        if(resultObject.faceAdded):
            self.label_forShowAddFaceResult.setStyleSheet('color: rgb(0, 104, 0);font: 75 bold 14pt "Ubuntu";')
            self.label_forShowAddFaceResult.setText("ĐÃ THÊM KHUÔN MẶT")
        else:
            self.label_forShowAddFaceResult.setStyleSheet('color: rgb(104, 0, 0);font: 75 bold 14pt "Ubuntu";')
            self.label_forShowAddFaceResult.setText("CHƯA THÊM KHUÔN MẶT")

        if(resultObject.FGPadded):
            self.label_forShowAddFGPresult.setStyleSheet('color: rgb(0, 104, 0);font: 75 bold 14pt "Ubuntu";')
            self.label_forShowAddFGPresult.setText("ĐÃ THÊM VÂN TAY")
        else:
            self.label_forShowAddFGPresult.setStyleSheet('color: rgb(104, 0, 0);font: 75 bold 14pt "Ubuntu";')
            self.label_forShowAddFGPresult.setText("CHƯA THÊM VÂN TAY ")

        if(resultObject.cardWritten):
            self.label_forShowAddCardResult.setStyleSheet('color: rgb(0, 104, 0);font: 75 bold 14pt "Ubuntu";')
            self.label_forShowAddCardResult.setText("ĐÃ GHI THẺ")
        else:
            self.label_forShowAddCardResult.setStyleSheet('color: rgb(104, 0, 0);font: 75 bold 14pt "Ubuntu";')
            self.label_forShowAddCardResult.setText("CHƯA GHI THẺ ")

    def CloseDialog(self):
        self.dialog.close()
        self.deleteLater()
        #self.dialog.killTimer(0)
