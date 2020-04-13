from AddFace.AddFaceUI     import Ui_Frame_containAddFaceScreen
from PyQt5          import QtCore, QtGui
from PyQt5.QtCore   import pyqtSlot, pyqtSignal,QTimer, QDateTime, Qt, QObject, QPointF, QPropertyAnimation, pyqtProperty, QSize
from PyQt5          import QtWidgets
from CameraAndFaceRecognition.CameraAndFaceRecognition   import GetImageFromCamera

class AddFaceScreen(QObject, Ui_Frame_containAddFaceScreen):

    SignalPictureTaked = pyqtSignal(str)
    
    def __init__(self, frameContain):
        QObject.__init__(self)
        Ui_Frame_containAddFaceScreen.__init__(self)
        self.frameContainCurrentStep = frameContain
        self.setupUi(frameContain)
        self.cameraObj = GetImageFromCamera()
        self.cameraObj.PixmapFromCamera.connect(self.ShowCameraImage)
        self.TimerCountdownTakePictureTime = QTimer(self)
        self.TimerCountdownTakePictureTime.timeout.connect(self.TakeAPicture)
        self.__timeCountdown = 3
        self.__pictureTaked = False

    def StopTakePicture(self):
        self.TimerCountdownTakePictureTime.stop()
        self.__pictureTaked = False
        self.__timeCountdown = 3
        self.cameraObj.StopReadImage()

        

    def TakeAPicture(self):
        self.__timeCountdown = self.__timeCountdown - 1
        self.label_forShowTimeCountdown.setText(str(self.__timeCountdown))
        if(self.__timeCountdown == 0):
            self.__pictureTaked = True
            self.TimerCountdownTakePictureTime.stop()
            self.cameraObj.StopReadImage()
            self.cameraObj.FaceTracking()
            faceFeatures = self.cameraObj.GetFaceFeature()
            if(len(faceFeatures) == 1):
                faceFeatureStrElem = [str(elem) for elem in faceFeatures[0]]
                faceFeatureStr = ",".join(faceFeatureStrElem)
            else:
                faceFeatureStr = ""
            self.SignalPictureTaked.emit(faceFeatureStr)

    def RetakePicture(self):
        if(self.__pictureTaked):
            self.__pictureTaked = False
            self.__timeCountdown = 3
            self.cameraObj.ClearFaceLocation()
            self.cameraObj.StartReadImage()
            self.TimerCountdownTakePictureTime.start(1000)

        
    def StartCamera(self):
        self.TimerCountdownTakePictureTime.start(1000)
        self.cameraObj.StartReadImage()
    
    def ShowCameraImage(self, pixmap):
        self.label_forShowCamera.setPixmap(pixmap)
    
    def ShowStepStudentInformationAnim(self, frameOfPreStep):

        self.preStepGoToLeftAnim = QPropertyAnimation(frameOfPreStep, b"geometry")
        self.preStepGoToLeftAnim.setDuration(300)
        self.preStepGoToLeftAnim.setStartValue(QtCore.QRect(0 , frameOfPreStep.y() , frameOfPreStep.width(), frameOfPreStep.height()))
        self.preStepGoToLeftAnim.setEndValue(QtCore.QRect(0-frameOfPreStep.width() , frameOfPreStep.y(), frameOfPreStep.width(), frameOfPreStep.height()))
        
        self.currentStepToLeftAnim = QPropertyAnimation(self.frameContainCurrentStep, b"geometry")
        self.currentStepToLeftAnim.setDuration(300)
        self.currentStepToLeftAnim.setStartValue(QtCore.QRect(frameOfPreStep.width() , self.frameContainCurrentStep.y() , self.frameContainCurrentStep.width(), self.frameContainCurrentStep.height()))
        self.currentStepToLeftAnim.setEndValue(QtCore.QRect(0 , self.frameContainCurrentStep.y(), self.frameContainCurrentStep.width(), self.frameContainCurrentStep.height()))
        
        self.preStepGoToLeftAnim.start()
        self.currentStepToLeftAnim.start()
        self.currentStepToLeftAnim.finished.connect(self.StartCamera)