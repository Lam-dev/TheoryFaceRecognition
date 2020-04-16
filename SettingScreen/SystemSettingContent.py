from SettingScreen.SystemSettingContentUI import Ui_widget_containSettingContent
from PyQt5.QtCore import pyqtSlot, pyqtSignal,QTimer, QDateTime, Qt, QObject, QPointF, QPropertyAnimation, pyqtProperty
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from GetSettingFromJSON   import GetSetting, SaveSetting
import json

class SystemSettingContent(Ui_widget_containSettingContent, QObject):
    GetTextFromKeyBoard = pyqtSignal(object)
    SignalModifyFRpoint = pyqtSignal(float)
    SignalModifyFaceMark = pyqtSignal(bool)
    SignalModifyImageQuality = pyqtSignal(float)
    SignalConnectNewServer = pyqtSignal(dict)
    SignalConnectNewFTPserver = pyqtSignal(dict)
    SignalCleanFGPsensor = pyqtSignal()
    SignalDeleteAllData = pyqtSignal()
    SignalModifyFGPsecurityLevel = pyqtSignal(int)
    

    def __init__(self):
        QObject.__init__(self)
        Ui_widget_containSettingContent.__init__(self)
        self.scrollAreaContent = QtWidgets.QWidget()
        self.setupUi(self.scrollAreaContent)

        self.lineEdit_forInputIP.mouseReleaseEvent = lambda event: self.GetTextFromKeyBoard.emit(self.lineEdit_forInputIP)
        self.lineEdit_forInputPort.mouseReleaseEvent = lambda event: self.GetTextFromKeyBoard.emit(self.lineEdit_forInputPort)

        # self.comboBox_forChooseFRPoint.currentIndexChanged.connect(self.ChangeFRpoint)
        # self.comboBox_forChoseFGPscuLevel.currentIndexChanged.connect(self.ChangeSecurityLevel)
        self.checkFailPixmap = QtGui.QPixmap("icon/iconCheckFail.png")
        self.checkOKpixmap = QtGui.QPixmap("icon/iconCheckOk.png")
        self.label_iconSocketStatus.setPixmap(QtGui.QPixmap("icon/iconConnected.png"))
        self.lineEdit_forInputIP.textChanged.connect(lambda:self.__CheckIPrule(self.lineEdit_forInputIP.text(), self.label_iconCheckServerIP))
        self.lineEdit_forInputPort.textChanged.connect(lambda:self.__CheckPortRule(self.lineEdit_forInputPort.text(), self.label_iconCheckServerPort))

        self.pushButton_connectNewServer.clicked.connect(self.__ConnectNewServer)


        self.pushButton_deleteAllData.clicked.connect(self.SignalDeleteAllData.emit)
        self.GetAndShowSetting()
        self.__GetAndShowCurrentVersion()

    def __GetAndShowCurrentVersion(self):
        try:
            with open("version.json", "r") as fp:
                versionDict = json.load(fp)
                self.label_forShowFirmwareVersion.setText(versionDict["crVer"])
        except:
            self.label_forShowFirmwareVersion.setText("v0.0.0")
        
    def __ConnectNewServer(self):
        
        serverInfoDict  ={
            "serverIP"     : self.lineEdit_forInputIP.text(),
            "serverPort"   : self.lineEdit_forInputPort.text(),
        }
        self.SignalConnectNewServer.emit(serverInfoDict)

        self.__ConnectNewFTPserver()

    def __ConnectNewFTPserver(self):
        
        FTPserverDict = {
            "ftpIP" : self.lineEdit_forInputIP.text(),
            "ftpPort" : 21,
            "ftpAccount" : "ecotek",
            "ftpPassword" : "Ecotek@123"
        }
        self.SignalConnectNewFTPserver.emit(FTPserverDict)

    def GetAndShowSetting(self):
        
        settingDict = GetSetting.GetSystemSetting()
        if(type(settingDict) is  bool):
            return
        try:
            # self.comboBox_chooseTime.setCurrentIndex(int(settingDict["autoShutdown"]))
            self.lineEdit_forInputIP.setText(settingDict["serverIP"])
            self.lineEdit_forInputPort.setText(settingDict["serverPort"])
            # self.lineEdit_forInputAccount.setText(settingDict["serverAccount"])
            # self.lineEdit_forInputPassword.setText(settingDict["serverPassword"])

            # self.lineEdit_forInputFTPIP.setText(settingDict["ftpIP"])
            # self.lineEdit_forInputFTPport.setText(settingDict["ftpPort"])
            # self.lineEdit_forInputFTPaccount.setText(settingDict["ftpAccount"])
            # self.lineEdit_forInputFPTpassword.setText(settingDict["ftpPassword"])

            # self.comboBox_forChooseFRPoint.setCurrentIndex(settingDict["FRthreshold"])
            # self.comboBox_forChooserImageQuality.setCurrentIndex(settingDict["imageQuality"])
            # self.comboBox_forChooseFaceMark.setCurrentIndex(settingDict["faceMark"])

            # self.comboBox_forChoseFGPscuLevel.setCurrentIndex(settingDict["FGPscuLevel"])
        except:
            pass
        
    def SaveSetting(self):
        settingDict = {
            # "autoShutdown" : self.comboBox_chooseTime.currentIndex(),
            "serverIP"     : self.lineEdit_forInputIP.text(),
            "serverPort"   : self.lineEdit_forInputPort.text(),
            # "serverAccount" : self.lineEdit_forInputAccount.text(),
            # "serverPassword" : self.lineEdit_forInputPassword.text(),
            "ftpIP" : self.lineEdit_forInputIP.text(),
            "ftpPort" : 21,
            "ftpAccount" : "ecotek",
            "ftpPassword" : "Ecotek@123",
            # "FRthreshold" : self.comboBox_forChooseFRPoint.currentIndex(),
            # "imageQuality" : self.comboBox_forChooserImageQuality.currentIndex(),
            # "faceMark":self.comboBox_forChooseFaceMark.currentIndex(),
            # "FGPscuLevel":self.comboBox_forChoseFGPscuLevel.currentIndex()
        }
        SaveSetting.SaveSystemSetting(settingDict)

    def __CheckIPrule(self, ipText, labelForShowIcon):
        try:
            ipArr = ipText.split(".")
            if(len(ipArr) == 4):
                for number in ipArr:
                    if(not self.__CheckNumberRule(number)):
                        labelForShowIcon.setPixmap(self.checkFailPixmap)
                        return
                labelForShowIcon.setPixmap(self.checkOKpixmap)
                
            else:
                labelForShowIcon.setPixmap(self.checkFailPixmap)
        except:
            labelForShowIcon.setPixmap(self.checkFailPixmap)

    def __CheckPortRule(self, portText, labelForShowIcon):
        try:
            portNumber = int(portText)
            if((portNumber >= 0) & (portNumber <= 65535)):
                labelForShowIcon.setPixmap(self.checkOKpixmap)
            else:
                labelForShowIcon.setPixmap(self.checkFailPixmap)
        except:
            labelForShowIcon.setPixmap(self.checkFailPixmap)
    
    def __CheckAccount(self, accountText, labelForShowIcon): 

        if((accountText.__contains__(" "))|(accountText.__len__() == 0)):
            labelForShowIcon.setPixmap(self.checkFailPixmap)
        else:
            labelForShowIcon.setPixmap(self.checkOKpixmap)

    def __CheckPassword(self, password, labelForShowIcon): 
        if((password.__contains__(" ")) | (password.__len__() == 0)):
            labelForShowIcon.setPixmap(self.checkFailPixmap)
        else:
            labelForShowIcon.setPixmap(self.checkOKpixmap)

    def __CheckNumberRule(self, numberText):
        try:
            intNumber = int(numberText)
            if((intNumber >= 0) & (intNumber <= 255)):
                return True
            else:
                return False
        except:
            return False

    def ChangedImageQuality(self):
        text = self.comboBox_forChooserImageQuality.currentText()
        if(text == "1"):
            self.SignalModifyImageQuality.emit(1)
        elif(text == "2"):
            self.SignalModifyImageQuality.emit(2)
        elif(text == "3"):
            self.SignalModifyImageQuality.emit(3)
        elif(text == "4"):
            self.SignalModifyImageQuality.emit(4)
        elif(text == "5"):
            self.SignalModifyImageQuality.emit(5)
        elif(text == "6"):
            self.SignalModifyImageQuality.emit(6)


    def ChangeFaceYesOrNoFaceMark(self):
        text = self.comboBox_forChooseFaceMark.currentText()
        if(text == "Có"):
            self.SignalModifyFaceMark.emit(True)
        else:
            self.SignalModifyFaceMark.emit(False)

    def ChangeFRpoint(self):
        text = self.comboBox_forChooseFRPoint.currentText()
        if(text == "1"):
            self.SignalModifyFRpoint.emit(0.65)
        elif(text == "2"):
            self.SignalModifyFRpoint.emit(0.6)
        elif(text == "3"):
            self.SignalModifyFRpoint.emit(0.55)
        elif(text == "4"):
            self.SignalModifyFRpoint.emit(0.5)
        elif(text == "5"):
            self.SignalModifyFRpoint.emit(0.45)
        elif(text == "6"):
            self.SignalModifyFRpoint.emit(0.4)
    
    def ChangeSecurityLevel(self):
        text = self.comboBox_forChoseFGPscuLevel.currentText()
        if(text == "1"):
            self.SignalModifyFGPsecurityLevel.emit(1)
        elif(text == "2"):
            self.SignalModifyFGPsecurityLevel.emit(2)
        elif(text == "3"):
            self.SignalModifyFGPsecurityLevel.emit(3)
        elif(text == "4"):
            self.SignalModifyFGPsecurityLevel.emit(4)
        elif(text == "5"):
            self.SignalModifyFGPsecurityLevel.emit(5)
        elif(text == "6"):
            self.SignalModifyFGPsecurityLevel.emit(5)

    def GetWidgetContent(self):
        return self.scrollAreaContent