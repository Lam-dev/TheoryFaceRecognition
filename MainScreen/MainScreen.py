from        MainScreen.MainScreenUi    import Ui_Frame_MainScreen
from        MainScreen.WaitForUpdateAction   import WaitForUpdateScreen
from        PyQt5.QtCore    import pyqtSlot, pyqtSignal,QTimer, QDateTime,Qt, QObject
from        PyQt5.QtGui     import QPixmap
from        PyQt5           import QtWidgets, QtGui, QtCore
from        PIL             import Image, ImageQt
import      io
from        datetime        import datetime
import      pytz
from    UpdateScreen.UpdateScreen               import UpdateScreen
from    Outdoor.OutDoor                         import OutDoor
from    SettingScreen.SettingScreen             import SettingScreen
from    SettingScreen.DatabaseManagerScreen     import DatabaseManagerScreen
from    KeyBoard.KeyBoard                       import KeyBoard
from    SettingScreen.HideSettingScreenAction   import HideSettingScreen
from    CheckVersionScreen.CheckVersion         import CheckUpdate
from    GetSettingFromJSON    import GetSetting 

try:
    NAME_SETTING_DICT = GetSetting.GetPersionalSetting()
    NAME_CENTER = NAME_SETTING_DICT["scName"]
    NAME_DEVICE = NAME_SETTING_DICT["cenName"]
except:
    NAME_CENTER = ""
    NAME_DEVICE = ""

