from    SettingScreen.SystemSettingContentUI import Ui_widget_containSettingContent
from    PyQt5.QtCore                        import pyqtSlot, pyqtSignal,QTimer, QDateTime, Qt, QObject, QPointF, QPropertyAnimation, pyqtProperty
from    PyQt5                               import QtWidgets
from    PyQt5                               import QtGui
from    GetSettingFromJSON                  import GetSetting, SaveSetting
from    GetCurrentIP.GetCurrentIP           import GetCurrentIp
import  json
import  socket
import  ftplib

class SystemSettingContent(Ui_widget_containSettingContent, QObject):
    GetTextFromKeyBoard = pyqtSignal(object)
    SignalModifyFRpoint = pyqtSignal(float)
    SignalModifyFaceMark = pyqtSignal(bool)
    SignalModifyImageQuality = pyqtSignal(float)
    SignalConnectNewServer = pyqtSignal(dict)
    SignalConnectNewFTPserver = pyqtSignal(dict)
    SignalCleanFGPsensor = pyqtSignal()
    SignalDeleteAllData = pyqtSignal()
    

    def __init__(self):
        QObject.__init__(self)
        Ui_widget_containSettingContent.__init__(self)
        self.scrollAreaContent = QtWidgets.QWidget()
        self.setupUi(self.scrollAreaContent)
        # self.comboBox_chooseTime.addItems(("15 phút", "30 Phút", "1 Giờ"))
        # self.lineEdit_forInputAccount.mouseReleaseEvent = lambda event: self.GetTextFromKeyBoard.emit(self.lineEdit_forInputAccount)
        # self.lineEdit_forInputFPTpassword.mouseReleaseEvent = lambda event: self.GetTextFromKeyBoard.emit(self.lineEdit_forInputFPTpassword)
        # self.lineEdit_forInputFTPaccount.mouseReleaseEvent = lambda event: self.GetTextFromKeyBoard.emit(self.lineEdit_forInputFTPaccount)
        # self.lineEdit_forInputFTPIP.mouseReleaseEvent = lambda event: self.GetTextFromKeyBoard.emit(self.lineEdit_forInputFTPIP)
        # self.lineEdit_forInputFTPport.mouseReleaseEvent = lambda event: self.GetTextFromKeyBoard.emit(self.lineEdit_forInputFTPport)
        self.lineEdit_forInputIP.mouseReleaseEvent = lambda event: self.GetTextFromKeyBoard.emit(self.lineEdit_forInputIP)
        # self.lineEdit_forInputPassword.mouseReleaseEvent = lambda event: self.GetTextFromKeyBoard.emit(self.lineEdit_forInputPassword)
        self.lineEdit_forInputPort.mouseReleaseEvent = lambda event: self.GetTextFromKeyBoard.emit(self.lineEdit_forInputPort)
        self.lineEdit_forInputIP_DT.mouseReleaseEvent = lambda event: self.GetTextFromKeyBoard.emit(self.lineEdit_forInputIP_DT)
        self.lineEdit_forInputPort_DT.mouseReleaseEvent = lambda event: self.GetTextFromKeyBoard.emit(self.lineEdit_forInputPort_DT)
        # self.GetTextFromKeyBoard.emit(self.lineEdit_forInputAccount)
        # self.comboBox_forChooseFaceMark.currentIndexChanged.connect(self.ChangeFaceYesOrNoFaceMark)
        # self.comboBox_forChooseFRPoint.currentIndexChanged.connect(self.ChangeFRpoint)
        # self.comboBox_forChooserImageQuality.currentIndexChanged.connect(self.ChangedImageQuality)
        self.checkFailPixmap = QtGui.QPixmap("icon/iconCheckFail.png")
        self.checkOKpixmap = QtGui.QPixmap("icon/iconCheckOk.png")
        self.label_iconSocketStatus.setPixmap(QtGui.QPixmap("icon/iconConnected.png"))
        self.lineEdit_forInputIP.textChanged.connect(lambda:self.__CheckIPrule(self.lineEdit_forInputIP.text(), self.label_iconCheckServerIP))
        self.lineEdit_forInputPort.textChanged.connect(lambda:self.__CheckPortRule(self.lineEdit_forInputPort.text(), self.label_iconCheckServerPort))
        self.lineEdit_forInputIP_DT.textChanged.connect(lambda:self.__CheckIPrule(self.lineEdit_forInputIP_DT.text(), self.label_iconCheckServerIP_DT))
        self.lineEdit_forInputPort_DT.textChanged.connect(lambda:self.__CheckPortRule(self.lineEdit_forInputPort_DT.text(), self.label_iconCheckServerPort_DT))
        # self.lineEdit_forInputAccount.textChanged.connect(lambda:self.__CheckAccount(self.lineEdit_forInputAccount.text(), self.label_iconCheckServerAccount))
        # self.lineEdit_forInputPassword.textChanged.connect(lambda:self.__CheckPassword(self.lineEdit_forInputPassword.text(), self.label_iconCheckServerPassword))
        # self.lineEdit_forInputFTPIP.textChanged.connect(lambda:self.__CheckIPrule(self.lineEdit_forInputFTPIP.text(), self.label_iconCheckFTPip))
        # self.lineEdit_forInputFTPport.textChanged.connect(lambda:self.__CheckPortRule(self.lineEdit_forInputFTPport.text(), self.label_iconCheckFTPport))
        # self.lineEdit_forInputFTPaccount.textChanged.connect(lambda:self.__CheckAccount(self.lineEdit_forInputFTPaccount.text(), self.label_iconCheckFTPaccount))
        # self.lineEdit_forInputFPTpassword.textChanged.connect(lambda:self.__CheckPassword(self.lineEdit_forInputFPTpassword.text(), self.label_iconCheckFTPpassword))
        self.pushButton_connectNewServer.clicked.connect(self.__ConnectNewServer)
        # self.pushButton_connectNewFTP.clicked.connect(self.__ConnectNewFTPserver)
        # self.pushButton_cleanFGPsensor.clicked.connect(self.SignalCleanFGPsensor.emit)
        self.pushButton_deleteAllData.clicked.connect(self.SignalDeleteAllData.emit)
        self.pushButton_connectNewServer_DT.clicked.connect(self.CheckConnectDTdesktop)
        self.GetAndShowSetting()
        self.__GetAndShowCurrentVersion()

    def CheckConnectDTdesktop(self):
        try:
            self.clientObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.clientObj.setblocking(1)
            self.clientObj.settimeout(2)
            self.clientObj.connect((self.lineEdit_forInputIP_DT.text(), int(self.lineEdit_forInputPort_DT.text())))
            self.label_showSocketConnectStatus_DT.setText("Máy chủ đang hoạt động")
            self.clientObj.shutdown(1)
            self.clientObj.close()
        except Exception as ex:
            self.label_showSocketConnectStatus_DT.setText(str(ex.args))

        try:
            self.ftpObj = ftplib.FTP(host = self.lineEdit_forInputIP_DT.text(), timeout = 1)
            self.ftpObj.timeout = 1
            self.ftpObj.login("ELT", "1")
            self.label_showFTPconnectStatus_DT.setText("Máy chủ FTP đang hoạt động")
            self.ftpObj.close()
        except Exception as ex:
            self.label_showFTPconnectStatus_DT.setText(str(ex.args))


    def ShowCurentIP(self):
        getCrIpObj = GetCurrentIp()
        crIP = getCrIpObj.GetIP()
        if(crIP["privateIP"] != False):
            self.label_currentIP.setText(crIP["privateIP"])
        else:
            self.label_currentIP.setText("CHƯA NHẬN ĐƯỢC IP")
        
        if(crIP["subnetMask"] != False):
            self.label_currentIP.setText(crIP["subnetMask"])
        else:
            self.label_currentIP.setText("CHƯA NHẬN ĐƯỢC IP")

        if(crIP["gateway"] != False):
            self.label_currentIP.setText(crIP["privateIP"])
        else:
            self.label_currentIP.setText("CHƯA NHẬN ĐƯỢC IP")


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
            "serverAccount" : "",
            "serverPassword" : ""
        }
        self.SignalConnectNewServer.emit(serverInfoDict)

    def __ConnectNewFTPserver(self):
        
        FTPserverDict = {
            "ftpIP" : self.lineEdit_forInputIP.text(),
            "ftpPort" : self.lineEdit_forInputPort.text(),
            "ftpAccount" : "ecotek",
            "ftpPassword" : "Ecotek@123"
        }
        self.SignalConnectNewFTPserver.emit(FTPserverDict)

    def __ConnectNewFTPserver(self):
        pass

    def GetAndShowSetting(self):
        
        settingDict = GetSetting.GetSystemSetting()
        if(type(settingDict) is  bool):
            return
        try:
            # self.comboBox_chooseTime.setCurrentIndex(int(settingDict["autoShutdown"]))
            self.lineEdit_forInputIP.setText(settingDict["serverIP"])
            self.lineEdit_forInputPort.setText(settingDict["serverPort"])
            self.lineEdit_forInputIP_DT.setText(settingDict["serverIP_DT"])
            self.lineEdit_forInputPort_DT.setText(settingDict["serverPort_DT"])
            
            # self.lineEdit_forInputAccount.setText(settingDict["serverAccount"])
            # self.lineEdit_forInputPassword.setText(settingDict["serverPassword"])

            # self.lineEdit_forInputFTPIP.setText(settingDict["ftpIP"])
            # self.lineEdit_forInputFTPport.setText(settingDict["ftpPort"])
            # self.lineEdit_forInputFTPaccount.setText(settingDict["ftpAccount"])
            # self.lineEdit_forInputFPTpassword.setText(settingDict["ftpPassword"])

            # self.comboBox_forChooseFRPoint.setCurrentIndex(settingDict["FRthreshold"])
            # self.comboBox_forChooserImageQuality.setCurrentIndex(settingDict["imageQuality"])
            # self.comboBox_forChooseFaceMark.setCurrentIndex(settingDict["faceMark"])
        except:
            pass
        
    def SaveSetting(self):
        settingDict = {
            # "autoShutdown" : self.comboBox_chooseTime.currentIndex(),
            "serverIP"     : self.lineEdit_forInputIP.text(),
            "serverPort"   : self.lineEdit_forInputPort.text(),
            "serverAccount" : "",
            "serverPassword" : "",
            "ftpIP" : self.lineEdit_forInputIP.text(),
            "ftpPort" : 21,
            "ftpAccount" : "ecotek",
            "ftpPassword" : "Ecotek@123",

            "serverIP_DT" : self.lineEdit_forInputIP_DT.text(), 
            "serverPort_DT":self.lineEdit_forInputPort_DT.text(),
            "serverAccount_DT":"",
            "serverPassword_DT" : "",
            "ftpIP_DT" : self.lineEdit_forInputIP_DT.text(),
            "ftpPort_DT" : 21,
            "ftpAccount_DT" : "ELT",
            "ftpPassword_DT" : "1",


            # "FRthreshold" : self.comboBox_forChooseFRPoint.currentIndex(),
            # "imageQuality" : self.comboBox_forChooserImageQuality.currentIndex(),
            # "faceMark":self.comboBox_forChooseFaceMark.currentIndex()
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
    
    def GetWidgetContent(self):
        return self.scrollAreaContent