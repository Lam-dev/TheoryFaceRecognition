from PyQt5                  import QtCore, QtGui, QtWidgets
from PyQt5                  import QtCore, QtGui, QtWidgets
from PyQt5.QtGui            import QIcon, QPixmap
from PyQt5.QtCore           import pyqtSlot, pyqtSignal,QTimer, QDateTime, Qt, QObject, QPointF, QPropertyAnimation, pyqtProperty
from SettingScreen.HideSettingScreenUI    import Ui_Frame_containHideSettingScreen
from SettingScreen.DialogInputPassword    import DialogInputPassword
from DatabaseAccess.DatabaseAccess    import *

class HideSettingScreen(Ui_Frame_containHideSettingScreen, QObject):

    def __init__(self, frameContain):
        Ui_Frame_containHideSettingScreen.__init__(self)
        QObject.__init__(self)
        self.setupUi(frameContain)
        self.GetListAdminAccount()
        self.frameContain = frameContain
        self.listWidget_showListAdminAccount.currentRowChanged.connect(self.ChoseAccount)
        
    def GetListAdminAccount(self):
        adminAndPasswordRepo = TaiKhoanQuanLyRepository()
        self.listWidget_showListAdminAccount.clear()
        self.lstAdminAndPassword = adminAndPasswordRepo.layDanhSach(" 1 = 1 ")
        for adminAndPassword in self.lstAdminAndPassword:
            item =QtWidgets.QListWidgetItem()
            item.setText(adminAndPassword.TaiKhoan)
            self.listWidget_showListAdminAccount.addItem(item) 

    def ChoseAccount(self):
        rowChose = self.listWidget_showListAdminAccount.currentRow()        
        self.dialogScreenShadow = QtWidgets.QFrame(self.frameContain)
        self.dialogScreenShadow.setGeometry(QtCore.QRect(0, 0, 800, 480))
        self.dialogScreenShadow.setStyleSheet("background-color: rgba(0, 0, 0, 100);")
        self.frameContainDialog = QtWidgets.QFrame(self.dialogScreenShadow)
        self.dialogObj = DialogInputPassword(self.frameContainDialog)
        # self.dialogObj.passwordForCompare = self.lstAdminAndPassword(rowChose)
        self.dialogObj.SetAccountAndPasswordForCheck(self.lstAdminAndPassword[rowChose])
        self.dialogScreenShadow.raise_()
        self.dialogScreenShadow.show()
        

