from        CheckVersionScreen.CheckVersionUi    import Ui_Frame
from        PyQt5.QtCore    import pyqtSlot, pyqtSignal,QTimer, QDateTime,Qt, QObject
from        PyQt5.QtGui     import QPixmap
from        PyQt5           import QtWidgets, QtGui, QtCore
from        PIL             import Image, ImageQt
from        CheckVersionScreen.SocketClientEcotekServer   import SocketClient
import      json

class CheckUpdate(QObject, Ui_Frame):
    SignalRequestCloseScreen = pyqtSignal()
    SignalUpdateVersion = pyqtSignal()

    def __init__(self, Frame):
        QObject.__init__(self)
        Ui_Frame.__init__(self)
        self.setupUi(Frame)
        Frame.setGeometry((800-Frame.width())/2, (480-Frame.height())/2, Frame.width(), Frame.height())
        self.label_iconConnecting.setPixmap(QtGui.QPixmap("icon/connectIcon50.png"))
        self.pushButton_cancelCheck.clicked.connect(self.CloseCheckUpdateScreen)
        self.pushButton_cancelUpdated.clicked.connect(self.CloseCheckUpdateScreen)
        self.pushButton_update.clicked.connect(self.UpdateNewVersion)
        self.frameDetectNewVersion.hide()
        self.ConnectServerAndGetVersion()
        self.currentVersion = self.GetCurrentVersion()
        self.newVersionInfo = object

#region hien thi cac man hinh
    def ShowConnectNotify(self):
        self.frameNotNewVersion.hide()
        self.frame_containConnectingNotify.show()
        self.frameDetectNewVersion.hide()

    def ShowNotNewVersion(self):
        self.frameNotNewVersion.show()
        self.frame_containConnectingNotify.hide()
        self.frameDetectNewVersion.hide()
    
    def ShowNewVersion(self, version):
        self.label_forShowNewVersion.setText(version)
        self.frameNotNewVersion.hide()
        self.frame_containConnectingNotify.hide()
        self.frameDetectNewVersion.show()
#endregion
    
    def UpdateNewVersion(self):
        with open('update.json', 'w') as json_file:
            json.dump(self.newVersionInfo, json_file)
        self.SignalUpdateVersion.emit()

    def CloseCheckUpdateScreen(self):
        self.socketObj.CloseSocket()
        self.SignalRequestCloseScreen.emit()

    def ConnectServerAndGetVersion(self):
        self.ShowConnectNotify()
        self.socketObj = SocketClient()
        self.socketObj.SignalServerRequestCloneApp.connect(self.ReciptVersionInfoFromServer)
        self.socketObj.SendRequestCloneData()

    def GetCurrentVersion(self):
        try:
            with open('version.json') as json_file:
                return json.load(json_file)["crVer"]
        except:
            return ""

    def ReciptVersionInfoFromServer(self, dataObj):
        if(dataObj.ver != self.currentVersion):
            self.ShowNewVersion(dataObj.ver)
            self.newVersionInfo = dataObj


    def ShowNewVersionReady(self):
        self.frameDetectNewVersion.show()
        

# Mesage = {
#         “ver”: name of tag version
#         “ID”: commit ID
#         “hardReset”: hard reset (bool)
#         “delReclone”: (bool)
# }