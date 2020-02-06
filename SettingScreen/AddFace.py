from PyQt5                  import QtCore, QtGui, QtWidgets
from PyQt5                  import QtCore, QtGui, QtWidgets
from PyQt5.QtGui            import QIcon, QPixmap
from PyQt5.QtCore           import pyqtSlot, pyqtSignal,QTimer, QDateTime, Qt, QObject, QPointF, QPropertyAnimation, pyqtProperty
from SettingScreen.AddFaceUI                  import Ui_Frame_AddFace
from CameraAndFaceRecognition.CameraAndFaceRecognition  import *

class AddFaceScreen(Ui_Frame_AddFace, QObject):

    SignalGrappedImage = pyqtSignal(object)
    
    def __init__(self, Frame):
        Ui_Frame_AddFace.__init__(self)
        QObject.__init__(self)
        self.setupUi(Frame)
        self.frameContainCurrentStep = Frame
        self.cameraObj = GetImageFromCamera(labelObject = self.label_forShowCamera, size = (350, 425), frameCut = ((0, 640), (0, 480)))
        self.timer3sCountdown = QTimer(self)
        self.timer3sCountdown.timeout.connect(self.CountDown)
        self.countdownTime = 3
        self.faceRecognitionObj = FaceRecognition()
        # self.pushButton_changeImage.clicked.connect(self.ChangeImage)
        self.imageGrapped = False
        self.addForStudent = False
        self.reloadPixmap = QtGui.QPixmap("icon/iconReadFace.png")
        self.label_countdownTime.mouseReleaseEvent = lambda event : self.ChangeImage()

    def ClearAddAdded(self):
        self.imageGrapped = False
        self.countdownTime = 3

    def GetFaceEncodingImageGrapped(self):
        faceEcodingStr, faceEncodingArr = GetFaceEncodingFromImage().GetFaceEncodingStr(self.imageGrapped)
        faceInfoDict = {
            "image":self.imageGrapped,
            "faceEncodingStr":faceEcodingStr,
            "faceEncodingArr": faceEncodingArr,
            "student":self.addForStudent
        }
        return faceInfoDict

    def CountDown(self):
        if(self.countdownTime == 0):
            self.timer3sCountdown.stop()
            self.cameraObj.StopReadImage()
            self.faceRecognitionObj.StopFaceTracking()
            self.label_countdownTime.setText("")
            self.label_countdownTime.setPixmap(self.reloadPixmap)
            self.GrapImage()
            return
        self.countdownTime -= 1
        self.label_countdownTime.setText(str(self.countdownTime))

    def ChangeImage(self):
        self.countdownTime = 3
        self.StartCamera()

    def GrapImage(self):

        self.imageGrapped = self.cameraObj.TakeAphoto()
        rgbImage = cv2.cvtColor(self.imageGrapped, cv2.COLOR_BGR2RGB)
        convertToQtFormat = QtGui.QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0],
                                        QtGui.QImage.Format_RGB888)
        convertToQtFormat = QtGui.QPixmap.fromImage(convertToQtFormat)
        pixmap = QPixmap(convertToQtFormat)
        resizeImage = pixmap.scaled(280, 480, QtCore.Qt.KeepAspectRatio)
        self.label_forShowCamera.setPixmap(resizeImage)
    
    def StartCamera(self):
        self.cameraObj.StartReadImage()
        self.faceRecognitionObj.StartFaceTracking()
        self.timer3sCountdown.start(1000)

    def StopCamera(self):
        self.timer3sCountdown.stop()
        self.cameraObj.StopReadImage()
        self.faceRecognitionObj.StopFaceTracking()
        
    def ShowStepStudentInformationAnim(self, frameOfPreStep):

        self.preStepGoToLeftAnim = QPropertyAnimation(frameOfPreStep, b"geometry")
        self.preStepGoToLeftAnim.setDuration(300)
        self.preStepGoToLeftAnim.setStartValue(QtCore.QRect(0 , frameOfPreStep.y() , frameOfPreStep.width(), frameOfPreStep.height()))
        self.preStepGoToLeftAnim.setEndValue(QtCore.QRect(0-frameOfPreStep.width() , frameOfPreStep.y(), frameOfPreStep.width(), frameOfPreStep.height()))
        
        self.currentStepToLeftAnim = QPropertyAnimation(self.frameContainCurrentStep, b"geometry")
        self.currentStepToLeftAnim.setDuration(300)
        self.currentStepToLeftAnim.setStartValue(QtCore.QRect(frameOfPreStep.width() , self.frameContainCurrentStep.y() , self.frameContainCurrentStep.width(), self.frameContainCurrentStep.height()))
        self.currentStepToLeftAnim.setEndValue(QtCore.QRect(0 , self.frameContainCurrentStep.y(), self.frameContainCurrentStep.width(), self.frameContainCurrentStep.height()))
        self.frameContainCurrentStep.show()

        self.preStepGoToLeftAnim.start()
        self.currentStepToLeftAnim.start()
        self.currentStepToLeftAnim.finished.connect(self.StartCamera)
    