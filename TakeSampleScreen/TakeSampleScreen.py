from AddFace_DT.AddFaceAction                   import AddFaceScreen
from ShowInfomation.ShowInfomationAction        import ShowInfoScreen
from AddFGP_DT.AddFGPaction                     import AddFGPscreen 
from WriteRFcard.WriteRFcardScreenAction        import WriteRFcardAction
from PyQt5                                      import QtCore, QtGui
from PyQt5.QtCore                               import pyqtSlot, pyqtSignal,QTimer, QDateTime, Qt, QObject, QPointF, QPropertyAnimation, pyqtProperty, QSize
from PyQt5                                      import QtWidgets
from SocketConnectDT.SocketClientDT             import SocketClientDT
from TakeSampleScreen.TakeSampleScreenUI        import Ui_Frame

class TakeSampleScreen(QObject, Ui_Frame):
    SignalRequestGetFGP = pyqtSignal(object)
    SignalStartReadImage = pyqtSignal(object)
    SignalStopReadImage = pyqtSignal()
    SignalFaceTracking = pyqtSignal()
    SignalGetFaceFeature = pyqtSignal(object)
    SignalCloseTakeSampleScreen = pyqtSignal()
    
    SignalStartWriteRFcardDT = pyqtSignal(str, object)
    SignalStopWriteRFcardDT = pyqtSignal()
    CloseTakeSampleScreen = pyqtSignal()
    SignalStopGetFGP = pyqtSignal()

    def __init__(self, frame):
        QObject.__init__(self)
        Ui_Frame.__init__(self)
        self.setupUi(frame)
        icon = QtGui.QIcon()

        icon.addPixmap(QtGui.QPixmap("icon/closeIcon50.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)

        self.pushButton_exitexit.setIcon(icon)
        self.frameContain = QtWidgets.QFrame(frame)
        self.frameContain.setGeometry(QtCore.QRect(0, 50, 800, 429))
        self.frameContainShowInfo = QtWidgets.QFrame(self.frameContain)
        self.frameContainShowInfo.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.showInfoScreenObj = ShowInfoScreen(self.frameContainShowInfo)

        self.pushButton_exitexit.clicked.connect(self.CloseTakeSampleScreen)
        self.currentStep = 1
        self.nameStudentNeedAdd = ""

        self.frameContainAddFace = QtWidgets.QFrame(self.frameContain)
        self.frameContainAddFace.setGeometry(QtCore.QRect(self.frameContain.width(), 0, 0, 0))
        self.addFaceScreenObj = AddFaceScreen(self.frameContainAddFace)
        self.addFaceScreenObj.SignalStartReadImage.connect(self.SignalStartReadImage.emit)
        self.addFaceScreenObj.SignalStopReadImage.connect(self.SignalStopReadImage.emit)
        self.addFaceScreenObj.SignalFaceTracking.connect(self.SignalFaceTracking.emit)
        self.addFaceScreenObj.SignalGetFaceFeature.connect(self.SignalGetFaceFeature.emit)

        self.frameContainAddFGP = QtWidgets.QFrame(self.frameContain)
        self.frameContainAddFGP.setGeometry(QtCore.QRect(self.frameContain.width(), 0, 0, 0))
        self.addFGPscreenObj = AddFGPscreen(self.frameContainAddFGP)
        self.addFGPscreenObj.SignalRequestGetFGP.connect(self.SignalRequestGetFGP.emit)
        self.addFGPscreenObj.SignalStopGetFGP.connect(self.SignalStopGetFGP.emit)

        self.frameContainWriteRFcard = QtWidgets.QFrame(self.frameContain)
        self.frameContainWriteRFcard.setGeometry(QtCore.QRect(self.frameContain.width(), 0, 0, 0))
        self.writeRFcardObj = WriteRFcardAction(self.frameContainWriteRFcard)
        self.SignalWriteToRFcardSuccessfully = pyqtSignal()
        self.SignalStartWriteRFcard = pyqtSignal(str, object)
        self.SignalStopWriteRFcard = pyqtSignal()

        self.socketObj = SocketClientDT()
        self.socketObj.processReciptDataObj.SignalGoToAddFGP.connect(self.GoToAddFGPscreen)
        self.socketObj.processReciptDataObj.SignalGoToAddFace.connect(self.GoToAddFaceScreen)
        self.socketObj.processReciptDataObj.SignalShowInformation.connect(self.GoToShowInfomation)
        self.socketObj.SignalRequestWriteCard.connect(self.GoToWriteRFcardScreen)

        self.writeRFcardObj = WriteRFcardAction(self.frameContainWriteRFcard)
        self.writeRFcardObj.SignalStartWriteRFcardDT.connect(self.SignalStartWriteRFcardDT.emit)
        self.writeRFcardObj.SignalStopWriteRFcardDT.connect(self.SignalStopWriteRFcardDT.emit)
        self.writeRFcardObj.SignalWriteCardSuccess.connect(self.socketObj.SendNotifyWriteRFcardSuccessfully)

        self.addFGPscreenObj.SignalSendImageToServer.connect(self.socketObj.SendFingerImage)
        self.addFGPscreenObj.SignalSendFGPGetToServer.connect(self.socketObj.SendFingerFeature)
        # self.addFGPscreenObj.SignalPlayBip.connect(self.__PlayBip)

        self.addFaceScreenObj.SignalPictureTaked.connect(self.socketObj.SendTakedImage)
        self.currentStep = 1
        self.flagNoCameraMode = False

    
    def CloseTakeSampleScreen(self):
        self.socketObj.CloseConnect()
        self.socketObj.deleteLater()
        self.writeRFcardObj.StopWriteToCard()
        self.writeRFcardObj.deleteLater()
        self.addFGPscreenObj.StopAll()
        self.addFaceScreenObj.deleteLater()
        self.addFaceScreenObj.StopTakePicture()
        self.addFGPscreenObj.deleteLater()
        
        self.SignalCloseTakeSampleScreen.emit()
        

    def GoToWriteRFcardScreen(self, strMessage):
        try:
            self.writeRFcardObj.label_forShowName.setText(self.showInfoScreenObj.nameStudentNeedAdd)
            self.writeRFcardObj.WriteIDcardNumberToRFcard(strMessage)
        except:
            pass
        if(self.currentStep == 1):
            self.writeRFcardObj.ShowStepStudentInformationAnim(self.frameContainShowInfo)
            self.currentStep = 4

        elif(self.currentStep == 3):
            self.writeRFcardObj.ShowStepStudentInformationAnim(self.frameContainAddFace)
            self.currentStep = 4
            #self.addFaceScreenObj.cameraObj.StopReadImage()
            self.addFaceScreenObj.StopTakePicture()

        elif(self.currentStep == 2):
            self.writeRFcardObj.ShowStepStudentInformationAnim(self.frameContainAddFGP)
            self.addFGPscreenObj.StopAll()
            self.currentStep = 4

        elif(self.currentStep == 4):
            pass

        try:
            self.addFGPscreenObj.label_forShowName.setText(self.showInfoScreenObj.nameStudentNeedAdd)
        except:
            pass
    
    def GoToAddFGPscreen(self, strMessage):
        if(self.currentStep == 1):
            self.addFGPscreenObj.ShowStepStudentInformationAnim(self.frameContainShowInfo)
            self.currentStep = 2
            self.addFGPscreenObj.ListFingerNeedAdd(strMessage)
            self.addFGPscreenObj.GetFGP()

        elif(self.currentStep == 3):
            self.addFGPscreenObj.ShowStepStudentInformationAnim(self.frameContainAddFace)
            self.currentStep = 2
            #self.addFaceScreenObj.cameraObj.StopReadImage()
            self.addFaceScreenObj.StopTakePicture()
            self.addFGPscreenObj.ListFingerNeedAdd(strMessage)
            self.addFGPscreenObj.GetFGP()

        elif(self.currentStep == 2):
            self.addFGPscreenObj.ListFingerNeedAdd(strMessage)
            self.addFGPscreenObj.GetFGP()

        elif(self.currentStep == 4):
            self.addFGPscreenObj.ShowStepStudentInformationAnim(self.frameContainWriteRFcard)
            self.writeRFcardObj.StopWriteToCard()
            self.addFGPscreenObj.GetFGP()
            self.currentStep = 2
        
    def GoToAddFaceScreen(self):
        if(self.flagNoCameraMode == True):
            return
        try:
            self.addFaceScreenObj.label_forShowName.setText(self.showInfoScreenObj.nameStudentNeedAdd)
        except:
            pass
        if(self.currentStep == 2):
            self.addFaceScreenObj.ShowStepStudentInformationAnim(self.frameContainAddFGP)
            self.addFGPscreenObj.StopAll()
            self.currentStep = 3
        
        if(self.currentStep == 1):
            self.addFaceScreenObj.ShowStepStudentInformationAnim(self.frameContainShowInfo)
            self.currentStep = 3 
        
        if(self.currentStep == 3):
            self.addFaceScreenObj.RetakePicture()

        elif(self.currentStep == 4):
            self.addFaceScreenObj.ShowStepStudentInformationAnim(self.frameContainWriteRFcard)
            self.writeRFcardObj.StopWriteToCard()
            self.currentStep = 3

    def GoToShowInfomation(self, inforString):
        self.showInfoScreenObj.ShowInformation(inforString)
        
        if(self.currentStep == 2):
            self.showInfoScreenObj.ShowStepStudentInformationAnim(self.frameContainAddFGP)
            self.addFGPscreenObj.StopAll()
            self.currentStep = 1

        if(self.currentStep == 3):
            self.showInfoScreenObj.ShowStepStudentInformationAnim(self.frameContainAddFace)
            self.addFaceScreenObj.StopTakePicture()
            self.currentStep = 1

        elif(self.currentStep == 4):
            self.showInfoScreenObj.ShowStepStudentInformationAnim(self.frameContainWriteRFcard)
            self.writeRFcardObj.StopWriteToCard()
            self.currentStep = 1

