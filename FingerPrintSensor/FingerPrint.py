from    FingerPrintSensor.FingerprintLib    import PyFingerprint
from    PyQt5.QtCore       import QRect, QPropertyAnimation, QTimer, pyqtSignal, pyqtSlot, QObject
from    DatabaseAccess.DatabaseAccess   import *
import  time
from    PIL import Image
import  _thread
from    DatabaseAccess.DatabaseAccess     import *
import  threading
from    GetSettingFromJSON    import GetSetting

SETTING_DICT  = GetSetting.LoadSettingFromFile()
try:
    SCURITY_LEVEL = SETTING_DICT["FGPscuLevel"]
except:
    SCURITY_LEVEL = 3

class Fingerprint(QObject):
    SignalNewFGPadded = pyqtSignal(int, list)
    SignalRecognizedFGP = pyqtSignal(str)
    SignalFGPnotFind = pyqtSignal()
    SignalHandPushed = pyqtSignal()
    

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
        except:
            return -1

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
                self.SignalHandPushed.emit()
                self.fingerprintObj.convertImage(0x01)
                
                ketqua = self.fingerprintObj.searchTemplate()
                print("ket qua = %s"%(ketqua[0]))
                if(len(ketqua) == 2):
                    for idVaVanTay in self.lstIDvaVanTay:
                        if(idVaVanTay.ViTriVanTay == ketqua[0]):
                            self.SignalRecognizedFGP.emit(idVaVanTay.IDThiSinh)
                            self.FlagFGPfree = True
                            return
                self.SignalFGPnotFind.emit()

        except:
            self.fingerprintObj = PyFingerprint(self.port, self.baudRate, self.address, self.password)
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

# x = Fingerprint()
# x.XoaToanBoDatabase()
# x.NapLaiDuLieuChoCamBienVanTay()
# print(x.fingerprintObj.getTemplateCount())
# x.XoaToanBoDatabase()
# x.fingerprintObj.clearDatabase()
# while True:
#     x.ThemVanTay()
# x.Thread_ThemVanTay()
# while True:
# x = [1, 3, 4, 5, 12]
# print(x)
# print(x.__contains__(2))
