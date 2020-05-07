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
from        os                                  import path
from         FingerPrintSensor.FingerPrint      import Fingerprint
from         Sound.OrangePiSound                import Sound
from         WriteRFcard.ControlRFIDmodule      import ControlRFIDmudule
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
        self.__DisableLogo()
#region   dieu khien signal tu camera

        self.cameraObj.PixmapFromCamera.connect(self.__ShowImageFromCamera)
        self.cameraObj.CanNotConnectCamera.connect(self.__NoCameraMode)
        self.cameraObj.StartReadImage()
        self.cameraObj.SignalHideCamera.connect(self.__HideCamera)

        self.mainScreenObj.SignalStartReadImage.connect(self.cameraObj.ReadCameraForDT)
        self.mainScreenObj.SignalStopReadImage.connect(self.cameraObj.StopReadImageForDT)
        self.mainScreenObj.SignalFaceTracking.connect(self.cameraObj.FaceTrackingForDT)
        self.mainScreenObj.SignalGetFaceFeature.connect(self.cameraObj.GetFaceFeatureForDT)
        self.mainScreenObj.SignalCloseTakeSampleScreen.connect(self.CloseTakeSampleScreen)


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
        self.mainScreenObj.SignalRequestGetFGP.connect(self.FGPobj.GetFGPforDT)
        self.mainScreenObj.SignalStopGetFGP.connect(self.FGPobj.StopGetFGP)

        self.rfModuleObj = ControlRFIDmudule()
        self.rfModuleObj.SignalRecognizedStudent.connect(self.RecognizedCard)
        self.rfModuleObj.SignalNotReconizedStudent.connect(self.PlayNotRecognized)
        self.rfModuleObj.lstStudent = self.lstStudent
        
        self.mainScreenObj.SignalStartWriteRFcardDT.connect(self.rfModuleObj.WriteIDcardNumberForDT)
        self.mainScreenObj.SignalStopWriteRFcardDT.connect(self.rfModuleObj.StopWriteToCardDT)


        self.__FlagUpdateScreenIsShow = False
        self.__FlagNeedWaitContinue = False
        self.__FlagNoCameraMode = False
        self.__FlagSettingScreenShow = False
        # self.socketServerForRFIDobj = SocketServerForRFID()
        # self.socketServerForRFIDobj.SignalRFIDputOn.connect(self.RFIDputOn)
        
        self.mainScreenObj.ShowCamera()
    
    def __DisableLogo(self):
        if(not path.exists("../Setting/dlogo.json")):
            os.system("sh DisableLogo/disLogo.sh")
            with open('../Setting/dlogo.json', 'w') as json_file:
                dict = {
                    "disable":"1",
                }
                json.dump(dict, json_file)

    def CloseTakeSampleScreen(self):
        self.cameraObj.ResetSettingCameraForMainScreen()

    def GoToTakeSampleScreen(self):
        pass

    def PlayBip(self):
        self.soundObj.ThreadPlayBip()

    def __NoCameraMode(self):
        self.__FlagNoCameraMode = True
        self.mainScreenObj.flagNoCameraMode = True
        self.mainScreenObj.ShowCanNotConnectCamera()
        self.faceRecognitionObj.StopFaceRecognize()
        self.cameraObj.StopReadImage()

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
        return
        
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
            if(not self.__FlagSettingScreenShow):
                self.__ReopenReadCamera()
            

    def AddStudentInfomation(self, infoDict):
        try:
            self.ThemKhuonMatVaoDanhSachDaLay(infoDict["idStudent"], infoDict["faceEncodingArr"])
            self.faceRecognitionObj.SetListStudent(self.lstStudent)
            khoIDvaVanTay = IDvaVanTayRepository()
            if(len(infoDict["FGPencoding"]) == 0):
                self.__AddSuccessOrError("er >>noFGP>> ID = " + infoDict["idStudent"])
            else:
                khoIDvaVanTay.xoaBanGhi(" IDThiSinh = %s "%(infoDict["idStudent"]))
                for FGPfeature in infoDict["FGPencoding"]:
                    try:
                        viTri = self.FGPobj.NapVanTayTuThietBiVaoCamBien(FGPfeature)
                        idVaVanTay = AnhXaIDvaVanTay()
                        idVaVanTay.IDThiSinh = infoDict["idStudent"]
                        idVaVanTay.ViTriVanTay = viTri
                        
                        khoIDvaVanTay.ghiDuLieu(idVaVanTay)
                        self.FGPobj.ThemIDvaVanTayVaoDanhSachDaLay(infoDict["idStudent"], viTri)
                        self.__AddSuccessOrError("er >>fgpAdded>>" + "ID = " + infoDict["idStudent"])
                    except Exception as ex:
                        self.__AddSuccessOrError("er >>fgpAddEr>>+"+str(ex.args)+ "ID = " + infoDict["idStudent"])
        except:
            pass
    
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
        try:
            for student in self.lstStudent:
                if(student.ID == idStudent):
                    student.NhanDienKhuonMatThem.append(faceEncoding)
                    if(len(faceEncoding) == 0):
                        self.__AddSuccessOrError("er >> notFace >> ID = "+ student.ID)
                        
                    else:
                        self.__AddSuccessOrError("suc >> addFace >> ID = "+ student.ID)
                    return
            self.__AddSuccessOrError("er >> stNotMatch >> ID = "+ student.ID)
        except:
            pass

    def __DeleteFaceAdded(self, idStudent):
        for student in self.lstStudent:
            if(student.ID == idStudent):
                student.NhanDienKhuonMatThem = ""
                return

    def __AddSuccessOrError(self, errStr):
        self.socketObject.SendLogError(errStr)

    def __DeleteFGPadded(self):
        self.FGPobj.LayDanhSachIDvaVanTay()
   
    def __SettingScreenHiden(self):
        
        # if(not self.__FlagNoCameraMode):
        #     self.cameraObj.StartReadImage()
        #     # self.faceRecognitionObj.StartFaceTracking()
        #     self.faceRecognitionObj.StartFaceRecognize()
        # self.FGPobj.BatLayVanTayDangNhap()
        # self.rfModuleObj.StartReadDataInCard()
        self.__FlagSettingScreenShow = False
        self.__ReopenReadCamera()

    def __ReopenReadCamera(self):
        if(self.__FlagUpdateScreenIsShow):
            return
        if(not self.__FlagNoCameraMode):
            self.cameraObj.StartReadImage()
            self.mainScreenObj.ShowCamera()
            self.faceRecognitionObj.StartFaceRecognize()
        else:
            self.mainScreenObj.ShowCamera()
            self.mainScreenObj.ShowCanNotConnectCamera()
        self.mainScreenObj.ClearStudentRecognizedInfomation()
        # self.faceRecognitionObj.StartFaceTracking()
        self.FGPobj.BatLayVanTayDangNhap()
        self.timerReopenReadCam.stop()
        self.rfModuleObj.StartReadDataInCard()
    
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
        if(not self.__FlagNoCameraMode):
            self.cameraObj.StartReadImage()
            self.faceRecognitionObj.StartFaceRecognize()
            
        # self.mainScreenObj.fateScreen()

    def WaitForUpdateDatabase(self, filePath):
        self.faceRecognitionObj.StopFaceRecognize()
        self.cameraObj.StopReadImage()
        self.mainScreenObj.ShowUpdateScreen(filePath)
        self.rfModuleObj.StopReadDataInCard()

    def __GetPassword(self):
        self.mainScreenObj.ShowInputPasswordScreen()

    def __ShowSettingScreen(self):
        self.__FlagSettingScreenShow = True
        self.faceRecognitionObj.StopFaceRecognize()
        # self.faceRecognitionObjfaceRecognitionObj.StopFaceTracking()
        self.FGPobj.TatLayVanTayDangNhap()
        self.cameraObj.StopReadImage()
        self.rfModuleObj.StopReadDataInCard()
        self.mainScreenObj.ShowSettingScreen()

    def ServerNotConnect(self):
        # self.cameraObj.StopReadImage()
        self.mainScreenObj.ShowNotConnect()

    def ServerConnected(self):
        # self.cameraObj.StartReadImage()
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
        if(studentObj.ID.__contains__("ELT")):
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
        try:
            teacherID = int(teacher.ID.split("_")[1])
            teacherStudentRepo = DanhSachThiSinhTuongUngTaiKhoanRepository()
            lstTeacherStudent = teacherStudentRepo.layDanhSach(" IDTaiKhoanQuanLy = %s "%(teacherID))
            for teacherStudent in lstTeacherStudent:
                self.socketObject.SendResultsFGPrecognition(teacherStudent.IDthiSinh)
        except Exception as ex:
            print(ex)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowFlags(Qt.FramelessWindowHint)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
