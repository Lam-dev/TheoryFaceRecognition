from AddFace_DT.AddFaceAction                   import AddFaceScreen
from ChoseStudent_DT.ChoseStudentAction         import ChoseStudent
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
    SignalAddDataForStudent = pyqtSignal(dict)
    
    SignalStartWriteRFcardDT = pyqtSignal(str, object)
    SignalStopWriteRFcardDT = pyqtSignal()
    # CloseTakeSampleScreen = pyqtSignal()
    SignalStopGetFGP = pyqtSignal()

    def __init__(self, frame, cameraObj):
        QObject.__init__(self)
        Ui_Frame.__init__(self)
        self.setupUi(frame)
        icon = QtGui.QIcon()
        icon1 = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/closeIcon50.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        icon1.addPixmap(QtGui.QPixmap("icon/back40.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_choseStudent.setIcon(icon1)
        self.pushButton_choseStudent.setIconSize(QtCore.QSize(40, 40))
        
        self.pushButton_exit.setIcon(icon)
        self.frameContain = QtWidgets.QFrame(frame)
        self.frameContain.setGeometry(QtCore.QRect(0, 50, 800, 429))
        self.frameContainShowInfo = QtWidgets.QFrame(self.frameContain)
        self.frameContainShowInfo.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.showInfoScreenObj = ShowInfoScreen(self.frameContainShowInfo)

        self.pushButton_exit.clicked.connect(self.CloseTakeSampleScreen)
        self.pushButton_choseStudent.clicked.connect(self.GoToChoseStudentScreen)

        self.currentStep = 1
        self.nameStudentNeedAdd = ""
        
        self.frameContainAddFace = QtWidgets.QFrame(self.frameContain)
        self.frameContainAddFace.setGeometry(QtCore.QRect(self.frameContain.width(), 0, 0, 0))

        self.frameContainChoseStudent = QtWidgets.QFrame(self.frameContain)
        self.frameContainChoseStudent.setGeometry(QtCore.QRect(self.frameContain.width(), 0, 0, 0))
        self.choseStudentObj = ChoseStudent(self.frameContainChoseStudent)
        self.choseStudentObj.SignalRequesDirectWriteCard.connect(self.__SlotWriteCard)
        self.choseStudentObj.SignalRequestDirectAddFace.connect(self.__SlotAddFace)
        self.choseStudentObj.SignalRequestDirectAddFGP.connect(self.__SlotAddFGP)
        self.choseStudentObj.SignalChoseStudent.connect(self.ChoseStudent)
        

        self.addFaceScreenObj = AddFaceScreen(self.frameContainAddFace, cameraObj)
        # self.addFaceScreenObj.SignalStartReadImage.connect(self.SignalStartReadImage.emit)
        # self.addFaceScreenObj.SignalStopReadImage.connect(self.SignalStopReadImage.emit)
        # self.addFaceScreenObj.SignalFaceTracking.connect(self.SignalFaceTracking.emit)
        # self.addFaceScreenObj.SignalGetFaceFeature.connect(self.SignalGetFaceFeature.emit)

        self.frameContainAddFGP = QtWidgets.QFrame(self.frameContain)
        self.frameContainAddFGP.setGeometry(QtCore.QRect(self.frameContain.width(), 0, 0, 0))
        self.addFGPscreenObj = AddFGPscreen(self.frameContainAddFGP)
        # self.addFGPscreenObj.SignalRequestGetFGP.connect(self.SignalRequestGetFGP.emit)
        # self.addFGPscreenObj.SignalStopGetFGP.connect(self.SignalStopGetFGP.emit)

        self.frameContainWriteRFcard = QtWidgets.QFrame(self.frameContain)
        self.frameContainWriteRFcard.setGeometry(QtCore.QRect(self.frameContain.width(), 0, 0, 0))
        self.writeRFcardObj = WriteRFcardAction(self.frameContainWriteRFcard)
        
        self.SignalWriteToRFcardSuccessfully = pyqtSignal()
        self.SignalStartWriteRFcard = pyqtSignal(str, object)
        self.SignalStopWriteRFcard = pyqtSignal()

        self.socketObj = SocketClientDT()
        self.socketObj.processReciptDataObj.SignalGoToAddFGP.connect(self.__SlotAddFGP)
        self.socketObj.processReciptDataObj.SignalGoToAddFace.connect(self.__SlotAddFace)
        self.socketObj.processReciptDataObj.SignalShowInformation.connect(self.GoToShowInfomation)
        self.socketObj.SignalRequestWriteCard.connect(self.__SlotWriteCard)

        

        self.writeRFcardObj = WriteRFcardAction(self.frameContainWriteRFcard)
        # self.writeRFcardObj.SignalStartWriteRFcardDT.connect(self.SignalStartWriteRFcardDT.emit)
        # self.writeRFcardObj.SignalStopWriteRFcardDT.connect(self.SignalStopWriteRFcardDT.emit)
        self.writeRFcardObj.SignalWriteCardSuccess.connect(self.socketObj.SendNotifyWriteRFcardSuccessfully)
        self.addFGPscreenObj.SignalSendImageToServer.connect(self.socketObj.SendFingerImage)
        self.addFGPscreenObj.SignalSendFGPGetToServer.connect(self.ProcessFGPadded)
        # self.addFGPscreenObj.SignalPlayBip.connect(self.__PlayBip)

        self.addFaceScreenObj.SignalPictureTaked.connect(self.ProcessFaceAdded)
        self.currentStep = 1
        self.flagNoCameraMode = False
        self.__flagDirectAdd = True
        self.__IDstudentNeedAdd = str

    def __SlotAddFGP(self, strMessage):
        if(self.sender() == self.socketObj.processReciptDataObj):
            self.GoToAddFGPscreen(strMessage)
            self.label_addDataMode.setText("LÊN MÁY CHỦ")
            self.__flagDirectAdd = False
        else:
            self.GoToAddFGPscreen(strMessage)
            self.label_addDataMode.setText("TRỰC TIẾP")
            self.__flagDirectAdd = True

    def __SlotAddFace(self):
        if(self.sender() == self.socketObj.processReciptDataObj):
            self.GoToAddFaceScreen()
            self.label_addDataMode.setText("LÊN MÁY CHỦ")
            self.__flagDirectAdd = False
        else:
            self.GoToAddFaceScreen()
            self.label_addDataMode.setText("TRỰC TIẾP")
            self.__flagDirectAdd = True
    
    def __SlotWriteCard(self, strMessage):
        if(self.sender() == self.socketObj.processReciptDataObj):
            self.GoToWriteRFcardScreen(strMessage)
            self.label_addDataMode.setText("LÊN MÁY CHỦ")
            self.__flagDirectAdd = False
        else:
            self.GoToWriteRFcardScreen(strMessage)
            self.label_addDataMode.setText("TRỰC TIẾP")
            self.__flagDirectAdd = True

    def ChoseStudent(self, student):
        self.__flagDirectAdd = True
        self.__IDstudentNeedAdd = student.ID
        self.label_addDataMode.setText("TRỰC TIẾP")

    def ProcessFGPadded(self, feature, nameFinger):
        if(self.__flagDirectAdd == True):
            self.CreateInfoDict("", feature)
        else:
            self.socketObj.SendFingerFeature(feature, nameFinger)

    def ProcessFaceAdded(self, feature):
        if(self.__flagDirectAdd == True):
            self.CreateInfoDict(feature, "")
        else:
            self.socketObj.SendTakedImage(feature)

    def CreateInfoDict(self, faceFeatureStr, FGPfeatureStr):
        try:
            faceEncodingStringArr = faceFeatureStr.split(",")
            faceEncodingArr = [float(elem) for elem in faceEncodingStringArr]
        except:
            faceEncodingArr = []
        try:
            lstMultiFGPfeatureStr = FGPfeatureStr.split(";")
            lstFGP = []
            for FGPfeatureStr in lstMultiFGPfeatureStr:
                FGPfeatureStrArr = FGPfeatureStr.split(",")
                FGPfeatureArr = [int(elem) for elem in FGPfeatureStrArr]
                lstFGP.append(FGPfeatureArr)
        # FGPencodingStringArr = jsonDict["FGPEncoding"].split(",")
        # FGPencodingArr = [int(elem) for elem in FGPencodingStringArr]
        except:
            lstFGP = []
        faceInfoDict = {
            "faceEncodingArr": faceEncodingArr,
            "FGPencoding":lstFGP,
            "idStudent" : self.__IDstudentNeedAdd,
        }
        self.SignalAddDataForStudent.emit(faceInfoDict)
        

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
        if(self.currentStep == 0):
            self.writeRFcardObj.ShowStepStudentInformationAnim(self.frameContainChoseStudent)
            self.currentStep = 4

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
        if(self.currentStep == 0):
            self.addFGPscreenObj.ShowStepStudentInformationAnim(self.frameContainChoseStudent)
            self.currentStep = 2

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
        if(self.currentStep == 0):
            self.addFaceScreenObj.ShowStepStudentInformationAnim(self.frameContainChoseStudent)
            self.currentStep = 3

        elif(self.currentStep == 2):
            self.addFaceScreenObj.ShowStepStudentInformationAnim(self.frameContainAddFGP)
            self.addFGPscreenObj.StopAll()
            self.currentStep = 3
        
        elif(self.currentStep == 1):
            self.addFaceScreenObj.ShowStepStudentInformationAnim(self.frameContainShowInfo)
            self.currentStep = 3 
        
        elif(self.currentStep == 3):
            self.addFaceScreenObj.RetakePicture()

        elif(self.currentStep == 4):
            self.addFaceScreenObj.ShowStepStudentInformationAnim(self.frameContainWriteRFcard)
            self.writeRFcardObj.StopWriteToCard()
            self.currentStep = 3

    def GoToShowInfomation(self, inforString):
        self.showInfoScreenObj.ShowInformation(inforString)
        if(self.currentStep == 0):
            self.showInfoScreenObj.ShowStepStudentInformationAnim(self.frameContainChoseStudent)
            self.currentStep = 1

        elif(self.currentStep == 2):
            self.showInfoScreenObj.ShowStepStudentInformationAnim(self.frameContainAddFGP)
            self.addFGPscreenObj.StopAll()
            self.currentStep = 1

        elif(self.currentStep == 3):
            self.showInfoScreenObj.ShowStepStudentInformationAnim(self.frameContainAddFace)
            self.addFaceScreenObj.StopTakePicture()
            self.currentStep = 1

        elif(self.currentStep == 4):
            self.showInfoScreenObj.ShowStepStudentInformationAnim(self.frameContainWriteRFcard)
            self.writeRFcardObj.StopWriteToCard()
            self.currentStep = 1
    
    def GoToChoseStudentScreen(self):
        if(self.currentStep == 0):
            pass

        elif(self.currentStep == 1):
            self.choseStudentObj.ShowStepStudentInformationAnim(self.frameContainShowInfo)
            self.currentStep = 0

        elif(self.currentStep == 2):
            self.choseStudentObj.ShowStepStudentInformationAnim(self.frameContainAddFGP)
            self.addFGPscreenObj.StopAll()
            self.currentStep = 0
        
        elif(self.currentStep == 3):
            self.choseStudentObj.ShowStepStudentInformationAnim(self.frameContainAddFace)
            self.addFaceScreenObj.StopTakePicture()
            self.currentStep = 0

        elif(self.currentStep == 4):
            self.choseStudentObj.ShowStepStudentInformationAnim(self.frameContainWriteRFcard)
            self.writeRFcardObj.StopWriteToCard()
            self.currentStep = 0