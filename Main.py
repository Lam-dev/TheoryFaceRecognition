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
# from         Sound.OrangePiSound                import Sound
from         SocketConnect.SocketClient         import SocketClient
import       os
from         FingerPrintSensor.FingerPrint      import Fingerprint
from         Sound.OrangePiSound                import Sound
from         WriteRFcard.ControlRFIDmodule   import ControlRFIDmudule
import       json

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
        # self.mainScree-nObj.pushButton_shutdown.clicked.connect(lambda:os.system('sudo shutdown now'))\
        self.mainScreenObj.pushButton_shutdown.clicked.connect(self.__ShowSettingScreen)
        # self.mainScreenObj.ShowNotStudentInformation()
        self.mainScreenObj.SignalGoToDesktop.connect(self.GoToDesktop)
        self.mainScreenObj.SignalModifyImageQuality.connect(self.__ModifyImageQuality)
        self.mainScreenObj.SignalModifyFaceMark.connect(self.__ModifyFaceMark)
        self.mainScreenObj.SignalModifyFRthreshold.connect(self.__ModifyFRthreshold)
        self.mainScreenObj.SignalConnectNewServer.connect(self.socketObject.ConnectNewServer)
        self.mainScreenObj.SignalConnectNewFTPserver.connect(self.__ConnectNewFTPserver)
        self.mainScreenObj.SignalSettingScreenHiden.connect(self.__SettingScreenHiden)
        self.mainScreenObj.SignalAddFaceEncodeAndFGP.connect(self.__AddFaceEncodingAndFGP)
        self.mainScreenObj.SignalDeleteFaceAdded.connect(self.__DeleteFaceAdded)
        self.mainScreenObj.SignalDeleteFGPadded.connect(self.__DeleteFGPadded)
        self.mainScreenObj.SignalShutdown.connect(self.Shutdown)
        self.mainScreenObj.SignalCloseELT.connect(self.close)
        self.mainScreenObj.SignalDeleteAllData.connect(self.DeleteAllData)
        self.mainScreenObj.SignalRequestGoToTakeSampleScreen.connect(self.GoToTakeSampleScreen)

        self.khoLichSu = LichSuRepository()
        self.soundObj = Sound()

#region   dieu khien signal tu camera

        self.cameraObj.PixmapFromCamera.connect(self.__ShowImageFromCamera)
        self.cameraObj.CanNotConnectCamera.connect(self.mainScreenObj.ShowCanNotConnectCamera)
        self.cameraObj.StartReadImage()
        self.cameraObj.SignalHideCamera.connect(self.__HideCamera)

        self.faceRecognitionObj.StudentRecognized.connect(self.__RecognizedStudent)
        self.faceRecognitionObj.StudentNotRecognized.connect(self.__NotRecognized)
        # self.faceRecognitionObj.StartFaceTracking()
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
        self.socketObject.SignalUpdateOrSyncStudentInfo.connect(self.AddStudentInfomation)
        self.socketObject.SignalStopForUpdateData.connect(self.ShowWaitForUpdateDataScreen)
        self.socketObject.SignalDeleteFGPofStudent.connect(self.DeleteFGPofStudentInSensor)

