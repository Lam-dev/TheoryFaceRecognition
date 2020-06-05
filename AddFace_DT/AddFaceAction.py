from AddFace_DT.AddFaceUI     import Ui_Frame_containAddFaceScreen
from PyQt5          import QtCore, QtGui
from PyQt5.QtCore   import pyqtSlot, pyqtSignal,QTimer, QDateTime, Qt, QObject, QPointF, QPropertyAnimation, pyqtProperty, QSize
from PyQt5          import QtWidgets
from CameraAndFaceRecognition_DT.CameraAndFaceRecognition   import GetImageFromCamera, FaceQuality

class AddFaceScreen(QObject, Ui_Frame_containAddFaceScreen):

    SignalPictureTaked = pyqtSignal(str)
    
    def __init__(self, frameContain, cameraObj):
        QObject.__init__(self)
        Ui_Frame_containAddFaceScreen.__init__(self)
        self.frameContainCurrentStep = frameContain
        self.setupUi(frameContain)
        self.cameraObj = GetImageFromCamera(cameraObj = cameraObj)
        self.cameraObj.PixmapFromCamera.connect(self.ShowCameraImage)
        self.cameraObj.SignalFaceQuality.connect(self.FaceQualityNotify)
        self.TimerCountdownTakePictureTime = QTimer(self)
        self.TimerCountdownTakePictureTime.timeout.connect(self.TakeAPicture)
        self.__timeCountdown = 3
        self.__pictureTaked = False
        self.__pixmapWarning = QtGui.QPixmap("icon/warning100.png")
        self.__pixmapHourglass = QtGui.QPixmap("icon/hourglass100.png")
        self.__pixmapNoFace = QtGui.QPixmap("icon/noFace100.png")
        self.__pixmapOk = QtGui.QPixmap("icon/ok100.png")
        self.__faceOkTime = 3
        self.label_showIconNotifyowIconNotify.show()

    def FaceQualityNotify(self, status):
        if(status == FaceQuality.NotFace):
            self.__faceOkTime = 4
            self.label_showGetFaceNotifyowGetFaceNotify.setStyleSheet('color: rgb(198, 0, 0);font: 75 bold 18pt "Ubuntu";')
            self.label_showGetFaceNotifyowGetFaceNotify.setText("* KHÔNG CÓ KHUÔN MẶT")
            self.label_showIconNotifyowIconNotify.setPixmap(self.__pixmapNoFace)
        if(status == FaceQuality.Small):
            self.__faceOkTime = 4
            self.label_showGetFaceNotifyowGetFaceNotify.setStyleSheet('color: rgb(198, 0, 0);font: 75 bold 18pt "Ubuntu";')
            self.label_showGetFaceNotifyowGetFaceNotify.setText("* VUI LÒNG ĐỨNG GẦN HƠN")
            self.label_showIconNotifyowIconNotify.setPixmap(self.__pixmapWarning)
        elif(status == FaceQuality.PoseWrong):
            self.__faceOkTime = 4
            self.label_showGetFaceNotifyowGetFaceNotify.setStyleSheet('color: rgb(198, 0, 0);font: 75 bold 18pt "Ubuntu";')
            self.label_showGetFaceNotifyowGetFaceNotify.setText("* VUI LÒNG NHÌN THẲNG")
            self.label_showIconNotifyowIconNotify.setPixmap(self.__pixmapWarning)
        elif(status == FaceQuality.PoseOk):
            self.__faceOkTime -= 1
            if(self.__faceOkTime == 0):
                self.label_showGetFaceNotifyowGetFaceNotify.setStyleSheet('color: rgb(0, 198, 0);font: 75 bold 18pt "Ubuntu";')
                self.label_showIconNotifyowIconNotify.setPixmap(self.__pixmapOk)
                self.label_showGetFaceNotifyowGetFaceNotify.setText("ĐÃ LẤY KHUÔN MẶT. XIN CẢM ƠN !")
                self.StopTakePicture()
                self.__TakeFeatureAndSendToServer()
                
                return
            self.label_showGetFaceNotifyowGetFaceNotify.setStyleSheet('color: rgb(255, 170, 0);font: 75 bold 18pt "Ubuntu";')
            self.label_showGetFaceNotifyowGetFaceNotify.setText("* GIỮ KHUÔN MẶT KHÔNG DI CHUYỂN TRONG  "+str(self.__faceOkTime) + " GIÂY")
            self.label_showIconNotifyowIconNotify.setPixmap(self.__pixmapHourglass)
    
    def __TakeFeatureAndSendToServer(self):
        faceFeatures = self.cameraObj.GetFaceFeature()
        if(len(faceFeatures) == 1):
            faceFeatureStrElem = [str(elem) for elem in faceFeatures[0]]
            faceFeatureStr = ",".join(faceFeatureStrElem)
        else:
            faceFeatureStr = ""
        self.SignalPictureTaked.emit(faceFeatureStr)


    def StopTakePicture(self):
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
        self.cameraObj.ClearFaceLocation()
        self.cameraObj.StartReadImage()
        self.__faceOkTime = 4

        
    def StartCamera(self):
        # self.TimerCountdownTakePictureTime.start(1000)
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