from AddFace.AddFaceAction                      import AddFaceScreen
from ShowInfomation.ShowInfomationAction        import ShowInfoScreen
from AddFGP.AddFGPaction                        import AddFGPscreen 
from WriteRFcard.WriteRFcardScreenAction        import WriteRFcardAction
from PyQt5                                      import QtCore, QtGui
from PyQt5.QtCore                               import pyqtSlot, pyqtSignal,QTimer, QDateTime, Qt, QObject, QPointF, QPropertyAnimation, pyqtProperty, QSize
from PyQt5                                      import QtWidgets

class TakeSampleScreen(QObject):

    def __init__(self, frame):
        QObject.__init__(self)
        self.frameContain = frame

        self.frameContainShowInfo = QtWidgets.QFrame(self.frameContain)
        self.frameContainShowInfo.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.showInfoScreenObj = ShowInfoScreen(self.frameContainShowInfo)


        self.frameContainAddFace = QtWidgets.QFrame(self.frameContain)
        self.frameContainAddFace.setGeometry(QtCore.QRect(self.frameContain.width(), 0, 0, 0))
        self.addFaceScreenObj = AddFaceScreen(self.frameContainAddFace)

        self.frameContainAddFGP = QtWidgets.QFrame(self.frameContain)
        self.frameContainAddFGP.setGeometry(QtCore.QRect(self.frameContain.width(), 0, 0, 0))
        self.addFGPscreenObj = AddFGPscreen(self.frameContainAddFGP)

        self.frameContainWriteRFcard = QtWidgets.QFrame(self.frameContain)
        self.frameContainWriteRFcard.setGeometry(QtCore.QRect(self.frameContain.width(), 0, 0, 0))
        self.writeRFcardObj = WriteRFcardAction(self.frameContainWriteRFcard)
    
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
            self.addFGPscreenObj.GetFGP()
            self.writeRFcardObj.StopWriteToCard()
            self.currentStep = 2
        
    def GoToAddFaceScreen(self):
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