#endregion
        self.timerReopenReadCam = QTimer(self)
        self.timerReopenReadCam.timeout.connect(self.__ReopenReadCamera)

        self.timerWaitForUpdateData = QTimer(self)
        self.timerWaitForUpdateData.timeout.connect(self.HideWaitForUpdateDataScreen)

        self.FGPobj = Fingerprint()
        self.FGPobj.SignalRecognizedFGP.connect(self.RecognizedFGP)
        self.FGPobj.BatLayVanTayDangNhap()
        self.FGPobj.SignalFGPnotFind.connect(self.PlayNotRecognized)
        self.FGPobj.SignalHandPushed.connect(self.PlayBip)
        self.FGPobj.LayDanhSachIDvaVanTay()
        self.mainScreenObj.SignalCleanFGPsensor.connect(self.FGPobj.LamSachCamBien)

        self.rfModuleObj = ControlRFIDmudule()
        self.rfModuleObj.SignalRecognizedStudent.connect(self.RecognizedCard)
        self.rfModuleObj.SignalNotReconizedStudent.connect(self.PlayNotRecognized)
        self.rfModuleObj.lstStudent = self.lstStudent
        

        self.__FlagUpdateScreenIsShow = False
        self.__FlagNeedWaitContinue = False
        # self.socketServerForRFIDobj = SocketServerForRFID()
        # self.socketServerForRFIDobj.SignalRFIDputOn.connect(self.RFIDputOn)

        self.mainScreenObj.ShowCamera()

    def GoToTakeSampleScreen(self):
        pass

    def PlayBip(self):
        self.soundObj.ThreadPlayBip()

    def PlayNotRecognized(self):
        self.soundObj.ThreadPlayVuiLongThuLai()

    def DeleteAllData(self):
        try:
            KhoaThiRepository().xoaBanGhi(" 1 = 1 ")
            ThiSinhRepository().xoaBanGhi( " 1 = 1 " )
            LichSuRepository().xoaBanGhi(" 1 = 1 " )
            IDvaVanTayRepository().xoaBanGhi( " 1 = 1 ")
            self.FGPobj.XoaToanBoDatabase()
            self.lstStudent = []
            self.faceRecognitionObj.SetListStudent(self.lstStudent)
            self.FGPobj.lstIDvaVanTay = []
        except:
            pass


    def DeleteFGPofStudentInSensor(self, ID):
        lstIDvaVanTay = IDvaVanTayRepository().layDanhSach(" IDThiSinh = '%s' "%(ID))
        for IDvaVanTay in lstIDvaVanTay:
            self.FGPobj.XoaVanTayTrongCamBien(IDvaVanTay.ViTriVanTay)

    def GoToDesktop(self):
        desktop = {
            'destop':1,
        }
        with open("desktop.json", 'w') as fp:
            json.dump(desktop,fp)
        self.close()
        
    def Shutdown(self):
        os.system("shutdown now")
    
    def ShowWaitForUpdateDataScreen(self):
        if(self.__FlagUpdateScreenIsShow):
            self.__FlagNeedWaitContinue = True
            return
        self.__FlagUpdateScreenIsShow = True    
        self.__OffCameraTemporary(autoReopen= False)
        self.timerWaitForUpdateData.start(6000)
        self.mainScreenObj.ShowWaitForUpdateScreen()

    def HideWaitForUpdateDataScreen(self):
        if(self.__FlagNeedWaitContinue):
            #self.timerWaitForUpdateData.start(10000)
            self.__FlagNeedWaitContinue = False
        else:
            self.lstStudent = GetDataFromDatabase().GetListStudent()
            self.faceRecognitionObj.SetListStudent(self.lstStudent)
            self.rfModuleObj.lstStudent = self.lstStudent
            self.FGPobj.LayDanhSachIDvaVanTay()
            self.timerWaitForUpdateData.stop()
            self.mainScreenObj.HideWaitForUpdateScreen()
            self.__FlagUpdateScreenIsShow = False
            self.__ReopenReadCamera()

    def AddStudentInfomation(self, infoDict):
        self.ThemKhuonMatVaoDanhSachDaLay(infoDict["idStudent"], infoDict["faceEncodingArr"])
        self.faceRecognitionObj.SetListStudent(self.lstStudent)
        khoIDvaVanTay = IDvaVanTayRepository()
        for FGPfeature in infoDict["FGPencoding"]:
            try:
                viTri = self.FGPobj.NapVanTayTuThietBiVaoCamBien(FGPfeature)
            except:
                pass
            idVaVanTay = AnhXaIDvaVanTay()
            idVaVanTay.IDThiSinh = infoDict["idStudent"]
            idVaVanTay.ViTriVanTay = viTri
            khoIDvaVanTay.ghiDuLieu(idVaVanTay)
            self.FGPobj.ThemIDvaVanTayVaoDanhSachDaLay(infoDict["idStudent"], viTri)
    
    def RecognizedCard(self, student):
        self.__OffCameraTemporary(recBy= "card")
        self.mainScreenObj.ShowStudentInfomation(student)
        self.socketObject.SendResultsCardrecognition(student.ID)
        self.__SaveHistory("card", student.ID)
        self.soundObj.ThreadPlayXinCamOn()

    def RecognizedFGP(self, studentID):
        self.__OffCameraTemporary(recBy= "fgp")
        for student in self.lstStudent:
            if(student.ID == studentID):
                self.mainScreenObj.ShowStudentInfomation(student) 
                self.socketObject.SendResultsFGPrecognition(studentID)
                break
        self.__SaveHistory("FGP", studentID)
        self.soundObj.ThreadPlayXinCamOn()
        
    def __AddFaceEncodingAndFGP(self, faceDict, FGPdict):

        khoThiSinh = ThiSinhRepository()
        faceEncodeSendToServer = ""
        FGPencodeSendToServer = ""
        if(not len(faceDict["faceEncodingStr"]) == 0):
            khoThiSinh.capNhatTruong(("NhanDienKhuonMatThem", ), (faceDict["faceEncodingStr"], ), 'ID = "%s"'%(str(faceDict["student"].ID)))
            #self.ThemKhuonMatVaoDanhSachDaLay(faceDict["student"].ID, faceDict["faceEncodingArr"])
            faceEncodeSendToServer = faceDict["faceEncodingStr"]
            self.lstStudent = GetDataFromDatabase().GetListStudent()
            self.faceRecognitionObj.SetListStudent(self.lstStudent)
        if(not len(FGPdict["AllFeatureStr"])==0):
            khoThiSinh.capNhatTruong(("NhanDienVanTay", ), (FGPdict["AllFeatureStr"], ), 'ID = "%s"'%(str(faceDict["student"].ID)))
            khoIDvaVanTay = IDvaVanTayRepository()
            FGPencodeSendToServer = FGPdict["AllFeatureStr"]
            khoIDvaVanTay.xoaBanGhi( " IDThiSinh = '%s' "%(str(faceDict["student"].ID) ))
            for pos in FGPdict["ListPos"]:
                idVaVanTay = AnhXaIDvaVanTay()
                idVaVanTay.IDThiSinh = faceDict["student"].ID
                idVaVanTay.ViTriVanTay = pos
                khoIDvaVanTay.ghiDuLieu(idVaVanTay)
                #self.FGPobj.ThemIDvaVanTayVaoDanhSachDaLay(faceDict["student"].ID, pos)
            self.FGPobj.LayDanhSachIDvaVanTay()
 
        # self.faceRecognitionObj.SetListStudent(self.lstStudent)
        # self.mainScreenObj.databaseScreenObj.ShowAddDataDialog()
        if((faceEncodeSendToServer.__len__() == 0) & (FGPencodeSendToServer.__len__()==0)):
            return
        sendDict = {
            "ID":faceDict["student"].ID,
            "FaceEncoding":faceEncodeSendToServer,
            "FGPEncoding":FGPencodeSendToServer,
                     }
        self.socketObject.SendAddFaceAndFGP(sendDict)

    
    def ThemKhuonMatVaoDanhSachDaLay(self, idStudent, faceEncoding):
        for student in self.lstStudent:
            if(student.ID == idStudent):
                student.NhanDienKhuonMatThem.append(faceEncoding)
                return

    def __DeleteFaceAdded(self, idStudent):
        for student in self.lstStudent:
            if(student.ID == idStudent):
                student.NhanDienKhuonMatThem = ""
                return

    def __DeleteFGPadded(self):
        self.FGPobj.LayDanhSachIDvaVanTay()
   
    def __SettingScreenHiden(self):
        self.cameraObj.StartReadImage()
        # self.faceRecognitionObj.StartFaceTracking()
        self.faceRecognitionObj.StartFaceRecognize()
        self.FGPobj.BatLayVanTayDangNhap()

    def __ReopenReadCamera(self):
        if(self.__FlagUpdateScreenIsShow):
            return
        self.mainScreenObj.ShowCamera()
        self.mainScreenObj.ClearStudentRecognizedInfomation()
        self.cameraObj.StartReadImage()
        self.faceRecognitionObj.StartFaceRecognize()
        # self.faceRecognitionObj.StartFaceTracking()
        self.FGPobj.BatLayVanTayDangNhap()
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
        # self.faceRecognitionObj.StopFaceTracking()
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
        if(studentObj.ID.__contains__("EC_9999")):
            self.SearchStudentAndCheck(studentObj)
        self.__OffCameraTemporary(recBy= "face")
        self.soundObj.ThreadPlayXinCamOn()
        fp = open("imageTosend.jpg", 'wb')
        fp.write(faceImageJpgData)
        self.mainScreenObj.ShowStudentInfomation(studentObj)
        self.__SaveHistory("Face", studentObj.ID)
        # self.mainScreenObj.ShowFaceRecognizeOK()
        self.socketObject.SendResultsFaceRecognize(studentObj.ID, "T", "imageTosend.jpg")

    def __OffCameraTemporary(self, recBy = "face", autoReopen = True):
        self.FGPobj.TatLayVanTayDangNhap()
        self.cameraObj.StopReadImage()
        # self.faceRecognitionObj.StopFaceTracking()
        self.faceRecognitionObj.StopFaceRecognize()
        self.mainScreenObj.HideCamera(recBy)
        if(autoReopen):
            self.timerReopenReadCam.start(3000)
        

    def __ShowImageFromCamera(self, pixmap):
        self.mainScreenObj.label_showCamera.setPixmap(pixmap)

    def __SaveHistory(self, FGPorFace, IDThiSinh):
        lichSu = ThongTinLichSuDiemDanh()
        lichSu.IDThiSinh = IDThiSinh
        lichSu.KhuonMatHayVanTay = FGPorFace
        lichSu.ThoiGian = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        lichSu.Anh = b''
        self.khoLichSu.ghiDuLieu(lichSu)

    def SearchStudentAndCheck(self, teacher):
        pass

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowFlags(Qt.FramelessWindowHint)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