class MainScreen(QObject, Ui_Frame_MainScreen):
    SignalGoToDesktop = pyqtSignal()
    SignalModifyFRthreshold = pyqtSignal(float)
    SignalModifyFaceMark = pyqtSignal(bool)
    SignalModifyImageQuality = pyqtSignal(int)
    SignalConnectNewServer = pyqtSignal(dict)
    SignalConnectNewFTPserver = pyqtSignal(dict)
    SignalSettingScreenHiden = pyqtSignal()
    SignalAddFaceEncodeAndFGP  = pyqtSignal(dict, dict)
    SignalDeleteFaceAdded = pyqtSignal(int)
    SignalDeleteFGPadded = pyqtSignal(int)
    SignalCleanFGPsensor = pyqtSignal()
    SignalShutdown = pyqtSignal()
    SignalCloseELT = pyqtSignal()
    SignalDeleteAllData = pyqtSignal()

    def __init__(self, MainWindow):
        QObject.__init__(self)
        Ui_Frame_MainScreen.__init__(self)
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.WindowModal)
        MainWindow.resize(800, 480)
        MainWindow.setMinimumSize(QtCore.QSize(800, 480))
        MainWindow.setMaximumSize(QtCore.QSize(800, 480))

        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.centralWidget.setGeometry(QtCore.QRect(0, 0, 800, 480))

        self.centralFrame = QtWidgets.QFrame(self.centralWidget)
        self.__keyBoardOpened = False
        
        self.setupUi(self.centralFrame)
        # self.label_logoEcotek.setPixmap(QtGui.QPixmap("icon/logo_.png"))
        self.pixmapNoCamera = QtGui.QPixmap("icon/noCamera.png")
        self.pixmapEyeIcon = QtGui.QPixmap("icon/iconEye.png")
        self.pixmapOkIcon = QtGui.QPixmap("icon/iconOk.png")
        self.pixmapFailIcon = QtGui.QPixmap("icon/iconFail.png")
        self.pixmapWarningIcon = QtGui.QPixmap("icon/iconWarning.png")
        self.pixmapNotRecognized = QtGui.QPixmap("icon/iconImageRepresent.png")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/settingIcon40.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_shutdown.setIcon(icon)
        self.label_7.setPixmap(QtGui.QPixmap("icon/iconEcotek.png"))
        self.label_regisImage.setPixmap(QtGui.QPixmap("icon/iconImageRepresent.png"))
        self.label_7.mouseDoubleClickEvent = lambda event: self.__OpenOutdoor()
        self.timerFlickerWarning = QTimer(self)
        self.timerFlickerWarning.timeout.connect(self.__FlickerWarning)
        self.iconFaceRecognized = QtGui.QPixmap("icon/iconFaceRecognized.png")
        self.iconFGPrecognized = QtGui.QPixmap("icon/iconFingerprintRecognitzed.png")
        self.iconCardRecognized = QtGui.QPixmap("icon/cardIcon100.png")
        self.label_cty.setText(self.__ConvertStringToUTF8String(NAME_CENTER))
        self.label_cty_2.setText(self.__ConvertStringToUTF8String(NAME_DEVICE))

    def HideCamera(self, faceRecognized = "face"):
        self.label_showCamera.hide()
        if(faceRecognized == "face"):
            self.label_forShowIconFaceRecognized.setPixmap(self.iconFaceRecognized)
        elif(faceRecognized == "fgp"):
            self.label_forShowIconFaceRecognized.setPixmap(self.iconFGPrecognized)
        else:
            self.label_forShowIconFaceRecognized.setPixmap(self.iconCardRecognized)
        # named_tuple = time.localtime()
        # time_string = time.strftime("%m/%d/%Y \n %H:%M:%S", named_tuple)
        tz_HCM = pytz.timezone('Asia/Ho_Chi_Minh') 
        datetime_HCM = datetime.now(tz_HCM)
        time_string = datetime_HCM.strftime("%d/%m/%Y \n %H:%M:%S")
        self.label_forShowTimeRecognized.setText(time_string)
    
    def ShowCamera(self):
        self.label_showCamera.raise_()
        self.label_showCamera.show()


    def __OpenOutdoor(self):
        self.outdoorScreenShadow = QtWidgets.QFrame(self.centralWidget)
        self.outdoorScreenShadow.setGeometry(QtCore.QRect(0, 0, 800, 480))
        self.outdoorScreenShadow.setStyleSheet("background-color: rgba(0, 0, 0, 100);")
        self.frameContainOutdoor = QtWidgets.QFrame(self.outdoorScreenShadow)
        self.outdoorObj = OutDoor(self.frameContainOutdoor)
        self.outdoorScreenShadow.raise_()
        self.outdoorScreenShadow.show()
        self.outdoorObj.SignalHideExitScreen.connect(self.__HideOutdoorScreen)
        self.outdoorObj.SignalGoToDesktop.connect(self.__GoToDesktop)

    def __ShowWaitToSync(self):
        self.waitShadow = QtWidgets.QFrame(self.centralWidget)
        self.waitShadow.setGeometry(QtCore.QRect(0, 0, 800, 480))
        self.waitShadow.setStyleSheet("background-color: rgba(0, 0, 0, 100);")
        self.frameContainWait = QtWidgets.QFrame(self.waitShadow)

    def ShowWaitForUpdateScreen(self):
        self.waitForUpdateShadow = QtWidgets.QFrame(self.centralWidget)
        self.waitForUpdateShadow.setGeometry(QtCore.QRect(0, 0, 800, 480))
        self.waitForUpdateShadow.setStyleSheet("background-color: rgba(0, 0, 0, 100);")
        self.frameContainWaitForUpdateScreen = QtWidgets.QFrame(self.waitForUpdateShadow)
        self.waitForUpdateScreenObj = WaitForUpdateScreen(self.frameContainWaitForUpdateScreen)
        self.waitForUpdateShadow .raise_()
        self.waitForUpdateShadow.show()

    def HideWaitForUpdateScreen(self):
        self.waitForUpdateScreenObj.deleteLater()
        self.waitForUpdateShadow.hide()
        self.waitForUpdateShadow.deleteLater()

    def __GoToDesktop(self):
        self.SignalGoToDesktop.emit()
        
    def __HideOutdoorScreen(self):
        self.outdoorScreenShadow.hide()
        self.outdoorScreenShadow.deleteLater()

    def ShowNotConnect(self):
        self.label_showConnectOrDisconnect.setStyleSheet("background-color: rgb(170, 0, 0);")
        self.FlagSocketConnected = False
        try:
            self.settingScreenObj.ShowConnectStatusToSettingScreen("Đang kết nối ...", False)
        except:
            pass

    def ShowConnected(self):
        self.FlagSocketConnected = True
        try:
            self.settingScreenObj.ShowConnectStatusToSettingScreen("Đã kết nối", True)
        except:
            pass
        self.label_showConnectOrDisconnect.setStyleSheet("background-color: rgb(0, 170, 0);")

    def ShowFTPserverConnectAvailabel(self, connectAvailable):
        try:
            if(connectAvailable):
                self.settingScreenObj.ShowConnectFTPserverStatusToSettingScreen("Máy chủ đang hoạt động", True)
            else:
                self.settingScreenObj.ShowConnectFTPserverStatusToSettingScreen("Máy chủ không hoạt động", False)
        except:
            pass

    def ShowCanNotConnectCamera(self):
        self.label_showCamera.setPixmap(self.pixmapNoCamera)

    def __FlickerWarning(self):
        if(self.label_textWarning.isHidden()):
            self.label_textWarning.show()
        else:
            self.label_textWarning.hide()

    def ShowStudentInfomation(self, student):
        try:
            image = Image.open(io.BytesIO(student.AnhDangKy))
            # im_data = ImageQt._toqclass_helper(image)
            # pixmap = QPixmap(im_data['im'].size[0], im_data['im'].size[1])
            # resizeImage = pixmap.scaled(150, 250, QtCore.Qt.KeepAspectRatio)
            # self.label_regisImage.setPixmap(resizeImage)
            # self.label_forShowName.setText(student.HoVaTen)
            #self.label_forShowNumberCard.setText(student.SBD)
            qim = ImageQt.ImageQt(image)
            pix = QtGui.QPixmap.fromImage(qim)
            resizePixmap = pix.scaled(150, 200, QtCore.Qt.KeepAspectRatio)
            self.SetGeometryForLabelShowRegisImage(resizePixmap.width(), resizePixmap.height())
            self.label_regisImage.setPixmap(resizePixmap)
        except:
            pass

        self.label_forShowName.setText(student.HoVaTen.upper())
        self.label_forShowNumberCard.setText(student.SoCMTND)
        self.label_dateOfBird.setText(student.NgaySinh)
        self.label_forShowIdentNumber.setText(student.SBD)
    
    def ClearStudentRecognizedInfomation(self):
        self.label_regisImage.setPixmap(self.pixmapNotRecognized)
        self.label_forShowName.setText("Chưa nhận được thí sinh")
        self.label_forShowNumberCard.setText("")
        self.label_forShowIdentNumber.setText("")
        self.label_dateOfBird.setText("")

    def SetGeometryForLabelShowCamera(self, cameraWidth, cameraHeight):
        x = (self.frame_containLabelShowCamera.width() - cameraWidth)/2
        y = (self.frame_containLabelShowCamera.height() - cameraHeight)/2
        self.label_showCamera.setGeometry(x, y, cameraWidth, cameraHeight)

    def SetGeometryForLabelShowRegisImage(self, regisImageWidth, regisImageHeight):
        x = (self.frame_containLabelShowRegisImage.width() - regisImageWidth)/2
        y = (self.frame_containLabelShowRegisImage.height() - regisImageHeight)/2
        self.label_regisImage.setGeometry(x, y, regisImageWidth, regisImageHeight)

    def ShowNotStudentInformation(self):
        self.label_iconWarning.setPixmap(self.pixmapWarningIcon)
        self.label_textWarning.setStyleSheet('color: rgb(160, 160, 0);\nfont: 75 bold 14pt "Ubuntu";')
        self.label_textWarning.setText("CHƯA NHẬN ĐƯỢC THÍ SINH \n TỪ MÁY CHỦ")

    def ShowWarningLookAtCamera(self):
        self.label_iconWarning.setPixmap(self.pixmapEyeIcon)
        self.label_textWarning.setStyleSheet('color: rgb(70, 70, 70);\nfont: 75 bold 14pt "Ubuntu";')
        self.label_textWarning.setText("VUI LÒNG NHÌN THẲNG VÀO CAMERA")
        # self.timerFlickerWarning.start(1000)

    def ShowFaceRecognizeOK(self):
        self.label_iconWarning.setPixmap(self.pixmapOkIcon)
        self.label_textWarning.setStyleSheet('color: rgb(0, 160, 0);\nfont: 75 bold 14pt "Ubuntu";')
        self.label_textWarning.setText("ĐÚNG THÍ SINH \nMỜI RA XE")

    def ShowFaceRecogntizeFail(self):
        self.label_iconWarning.setPixmap(self.pixmapFailIcon)
        self.label_textWarning.setStyleSheet('color: rgb(160, 0, 0);\nfont: 75 bold 14pt "Ubuntu";')
        self.label_textWarning.setText("KHÔNG NHẬN DIỆN ĐƯỢC THÍ SINH")

    def ShowUpdateScreen(self, filePath):
        self.updateSettingShadow = QtWidgets.QFrame(self.centralWidget)
        self.updateSettingShadow.setGeometry(QtCore.QRect(0, 0, 800, 480))
        self.updateSettingShadow.setStyleSheet("background-color: rgba(0, 0, 0, 100);")
        self.frameUpdateScreen = QtWidgets.QFrame(self.updateSettingShadow)
        self.updateScreenObj = UpdateScreen(self.frameUpdateScreen, filePath)
        self.updateSettingShadow.raise_()
        self.updateSettingShadow.show()
    
    def ShowSettingScreen(self):
        self.settingScreenShadow = QtWidgets.QFrame(self.centralWidget)
        self.settingScreenShadow.setGeometry(QtCore.QRect(0, 0, 800, 480))
        self.settingScreenShadow.setStyleSheet("background-color: rgba(0, 0, 0, 100);")
        self.settingScreenShadow.mousePressEvent = lambda event: self.__HideSettingScreen()
        self.frameContainUpdateScreen = QtWidgets.QFrame(self.settingScreenShadow)
        self.frameContainUpdateScreen.mousePressEvent = lambda event: self.__EventDontUse()
        self.settingScreenObj = SettingScreen(self.frameContainUpdateScreen)
        self.settingScreenObj.SignalModifyFaceMark.connect(self.__ModifyFaceMark)
        self.settingScreenObj.SignalModifyFRthreshold.connect(self.__ModifyFRthreadhold)
        self.settingScreenObj.SignalModifyImageQuality.connect(self.__SignalModifyImageQuality)
        self.settingScreenObj.RequestOpenKeyBoard.connect(self.__ShowKeyBoard)
        self.settingScreenObj.SignalConnectNewFTPserver.connect(self.SignalConnectNewFTPserver.emit)
        self.settingScreenObj.SignalConnectNewServer.connect(self.SignalConnectNewServer.emit)
        self.settingScreenObj.RequestOpenDatabaseScreen.connect(self.OpenDatabaseManagerScreen)
        self.settingScreenObj.SignalOpenHideSettingScreen.connect(self.OpenHideSettingScreen)
        self.settingScreenObj.SignalCleanFGPsensor.connect(self.SignalCleanFGPsensor.emit)
        self.settingScreenObj.SignalCheckVersion.connect(self.ShowVersionCheckScreen)
        self.settingScreenObj.SignalShutdown.connect(self.SignalShutdown.emit)
        self.settingScreenObj.SignalDeleteAllData.connect(self.SignalDeleteAllData.emit)

        self.settingScreenShadow.show()
        self.settingScreenShadow.raise_()
    
    def ShowVersionCheckScreen(self):
        
        self.checkVersionShadow = QtWidgets.QFrame(self.centralWidget)
        self.checkVersionShadow.setGeometry(QtCore.QRect(0, 0, 800, 480))
        self.checkVersionShadow.setStyleSheet("background-color: rgba(0, 0, 0, 100);")
        self.frameContainCheckVersionScreen = QtWidgets.QFrame(self.checkVersionShadow)
        self.checkVersionScreenObj = CheckUpdate(self.frameContainCheckVersionScreen)
        self.checkVersionScreenObj.SignalUpdateVersion.connect(self.SignalCloseELT.emit)
        self.checkVersionScreenObj.SignalRequestCloseScreen.connect(self.CloseCheckVersionScreen)
        self.checkVersionScreenObj.SignalServerSettingForDevice.connect(self.SaveAndChangeSetting)
        self.checkVersionShadow.raise_()
        self.checkVersionShadow.show()

    def SaveAndChangeSetting(self, settingDict):
        self.label_cty.setText(self.__ConvertStringToUTF8String(settingDict["scName"]))
        self.label_cty_2.setText(self.__ConvertStringToUTF8String(settingDict["cenName"]))

    def __ConvertStringToUTF8String(self, string):
        x = []
        for elem in string:
            x.append(ord(elem))
        return(bytes(x).decode("utf8", "ignore"))

    def CloseCheckVersionScreen(self):
        self.checkVersionShadow.hide()
        self.checkVersionShadow.deleteLater()
    
    def OpenHideSettingScreen(self):

        self.frameContainHideSettingScreen = QtWidgets.QFrame(self.centralWidget)
        self.frameContainHideSettingScreen.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.hideSettingScreenObj = HideSettingScreen(self.frameContainHideSettingScreen)
        self.frameContainHideSettingScreen.raise_()
        self.frameContainHideSettingScreen.show()


    def OpenDatabaseManagerScreen(self):
        self.frameContainDatabaseScreen = QtWidgets.QFrame(self.centralWidget)
        self.databaseScreenObj = DatabaseManagerScreen(self.frameContainDatabaseScreen)
        self.databaseScreenObj.SignalAddFaceEncodeAndFGP.connect(self.SignalAddFaceEncodeAndFGP.emit)
        self.databaseScreenObj.SignalCloseDatabaseScreen.connect(self.CloseDatabaseScreen)
        self.databaseScreenObj.SignalDeleteFaceAdded.connect(self.SignalDeleteFaceAdded.emit)
        self.databaseScreenObj.SignalDeleteFGPadded.connect(self.SignalDeleteFGPadded.emit)


        self.frameContainDatabaseScreen.show()
        self.frameContainDatabaseScreen.raise_()
        
        
    def CloseDatabaseScreen(self):
        self.frameContainDatabaseScreen.hide()
        self.frameContainDatabaseScreen.deleteLater()
        self.databaseScreenObj.deleteLater()

    def __EventDontUse(self):
        pass

    def __ShowKeyBoard(self, widgetTakeInput):
        if(not self.__keyBoardOpened):
            self.frameContainKeyBoard = QtWidgets.QFrame(self.centralWidget)
            self.frameContainKeyBoard.setGeometry(0, 0, 480, 220)
            self.keyBoardObject = KeyBoard(widgetTakeInput, self.frameContainKeyBoard)
            self.keyBoardObject.CloseKeyBoardSignal.connect(self.__CloseKeyBoard)
            self.__keyBoardOpened = True

    def __CloseKeyBoard(self):
        self.frameContainKeyBoard.deleteLater()
        self.keyBoardObject.deleteLater()
        self.__keyBoardOpened = False

    def __HideSettingScreen(self):
        self.settingScreenObj.SaveSetting()
        self.settingScreenShadow.hide()
        self.settingScreenShadow.deleteLater()
        self.settingScreenObj.deleteLater()
        self.SignalSettingScreenHiden.emit()

    def __ModifyFaceMark(self, mark):
        self.SignalModifyFaceMark.emit(mark)

    def __ModifyFRthreadhold(self, threshold):
        self.SignalModifyFRthreshold.emit(threshold)

    def __SignalModifyImageQuality(self, imageQuality):
        self.SignalModifyImageQuality.emit(imageQuality)

    def HideUpdateScreen(self):
        self.updateSettingShadow.hide()
        self.updateSettingShadow.deleteLater()

    def ShowNumberStudentParsed(self, number, all):
        self.updateScreenObj.ShowNumberUpdate(number, all)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame_MainScreen = QtWidgets.QFrame()
    ui = MainScreen(Frame_MainScreen)
    Frame_MainScreen.show()
    sys.exit(app.exec_())
