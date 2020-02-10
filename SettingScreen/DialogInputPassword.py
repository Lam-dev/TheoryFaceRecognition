from PyQt5                  import QtCore, QtGui, QtWidgets
from PyQt5                  import QtCore, QtGui, QtWidgets
from PyQt5.QtGui            import QIcon, QPixmap
from PyQt5.QtCore           import pyqtSlot, pyqtSignal,QTimer, QDateTime, Qt, QObject, QPointF, QPropertyAnimation, pyqtProperty
from SettingScreen.DialogInputPasswordUI    import Ui_Frame_forInputPassword
from DatabaseAccess.DatabaseAccess    import ThongTinTaiKhoanQuanLy

class DialogInputPassword(QObject, Ui_Frame_forInputPassword):
    SignalPasswordCorrect = pyqtSignal()
    SignalRequestExitScreen = pyqtSignal()
    
    
    def __init__(self, frame):
        Ui_Frame_forInputPassword.__init__(self)
        QObject.__init__(self)
        self.setupUi(frame)
        self.timerForShowPasswordInvalid = QTimer(self)
        self.timerForShowPasswordInvalid.timeout.connect(self.ReshowAccountName)
        
        self.pushButton_ok.clicked.connect(self.ComparePassword)
        self.pushButton_exit.clicked.connect(self.SignalRequestExitScreen.emit)
        self.passwordAndAcount = ""

    def SetAccountAndPasswordForCheck(self, accountAndPassword):
        self.passwordAndAcount = accountAndPassword
        self.ShowAccount(accountAndPassword.TaiKhoan)
        
        
    def ComparePassword(self):
        if(self.lineEdit_forInputPassword.text() == self.passwordAndAcount.MatKhau):
            self.SignalPasswordCorrect.emit()
        else:
            self.ShowPasswordInvalidNotify()

    def ShowAccount(self, nameAccount):
        self.accountName = "NHẬP MẬT KHẨU CHO  "+ nameAccount
        self.label_forShowNameAccount.setText(self.accountName)

    def ReshowAccountName(self):
        self.label_forShowNameAccount.setText(self.accountName )
        self.timerForShowPasswordInvalid.stop()

    def ShowPasswordInvalidNotify(self):
        self.label_forShowNameAccount.setText("MẬT KHẨU KHÔNG ĐÚNG ")
        self.lineEdit_forInputPassword.clear()
        self.timerForShowPasswordInvalid.start(1500)
