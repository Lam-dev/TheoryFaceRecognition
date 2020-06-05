from    FingerPrintSensor.FingerprintLib    import PyFingerprint
from    PyQt5.QtCore       import QRect, QPropertyAnimation, QTimer, pyqtSignal, pyqtSlot, QObject
from    DatabaseAccess.DatabaseAccess   import *
import  time
from    PIL import Image
import  _thread
from    DatabaseAccess.DatabaseAccess     import *
import  threading
from    GetSettingFromJSON    import GetSetting

# SETTING_DICT  = GetSetting.LoadSettingFromFile()
# try:
#     SCURITY_LEVEL = SETTING_DICT["FGPscuLevel"]
# except:
SCURITY_LEVEL = 1

class Fingerprint(QObject):
    SignalNewFGPadded = pyqtSignal(int, list)
    SignalRecognizedFGP = pyqtSignal(str)
    SignalFGPnotFind = pyqtSignal()
    SignalHandPushed = pyqtSignal()

    SignalDowloadedImage = pyqtSignal(str)
    SignalFGPget = pyqtSignal(str)
    SignalFGPputOnIsTheSame = pyqtSignal()
    
    

    def __init__(self, port = '/dev/ttyACM0', baudRate = 57600, address = 0xFFFFFFFF, password = 0xFFFFFFFF):
        super().__init__()
        self.port = port
        self.baudRate = baudRate
        self.address = address
        self.password = password
        try:
            global SCURITY_LEVEL
            self.fingerprintObj = PyFingerprint(port, baudRate, address, password)
            self.fingerprintObj.setSecurityLevel(SCURITY_LEVEL)
            # self.fingerprintObj.verifyPassword()
        except:
            self.fingerprintObj = False
        
        self.TimerThemVanTay = QTimer()
        self.TimerThemVanTay.timeout.connect(self.ThemVanTay)
        self.TimerLayVanTayDangNhap = QTimer()
        self.TimerLayVanTayDangNhap.timeout.connect(self.ThreadLayVanTayDangNhap)
        self.lstIDvaVanTay = []
        self.viTriDaChonChuaLuu = []
        self.LayDanhSachIDvaVanTay()
        self.FlagFGPfree = True

        self.timerGetFGPfeature = QTimer()
        self.timerGetFGPfeature.timeout.connect(self.ThreadGetFGPfeature)
        self.viTriDaChonChuaLuu = []
        self.__FlagLockFGPsensor = False

        self.FGPgetCallback = object
    
    def setSecurityLevel(self, level):
        global SCURITY_LEVEL
        SCURITY_LEVEL = level
        self.fingerprintObj.setSecurityLevel(SCURITY_LEVEL)

    def XoaVanTayTrongCamBien(self, viTri):
        try:
            self.fingerprintObj.deleteTemplate(viTri)
        except:
            pass

    def LamSachCamBien(self):
        lstIDvaVanTay = IDvaVanTayRepository().layDanhSach(" 1 = 1 ")
        for idVaVanTay in lstIDvaVanTay:
            studentExist = ThiSinhRepository().layDanhSach( " ID = '%s' "%(idVaVanTay.IDThiSinh))
            if(len(studentExist) == 0):
                IDvaVanTayRepository().xoaBanGhi( " IDThiSinh = '%s' "%(idVaVanTay.IDThiSinh))
                self.fingerprintObj.deleteTemplate(idVaVanTay.ViTriVanTay)

    def LayDanhSachIDvaVanTay(self):
        khoIDvaVanTay = IDvaVanTayRepository()
        self.lstIDvaVanTay = khoIDvaVanTay.layDanhSach(" 1 = 1 ")

    def ThemIDvaVanTayVaoDanhSachDaLay(self, IDthiSinh, viTriVanTay):
        idVaVanTay = AnhXaIDvaVanTay()
        idVaVanTay.IDThiSinh = IDthiSinh
        idVaVanTay.ViTriVanTay = viTriVanTay
        self.lstIDvaVanTay.append(idVaVanTay)

    def LayLaiDanhSachIDvaVanTay(self, IDthiSinh):
        khoIDvaVanTay = IDvaVanTayRepository()
        self.lstIDvaVanTay = khoIDvaVanTay.layDanhSach( " 1 = 1 ")

    def BatThemVanTay(self):
        if(not self.TimerThemVanTay.isActive()):
            self.TimerThemVanTay.start(300)
            
    def TatThemVanTay(self):
        if(self.TimerThemVanTay.isActive()):
            self.TimerThemVanTay.stop()
    
    def BatLayVanTayDangNhap(self):
        self.TimerLayVanTayDangNhap.stop()
        self.TimerLayVanTayDangNhap.start(1500)
    
    def TatLayVanTayDangNhap(self):
        if(self.TimerLayVanTayDangNhap.isActive()):
            self.TimerLayVanTayDangNhap.stop()

    def XoaToanBoDatabase(self):
        try:
            self.fingerprintObj.clearDatabase()
        except:
            pass

    def ThemVanTay(self):
        
        try:
            if(type(self.fingerprintObj) is not bool):
                if(self.fingerprintObj.readImage()):
                    self.SignalHandPushed.emit()
                    self.fingerprintObj.convertImage(0x01)
                    self.fingerprintObj.readImage()
                    self.fingerprintObj.convertImage(0x02)
                    if(self.fingerprintObj.compareCharacteristics() > 0):
                        result = self.fingerprintObj.searchTemplate()
                        
                        dacTrungVanTay = self.fingerprintObj.downloadCharacteristics(0x01)
                        if(result[0] > 0):
                            viTriLuu = result[0]
                        else:
                            viTriLuu = self.TimKhoangTrong()
                        self.fingerprintObj.storeTemplate(viTriLuu, 0x01)
                        self.SignalNewFGPadded.emit(viTriLuu, dacTrungVanTay)
            else:
                global SCURITY_LEVEL
                self.fingerprintObj = PyFingerprint(self.port, self.baudRate, self.address, self.password)
                self.fingerprintObj.setSecurityLevel(SCURITY_LEVEL)
                self.fingerprintObj.verifyPassword()
        except:
            self.fingerprintObj = False
    
    def NapVanTayTuThietBiVaoCamBien(self, FGPencoding):
        try:
            self.fingerprintObj.uploadCharacteristics(characteristicsData= FGPencoding)
            result = self.fingerprintObj.searchTemplate()
            if(result[0] >= 0):
                viTriLuu = result[0]
            else:
                viTriLuu = self.TimKhoangTrong()
            self.fingerprintObj.storeTemplate(viTriLuu, 0x01)
            return viTriLuu
        except Exception as ex:
            raise Exception(ex.args)

    def TimViTriLuu(self):
        for i in range(0,4):
            lstViTri =  self.fingerprintObj.getTemplateIndex(i)
            for j in range(0, len(lstViTri)):
                if(not lstViTri[j]):
                    return 256*i+j
        return False
    
    # def TimKhoangTrong(self):
    #     for i in range(self.ViTriDaTimDen, len(self.lstIDvaVanTay)):
    #         if(self.lstIDvaVanTay[i].Vi_Tri_Van_Tay != i):
    #             self.ViTriDaTimDen = i + 1
    #             return i
    #     self.ViTriDaTimDen = len(self.lstIDvaVanTay) + 1
    #     return len(self.ViTriDaTimDen)
    def TimKhoangTrong(self):
        dsIDvaVanTay = self.lstIDvaVanTay
        dsIDvaVanTay.sort(key = lambda idVaVanTay: idVaVanTay.ViTriVanTay)
        if((len(dsIDvaVanTay) == 0) & (len(self.viTriDaChonChuaLuu) == 0)):
            self.viTriDaChonChuaLuu.append(0)
            return 0
        for i in range(0, len(dsIDvaVanTay)):
            if((dsIDvaVanTay[i].ViTriVanTay != i) & (not self.viTriDaChonChuaLuu.__contains__(i))):
                self.viTriDaChonChuaLuu.append(i)
                return i
        if(len(dsIDvaVanTay) == 0):
            viTriTiepTheo = len(self.viTriDaChonChuaLuu)
            self.viTriDaChonChuaLuu.append(viTriTiepTheo)
            return viTriTiepTheo
        else:
            viTriTiepTheo = dsIDvaVanTay[len(dsIDvaVanTay)-1].ViTriVanTay + 1 + len(self.viTriDaChonChuaLuu)
            self.viTriDaChonChuaLuu.append(viTriTiepTheo)
            return viTriTiepTheo
        # self.viTriDaChonChuaLuu.append(len(dsIDvaVanTay))
        # return len(dsIDvaVanTay)
            

    # def TimViTriTrongTrongDatabase(self):
    #     lstIDvaVanTay = DatabaseAccecss.LayDSIDvaVanTay()
    #     lstIDvaVanTay.sort(lambda: )
    #     for i in range(0, 5000):

    def ThreadLayVanTayDangNhap(self):
        if(self.FlagFGPfree):
            self.FlagFGPfree = False
            thread = threading.Thread(target = self.LayVanTayDangNhap, args=(), daemon= True)
            thread.start()
    
    def LayVanTayDangNhap(self):
        
        try:
            if(self.fingerprintObj.readImage()):
                self.fingerprintObj.convertImage(0x01)
                
                ketqua = self.fingerprintObj.searchTemplate()
                self.SignalHandPushed.emit()
                print(ketqua)
                print("ket qua = %s"%(ketqua[0]))
                if(len(ketqua) == 2):
                    for idVaVanTay in self.lstIDvaVanTay:
                        if(idVaVanTay.ViTriVanTay == ketqua[0]):
                            self.SignalRecognizedFGP.emit(idVaVanTay.IDThiSinh)
                            self.FlagFGPfree = True
                            return
                self.SignalFGPnotFind.emit()

        except:
            try:
                self.fingerprintObj = PyFingerprint(self.port, self.baudRate, self.address, self.password)
            except:
                pass
        self.FlagFGPfree = True

    def NapLaiDuLieuChoCamBienVanTay(self):
        
        try:
            if(type(self.fingerprintObj) is not bool):
                self.XoaToanBoDatabase()
                dsIDvaVTvanTay = DatabaseAccecss.LayDSIDvaVanTay()
                khoThiSinh = ThiSinhRepository()
                for IDvaVTvanTay in dsIDvaVTvanTay:
                    vanTay = khoThiSinh.LayDuLieuTaiTruong(("Nhan_Dien_Van_Tay",), "ID_Thi_Sinh = %s"%(IDvaVTvanTay.ID_Thi_Sinh))
                    try:
                        print(vanTay)
                        if(type(vanTay[0][0]) is str):
                            lstVanTayStr = vanTay[0][0].split(",")
                            lstVanTayFloat = [int(elem) for elem in lstVanTayStr]
                            self.fingerprintObj.uploadCharacteristics(characteristicsData=lstVanTayFloat)
                            self.fingerprintObj.storeTemplate(positionNumber = IDvaVTvanTay.Vi_Tri_Van_Tay)
                    except:
                        pass
        except:
            pass
    
    def ThreadGetFGPfeature(self):
        if(self.FlagFGPfree):
            self.FlagFGPfree = False
            thread = threading.Thread(target = self.GetFGPfeature_DT)
            thread.start()
    
    def StartGetFGP(self):
        self.timerGetFGPfeature.start(700)
    
    def StopGetFGP(self):
        self.timerGetFGPfeature.stop()

    # def StartDownloadImage(self):
    #     self.timerDownloadFGPimage.start(1000)
    
    # def StopDownloadImage(self):
    #     self.timerDownloadFGPimage.stop()

    def ThreadDownloadFGPimage(self):
        if(self.FlagFGPfree):
            self.FlagFGPfree = False
            thread = threading.Thread(target = self.GetFGPfeature, args=(), daemon= True)
            thread.start()

    def DownloadFGPimage(self):
        try:
            if(type(self.fingerprintObj) is not bool):
                if(self.fingerprintObj.readImage()):
                    imageName = datetime.now().strftime("%H_%M_%S")+".bmp"
                    imageDir = os.getcwd() + "/" + imageName
                    self.fingerprintObj.downloadImage(imageDir)
                    self.SignalDowloadedImage.emit(imageName)
            else:
                self.fingerprintObj = PyFingerprint(self.port, self.baudRate, self.address, self.password)
                self.fingerprintObj.verifyPassword()
        except:
            self.fingerprintObj = False
        self.FlagFGPfree = True        

    def ClearFGPfeatureSaveOnSensor(self):
        try:
            self.fingerprintObj.clearDatabase()
        except:
            pass


    def GetFGPforDT(self, callback):
        self.FGPgetCallback = callback
        self.StartGetFGP()

    def GetFGPfeature_DT(self):
        try:
            if(self.fingerprintObj.readImage()):
                self.fingerprintObj.convertImage(0x01)
                self.fingerprintObj.readImage()
                self.fingerprintObj.convertImage(0x02)
                # self.SignalHandPushed.emit()
                # theSame = self.fingerprintObj.searchTemplate()
                # if(theSame[0] == -1):
                if(self.fingerprintObj.compareCharacteristics() > 0):
                    lstFGPfeature = self.fingerprintObj.downloadCharacteristics(0x02)
                    # self.fingerprintObj.storeTemplate()
                    lstFGPfeatureStrElem = [str(elem) for elem in lstFGPfeature]
                    FGPfeatureString = ",".join(lstFGPfeatureStrElem)
                    self.FGPgetCallback(FGPfeatureString)
                
                    
                # else:
                #     self.SignalFGPputOnIsTheSame.emit()


        except Exception as ex:
            self.FlagFGPfree = True
            # self.fingerprintObj = False
        self.FlagFGPfree = True
