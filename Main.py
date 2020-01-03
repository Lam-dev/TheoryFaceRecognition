from    CameraAndFaceRecognition.CameraAndFaceRecognition  import GetImageFromCamera, FaceRecognition
from    MainScreen.MainScreen                   import MainScreen

from        DatabaseAccess.DatabaseAccess       import *
from        PyQt5                               import QtCore, QtGui, QtWidgets, Qt
from        PyQt5.QtCore                        import pyqtSlot, pyqtSignal,QTimer, QDateTime,Qt, QObject
from         PyQt5                              import QtCore, QtGui, QtWidgets
from         PyQt5                              import QtGui
from         PyQt5                              import QtWidgets
from         PyQt5.QtGui                        import QPixmap,QColor
from         PyQt5.QtWidgets                    import *
import       sys
from         datetime                           import datetime
from         Sound.OrangePiSound                import Sound
from         SocketConnect.SocketClient         import SocketClient
import       os
from         FingerPrintSensor.FingerPrint      import Fingerprint

# from   Sound.Sound              import Sound
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.HideCameraPixmap = QtGui.QPixmap("icon/imageFaceRecognition.png")
        self.mainScreenObj = MainScreen(self)
        self.cameraObj = GetImageFromCamera(labelObject= self.mainScreenObj.label_showCamera)
        self.lstStudent = GetDataFromDatabase().GetListStudent()
        self.faceRecognitionObj = FaceRecognition(self.lstStudent)
        self.socketObject = SocketClient() #comment test came
        self.mainScreenObj.SetGeometryForLabelShowCamera(273,381)
        # self.mainScree-nObj.pushButton_shutdown.clicked.connect(lambda:os.system('sudo shutdown now'))
        self.mainScreenObj.pushButton_shutdown.clicked.connect(self.__ShowSettingScreen)
        # self.mainScreenObj.ShowNotStudentInformation()
        self.mainScreenObj.SignalGoToDesktop.connect(self.close)
        self.mainScreenObj.SignalModifyImageQuality.connect(self.__ModifyImageQuality)
        self.mainScreenObj.SignalModifyFaceMark.connect(self.__ModifyFaceMark)
        self.mainScreenObj.SignalModifyFRthreshold.connect(self.__ModifyFRthreshold)
        self.mainScreenObj.SignalConnectNewServer.connect(self.socketObject.ConnectNewServer)
        self.mainScreenObj.SignalConnectNewFTPserver.connect(self.__ConnectNewFTPserver)
        self.mainScreenObj.SignalSettingScreenHiden.connect(self.__SettingScreenHiden)
        self.mainScreenObj.SignalAddFaceEncodeAndFGP.connect(self.__AddFaceEncodingAndFGP)
        # self.soundObj = Sound()
#region   dieu khien signal tu camera

        self.cameraObj.PixmapFromCamera.connect(self.__ShowImageFromCamera)
        self.cameraObj.CanNotConnectCamera.connect(self.mainScreenObj.ShowCanNotConnectCamera)
        self.cameraObj.StartReadImage()
        self.cameraObj.SignalHideCamera.connect(self.__HideCamera)

        self.faceRecognitionObj.StudentRecognized.connect(self.__RecognizedStudent)
        self.faceRecognitionObj.StudentNotRecognized.connect(self.__NotRecognized)
        self.faceRecognitionObj.StartFaceTracking()
        self.faceRecognitionObj.StartFaceRecognize()
        
        
#endregion

#region cac cai dat
        self.settingFindOrConfirmStudent = "C" # che do tim mot hoc vien hoac xac nhan hoc vien gui xuong
#endregion 
#region
        self.socketObject.ShowStudentForConfirm.connect(self.__ShowAndChooseStudentForConfirm)
        self.socketObject.SignalServerNotConnect.connect(self.ServerNotConnect)
        self.socketObject.SignalServerConnected.connect(self.ServerConnected)
        self.socketObject.SignalWaitForUpdateDatabase.connect(self.WaitForUpdateDatabase)
        self.socketObject.SignalUpdateDatabaseSuccess.connect(self.UpdateDatabaseSuccess)
        self.socketObject.SignalNumberStudentParsed.connect(self.NumberStudentParsed)

