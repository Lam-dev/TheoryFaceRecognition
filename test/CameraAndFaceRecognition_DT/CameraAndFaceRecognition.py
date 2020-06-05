import cv2
from CameraAndFaceRecognition import face_recognition
import threading
from   PyQt5.QtCore     import pyqtSlot, pyqtSignal,QTimer, QDateTime,Qt, QObject
from   PyQt5.QtGui      import QPixmap,QColor
from   PyQt5            import QtCore, QtGui
import time
import math
from    GetSettingFromJSON    import GetSetting
import enum

Camera_Number = 0
Camera_Object = cv2.VideoCapture(Camera_Number)
frame = False
FaceLocationInImage = False
NumberFrameNotFace = 0


class GetImageFromCamera(QObject):
    CanNotConnectCamera = pyqtSignal()
    PixmapFromCamera = pyqtSignal(QPixmap)
    SignalHideCamera = pyqtSignal()
    SignalFaceQuality = pyqtSignal(object)

    def __init__(self, frameCut = ((140, 500), (0, 480)), size = (300, 400), scale = 0.4, time = 50, labelObject = ""):
        super().__init__()
        self.cameraObj = Camera_Object
        self.frameCut = frameCut
        self.scale = scale
        self.time = time
        self.size = size
        self.toBeReadImage = False
        self.timerReadImage = QTimer(self)
        self.timerReadImage.timeout.connect(self.__GetImageFromCamera)
        self.labelObject = labelObject
        self.__numberFrameNotDetectFace = 0
        self.__lst3imageOk = []

        SETTING_DICT= GetSetting.GetHeadPoseCalibValue()
        self.DISTANCE = SETTING_DICT["distance"]
        self.EAR_EYE = SETTING_DICT["eye"]
        self.Y_SMALLEST = SETTING_DICT["ySmallest"]
        self.Y_BIGGEST = SETTING_DICT["yBiggest"]
        self.X_SMALLEST = SETTING_DICT["xSmallest"]
        self.X_BIGGEST= SETTING_DICT["xBiggest"]
        self.__flagDistanceOK = False
        self.__flagPoseOk = False

        # self.StartReadImage()

    def StopReadImage(self):
        self.timerReadImage.stop()

    def StartReadImage(self):
        self.timerReadImage.start(60)
        self.__lst3imageOk.clear()


    def __ThreadReadCamera(self):
        threadReadCam = threading.Thread(target= self.__GetImageFromCamera, args=(), daemon=True)
        threadReadCam.start()

    def ClearFaceLocation(self):
        global FaceLocationInImage
        FaceLocationInImage = False

    def __GetImageFromCamera(self):
        global frame
        global FaceLocationInImage
        global NumberFrameNotFace
        # while True:
        ret, frame = self.cameraObj.read()
        
        if(not ret):
            self.CanNotConnectCamera.emit()
            time.sleep(2)
        else:
            frame = frame[self.frameCut[1][0]:self.frameCut[1][1], self.frameCut[0][0]:self.frameCut[0][1]]
            if(self.__numberFrameNotDetectFace == 20):
                FaceLocationInImage, poseQuality = self.__DetectFaceAndPose(cv2.resize(frame, (0, 0), fx = self.scale, fy = self.scale))
                notifyContent = FaceQuality.NotFace
                if(type(FaceLocationInImage) is bool):
                    notifyContent = FaceQuality.NotFace
                elif(self.NotifySmallFace(FaceLocationInImage[0][3], FaceLocationInImage[0][1])):
                    notifyContent = FaceQuality.Small
                else:
                    notifyContent = poseQuality
                    if(poseQuality == FaceQuality.PoseOk):
                        if(len(self.__lst3imageOk) == 2):
                            self.__lst3imageOk.pop()
                        
                        self.__lst3imageOk.insert(0, frame.copy())
                        
                self.SignalFaceQuality.emit(notifyContent)
                self.__numberFrameNotDetectFace = 0
            else:
                self.__numberFrameNotDetectFace += 1
            
            # frame = cv2.resize(frame, (0, 0), fx = self.scale, fy = self.scale)
            if(type(FaceLocationInImage) is not bool):


                # for (top, right, bottom, left) in FaceLocationInImage[0]:
                top = int(FaceLocationInImage[0][0] * 2.5)
                right = int(FaceLocationInImage[0][1] * 2.5)
                bottom = int(FaceLocationInImage[0][2] * 2.5)
                left = int(FaceLocationInImage[0][3] * 2.5)
                cv2.rectangle(frame, (left, top), (right, bottom), (255, 255, 0), 2)

            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            convertToQtFormat = QtGui.QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0],
                                            QtGui.QImage.Format_RGB888)
            convertToQtFormat = QtGui.QPixmap.fromImage(convertToQtFormat)
            pixmap = QPixmap(convertToQtFormat)
            resizeImage = pixmap.scaled(self.size[0], self.size[1], QtCore.Qt.KeepAspectRatio)
            self.PixmapFromCamera.emit(resizeImage)

    def __DetectFaceAndPose(self, frame):
        faceLocations = face_recognition.face_locations(frame)
        if(len(faceLocations) != 0):
            _,euler_angle = face_recognition.get_head_pose(frame, faceLocations)
            return faceLocations, self.calcAngle(euler_angle[1, 0], euler_angle[0, 0])
        else:
            return False, False

    def NotifySmallFace(self, x, y):
        print(y - x)
        if(abs(y - x) < self.DISTANCE):
            return True
        else:
            return False


    def calcAngle(self, x, y):
        if(x < 0):
            x = x / 4
        else:
            x = x/ 1.5
        y = y - 20
        # print(x, y)
        
        if(((y>=self.Y_SMALLEST)&(y<=self.Y_BIGGEST))&((x>=self.X_SMALLEST) & (x<=self.X_BIGGEST))):
            return FaceQuality.PoseOk
        else:
            return FaceQuality.PoseWrong

    def __DetectFaceInImage(self, image):
        faceLocInImage = face_recognition.face_locations(image)
        if(len(faceLocInImage) == 0):
            return False
        else:
            return faceLocInImage

    def FaceTracking(self):
        if(type(frame) is bool):
            return
        localFrame = frame
        # self.imageDetectFace = localFrame[:, :, ::-1]
        return self.__DetectFaceInImage(localFrame)
    
    def GetFaceFeature(self):
        faceImage = self.__lst3imageOk[1]
        FaceLocationInImage = face_recognition.face_locations(faceImage)
        if(type(FaceLocationInImage) is not bool):
            top = int(FaceLocationInImage[0][0])
            right = int(FaceLocationInImage[0][1])
            bottom = int(FaceLocationInImage[0][2])
            left = int(FaceLocationInImage[0][3])
            cv2.rectangle(faceImage, (left, top), (right, bottom), (255, 255, 0), 2)
        cv2.imwrite("imageToSend.jpg", faceImage)
        faceLocation = self.__lst3imageOk[1][1]
        faceEncodings = face_recognition.face_encodings(faceImage, FaceLocationInImage)
        return faceEncodings
    

class FaceQuality(enum.Enum):
    NotFace = 0
    Small = 1
    PoseWrong = 2
    DistanceOk = 3
    PoseOk = 4
