from        UpdateScreen.UpdateScreenUI   import Ui_FrameContainUpdateScreen
from        PyQt5.QtCore    import pyqtSlot, pyqtSignal,QTimer, QDateTime,Qt, QObject
from        PyQt5.QtGui     import QPixmap
from        PyQt5           import QtWidgets, QtGui, QtCore
from        PIL             import Image, ImageQt
from        SocketConnect.FTPclient       import FTPclient
from        DatabaseAccess.DatabaseAccess    import *
import      io
from        CameraAndFaceRecognition.CameraAndFaceRecognition    import GetFaceEncodingFromImage
from        datetime        import datetime
import      threading
import      numpy

class UpdateScreen(QObject, Ui_FrameContainUpdateScreen):
    __SignalCountUpNumberUpdated = pyqtSignal()
    __SignalShowNumberStudent = pyqtSignal(int)
    __SignalCountUpNumberError = pyqtSignal()
    __SignalNoStudentForUpdate = pyqtSignal()
    def __init__(self, frame, filePath):
        QObject.__init__(self)
        Ui_FrameContainUpdateScreen.__init__(self)
        self.setupUi(frame)
        self.numberStudentError = 0
        self.numberStudent = 0
        self.numberStudentUpdated = 0
        self.label_forShowDataTime.setText(datetime.now().strftime("%d//%m//%Y %H/%M/%S"))
        frame.setGeometry((800 - frame.width())/2, (480 - frame.height())/2, frame.width(), frame.height())
        frame.show()
        self.label.setPixmap(QtGui.QPixmap("icon/iconStudentUpdate.png"))
        self.__DownLoadAndUpdateData(filePath)
        self.__SignalCountUpNumberUpdated.connect(self.__CountUpNumberUpdated)
        self.__SignalCountUpNumberError.connect(self.__CountUpNumberStudentError)
        self.__SignalShowNumberStudent.connect(self.__ShowNumberStudent)

    def __ShowNumberStudent(self, numberStudent):
        self.numberStudent = numberStudent
        self.label_forShowNumberStudent.setText(str(numberStudent))

    def __CountUpNumberUpdated(self):
        self.numberStudentUpdated += 1
        string = "%s/%s thí sinh"%(self.numberStudentUpdated, self.numberStudent)
        self.label_forShowNumberUpdated.setText(string)

    def __CountUpNumberStudentError(self):
        self.numberStudentError += 1
        string = "%s thí sinh"%(str(self.numberStudentError))
        self.label_forShowNumberError.setText(string)

    def __CreateCourse(self, filePath):
        khoaThi = ThongTinKhoaThi()
        khoaThi.NgayTao = datetime.now().strftime("%d//%m//%Y %H/%M/%S")
        khoaThi.DuongDanLuuAnh = filePath + "AnhThiSinh/"
        khoKhoaThi = KhoaThiRepository()
        return khoKhoaThi.ghiDuLieu(khoaThi)
        
    def __DownLoadAndUpdateData(self, ftpFileDir):
        try:
            ftpObj = FTPclient()
            IDKhoaThi = self.__CreateCourse(ftpFileDir)
            lstImage = ftpObj.GetListStudentImage(ftpFileDir)
            numberImage = len(lstImage)
            if(numberImage == 0):
                self.__SignalNoStudentForUpdate.emit()
            # self.__SignalShowNumberStudent.emit(numberImage)
            self.__ShowNumberStudent(numberImage)
            if(numberImage == 1):
                thread1 = threading.Thread(target = self.__ProcessImage, args=(lstImage, IDKhoaThi, 0, numberImage))
                thread1.start()
            else:
                thread1 = threading.Thread(target = self.__ProcessImage, args=(lstImage, IDKhoaThi, 0, int(numberImage/2)))   
                thread2 = threading.Thread(target = self.__ProcessImage, args=(lstImage, IDKhoaThi, int(numberImage/2), numberImage))
                thread1.start()
                thread2.start()
        except:
            pass
    
    def __ProcessImage(self, lstImage, IDKhoaThi, start, end):
            khoThiSinh = ThiSinhRepository()
            for i in range(start, end):
                try:
                    thiSinh = ThongTinThiSinh()
                    fp = open("DataUpdate/" + lstImage[i], 'rb')
                    thiSinh.AnhDangKy = fp.read()
                    image = Image.open(io.BytesIO(thiSinh.AnhDangKy))
                    image = image.convert("RGB")
                    npArrayImage = numpy.array(image)
                    thiSinh.NhanDienKhuonMatStr = GetFaceEncodingFromImage().GetFaceEncodingStr(npArrayImage)
                    thiSinh.IDKhoaThi = IDKhoaThi
                    thiSinh.MaDK = lstImage[i].split(".")[0]
                    khoThiSinh.ghiDuLieu(thiSinh)
                    self.__SignalCountUpNumberUpdated.emit()
                except:
                    self.__SignalCountUpNumberError.emit()


    def __ServerRequestUpdateDatabase(self, ftpFileDir):
        
        try:
            ftpObj = FTPclient()
            lstImage = ftpObj.GetListStudentImage(ftpFileDir)
            self.label_forShowNumberStudent.setText(len(lstImage))
            listHocVien = []
            
            for imageName in lstImage:
                try:
                    hocVien = ThongTinThiSinh()
                    fp = open(imageName +'.jpg', 'rb')
                    hocVien.AnhDangKy = fp.read()
                    image = Image.open(io.BytesIO(hocVien.AnhDangKy))
                    image = image.convert("RGB")
                    npArrayImage = numpy.array(image)
                    hocVien.NhanDienKhuonMatStr = GetFaceEncodingFromImage().GetFaceEncodingStr(npArrayImage)
                    hocVien.IDKhoaHoc = idKhoaHoc
                    hocVien.MaDK = imageName
                    listHocVien.append(hocVien)

                except:
                    print(imageName)
                    self.__CountUpNumberStudentError()
            khoThiSinh = ThiSinhRepository()
            for hocVien in listHocVien:
                khoThiSinh.ghiDuLieu(hocVien)

            # for imageAndXml in lstImageAndXMLfile:
            #     if(imageAndXml.__contains__(".xml") | imageAndXml.__contains__(".XML")):
            #         self.parseXMLobj = ParseXML()
            #         self.parseXMLobj.SignalNumberParsed.connect(self.__NumberStudentParsed)
            #         lstHocVienCongThem = self.parseXMLobj.ReadListStudentFromXML(imageAndXml)
            #         for hocVien in lstHocVienCongThem:
            #             listHocVien.append(hocVien)
            # khoThiSinh = ThiSinhRepository()
            # khoThiSinh.xoaBanGhi( " 1 = 1 ")
            # for hocVien in listHocVien:
            #     khoThiSinh.ghiDuLieu(hocVien)
            # global FTP_FILE_PATH_TO_UPLOAD
            # FTP_FILE_PATH_TO_UPLOAD = remoteUpdateDir + "AnhNhanDien/"
            # GetSetting.UpdateServerImageDir(FTP_FILE_PATH_TO_UPLOAD)
            # self.SignalUpdateDataBaseSuccess.emit(listHocVien)

        except:
            pass
    
    