#endregion
        self.timerReopenReadCam = QTimer(self)
        self.timerReopenReadCam.timeout.connect(self.__ReopenReadCamera)

        self.FGPobj = Fingerprint()
        self.FGPobj.SignalRecognizedFGP.connect(self.RecognizedFGP)
        self.FGPobj.BatLayVanTayDangNhap()

    def RecognizedFGP(self, studentID):
        self.__OffCameraTemporary()
        for student in self.lstStudent:
            if(student.ID == studentID):
                self.mainScreenObj.ShowStudentInfomation(student)
                self.socketObject.SendResultsFGPrecognition(studentID)
                break
        

    def __AddFaceEncodingAndFGP(self, faceDict, FGPdict):
        khoThiSinh = ThiSinhRepository()
        khoThiSinh.capNhatTruong(("NhanDienKhuonMatThem", ), (faceDict["faceEncodingStr"], ), "ID = %s"%(str(faceDict["student"].ID)))
        
        idVaVanTay = AnhXaIDvaVanTay()
        idVaVanTay.IDThiSinh = faceDict["student"].ID
        idVaVanTay.ViTriVanTay = FGPdict["FGPsavePos"]
        featureStrArr = [str(elem) for elem in FGPdict["FGPfeature"]]
        featureStr = ",".join(featureStrArr)
        idVaVanTay.DacTrungVanTay = featureStr
        khoIDvaVanTay = IDvaVanTayRepository()
        khoIDvaVanTay.ghiDuLieu(idVaVanTay)
        
        for thiSinh in self.lstStudent:
            if(thiSinh.ID == faceDict["student"].ID):
                thiSinh.NhanDienKhuonMatThem = faceDict["faceEncodingArr"]
                break
        self.mainScreenObj.databaseScreenObj.ShowAddDataDialog()
        sendDict = {
            "ID":faceDict["student"].ID,
            "FaceEncoding":faceDict["faceEncodingStr"],
            "FGPEncoding":featureStr
        }
        self.socketObject.SendAddFaceAndFGP(sendDict)



    def __SettingScreenHiden(self):
        self.cameraObj.StartReadImage()
        self.faceRecognitionObj.StartFaceTracking()
        self.faceRecognitionObj.StartFaceRecognize()

    def __ReopenReadCamera(self):
        self.mainScreenObj.ClearStudentRecognizedInfomation()
        self.cameraObj.StartReadImage()
        self.faceRecognitionObj.StartFaceRecognize()
        self.faceRecognitionObj.StartFaceTracking()
        self.timerReopenReadCam.stop()
    
    def __ConnectNewFTPserver(self, ftpServerDict):
        connectAvailabel = self.socketObject.ftpObj.ConnectNewFTPserver(ftpServerDict)
        self.mainScreenObj.ShowFTPserverConnectAvailabel(connectAvailabel)

    def __HideCamera(self):
        self.mainScreenObj.label_showCamera.setPixmap(self.HideCameraPixmap)

    def __ModifyImageQuality(self, quality):
        print(quality)

    def __ModifyFaceMark(self, mark):
        print(mark)

    def __ModifyFRthreshold(self, threshold):
        self.faceRecognitionObj.FRthreshold = threshold

    def NumberStudentParsed(self, number, all):
        self.mainScreenObj.ShowNumberStudentParsed(number, all)

    def UpdateDatabaseSuccess(self, listStudents):
        self.lstStudent.clear()
        self.lstStudent.extend(listStudents)
        self.faceRecognitionObj.StartFaceRecognize()
        self.cameraObj.StartReadImage()
        self.mainScreenObj.fateScreen()

    def WaitForUpdateDatabase(self, filePath):
        self.faceRecognitionObj.StopFaceRecognize()
        self.cameraObj.StopReadImage()
        self.mainScreenObj.ShowUpdateScreen(filePath)

    def __ShowSettingScreen(self):
        self.faceRecognitionObj.StopFaceRecognize()
        self.faceRecognitionObj.StopFaceTracking()
        self.FGPobj.TatLayVanTayDangNhap()
        self.cameraObj.StopReadImage()
        self.mainScreenObj.ShowSettingScreen()

    def ServerNotConnect(self):
        # self.cameraObj.StopReadImage()
        self.mainScreenObj.ShowNotConnect()

    def ServerConnected(self):
        self.cameraObj.StartReadImage()
        self.mainScreenObj.ShowConnected()

    def __NotRecognized(self, student, jpegData):
        # self.soundObj.ThreadPlayBip__Bip()
        # self.soundObj.ThreadPlayTSkhongTrungKhop()
        fp = open("imageTosend.jpg", 'wb')
        fp.write(jpegData)
        self.socketObject.SendResultsFaceRecognize(student.MaDK, "F", "imageTosend.jpg")
    
    def __ShowAndChooseStudentForConfirm(self, maDK):
        for student in self.lstStudent:
            if(student.MaDK.__str__() == maDK):
                self.mainScreenObj.ShowWarningLookAtCamera()
                self.mainScreenObj.ShowStudentInfomation(student)
                studentForConfirm = []
                studentForConfirm.append(student)
                self.faceRecognitionObj.SetListStudent(studentForConfirm)
                self.faceRecognitionObj.StartFaceRecognize()
                return
                
    def __RecognizedStudent(self, studentObj, faceImageJpgData):
        self.__OffCameraTemporary()
        if(self.settingFindOrConfirmStudent == "C"):
            # self.soundObj.ThreadPlayBipBipBip()
            # self.soundObj.ThreadPlayMoiTSlenXe()
            fp = open("imageTosend.jpg", 'wb')
            fp.write(faceImageJpgData)
            self.mainScreenObj.ShowStudentInfomation(studentObj)
            # self.mainScreenObj.ShowFaceRecognizeOK()
            self.socketObject.SendResultsFaceRecognize(studentObj.ID, "T", "imageTosend.jpg")

    def __OffCameraTemporary(self):
        self.cameraObj.StopReadImage()
        self.faceRecognitionObj.StopFaceTracking()
        self.faceRecognitionObj.StopFaceRecognize()
        self.__HideCamera()
        self.timerReopenReadCam.start(1500)

    def __ShowImageFromCamera(self, pixmap):
        self.mainScreenObj.label_showCamera.setPixmap(pixmap)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowFlags(Qt.FramelessWindowHint)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
