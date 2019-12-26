import math
from    PyQt5.QtCore            import pyqtSlot, pyqtSignal,QTimer, QDateTime,Qt, QObject
from    SocketConnect.FTPclient import FTPclient 
from    CameraAndFaceRecognition.CameraAndFaceRecognition     import GetFaceEncodingFromImage
from    DatabaseAccess.DatabaseAccess    import *
from    GetSettingFromJSON      import GetSetting
import  json
from    collections import namedtuple
import  numpy
from    PIL         import Image
import io

CODE_RECIPT_DATA_FROM_SERVER = "3"
CODE_UPLOAD_DATA_TO_SERVER = "2"
CODE_PING_PING = "1"

MAC_ADDRESS_LENGTH                                  = 8
LOCAL_PATH_CONTAIN_DATA_UPDATE                      = "DataUpdate/"
FTP_FILE_PATH_TO_UPLOAD                             = GetSetting.GetSetting("--ServerImageDir")

class ProcessReciptData(QObject):
    ShowStudentForConfirm = pyqtSignal(str)
    ServerRequestTakePicture = pyqtSignal()
    ServerConfirmedConnect = pyqtSignal()
    ResponseRequestUpdataFromServer = pyqtSignal(str)
    SignalUpdateDataBaseSuccess = pyqtSignal(list)
    SignalNumberStudentParsed = pyqtSignal(int, int)

    def __init__(self):
        super().__init__()
        # self.ftpObj = FTPclient()

    def _json_object_hook(self, d): return namedtuple('X', d.keys())(*d.values())

    def json2obj(self, data): return json.loads(data, object_hook=self._json_object_hook)
    
    def ProcessDataFrame(self, khungNhan):
        try:
                reciptObj = self.json2obj(self.__CatLayPhanDataTrongFrame(khungNhan))

                if(reciptObj.code == CODE_RECIPT_DATA_FROM_SERVER):
                    self.__ProcessRequestUpdateDatabase(reciptObj)

                elif(reciptObj.code == CODE_UPLOAD_DATA_TO_SERVER):
                    self.ServerRequestTakePicture.emit()
                
                elif(reciptObj.code == CODE_PING_PING):
                    self.__ServerAcceptConnect(self.__CatLayPhanDataTrongFrame(khungNhan))

        except:
            pass
    
    def __ServerAcceptConnect(self, frame):
        self.ServerConfirmedConnect.emit()

    def __ServerRequestUpdateDatabase(self, ftpFileDir):
#region truong hop khong doc duoc anh tu xml
        # readFaceEncodingObj = GetFaceEncodingFromImage()

        # lstImageDir = self.ftpObj.GetListStudentImage()
        # lstStudent = []
        # for imageDir in lstImageDir:
        #     if(imageDir.__contains__("/")):
        #         parts = imageDir.split("/")
        #         maDK = (parts[len(parts) - 1].split("."))[0]
        #     else:
        #         maDK = imageDir.split(".")[0]
        #     studentObj = ThongTinThiSinh()
            
        #     encoding, encodingStr = readFaceEncodingObj.GetFaceEncodingFromImageFile(image)

        #     if(type(encoding) is not bool):
        #         lstStudent.append(studentObj)
#endregion
#region Truong hop lay thong tin thi sinh tu xml
        try:
            ftpObj = FTPclient()
            lstImageAndXMLfile = ftpObj.GetListStudentImage(ftpFileDir)
            listHocVien = []
            for imageAndXml in lstImageAndXMLfile:
                if(imageAndXml.__contains__(".xml") | imageAndXml.__contains__(".XML")):
                    self.parseXMLobj = ParseXML()
                    self.parseXMLobj.SignalNumberParsed.connect(self.__NumberStudentParsed)
                    lstHocVienCongThem = self.parseXMLobj.ReadListStudentFromXML(imageAndXml)
                    for hocVien in lstHocVienCongThem:
                        listHocVien.append(hocVien)
            khoThiSinh = ThiSinhRepository()
            khoThiSinh.xoaBanGhi( " 1 = 1 ")
            for hocVien in listHocVien:
                khoThiSinh.ghiDuLieu(hocVien)
            global FTP_FILE_PATH_TO_UPLOAD
            FTP_FILE_PATH_TO_UPLOAD = remoteUpdateDir + "AnhNhanDien/"
            GetSetting.UpdateServerImageDir(FTP_FILE_PATH_TO_UPLOAD)
            self.SignalUpdateDataBaseSuccess.emit(listHocVien)

        except NameError as e:
            print(e)
            pass
# #endregion 
        # try:
        #     ftpObj = FTPclient()
        #     lstImage = ftpObj.GetListStudentImage(ftpFileDir)
        #     lstStudent = []
        #     for image in lstImage:
        #         student = ThongTinThiSinh()
        #         fp = open(LOCAL_PATH_CONTAIN_DATA_UPDATE + image + '.jpg', 'rb')
        #         hocVien.AnhDangKy = fp.read()
        #         image = Image.open(io.BytesIO(hocVien.AnhDangKy))
        #         image = image.convert("RGB")
        #         npArrayImage = numpy.array(image)
        #         hocVien.NhanDienKhuonMatStr = GetFaceEncodingFromImage().GetFaceEncodingStr(npArrayImage)

    def __NumberStudentParsed(self, number, all):
        self.SignalNumberStudentParsed.emit(number, all)

    def __ProcessRequestUpdateDatabase(self, reciptObj):
        lstStudent = reciptObj.data.CardNumber
        if(len(lstStudent) == 0):
            return
        if(reciptObj.data.action == "update"):
            self.__AddStudent(lstStudent)
        elif(reciptObj.data.action == "getBy"):
            pass
        elif(reciptObj.data.action == "getAll"):
            pass
        elif(reciptObj.data.action == "deleteBy"):
            self.__DeleteStudentByNumber(lstStudent)
        elif(reciptObj.data.action == "deleteAll"):
            self.__DeleteAllStudent()
        
    def __AddStudent(self, lstStudentNumber):
        lstImage = []
        for stNumber in lstStudentNumber:
            lstImage.append(stNumber+".jpg")
        ftpObj = FTPclient()
        lstImageGrapped = ftpObj.GetListFileFromServer(lstImage)
        khoThiSinh = ThiSinhRepository()
        for image in lstImage:
            try:
                student = ThongTinThiSinh()
                fp = open(LOCAL_PATH_CONTAIN_DATA_UPDATE + image, 'rb')
                student.ID = image.split(".")[0]
                student.AnhDangKy = fp.read()
                image = Image.open(io.BytesIO(student.AnhDangKy))
                image = image.convert("RGB")
                npArrayImage = numpy.array(image)
                student.NhanDienKhuonMatStr = GetFaceEncodingFromImage().GetFaceEncodingStr(npArrayImage)
                khoThiSinh.ghiDuLieu(student)
                del student
            except:
                pass
    
    def __DeleteStudentByNumber(self, lstStudentNumber):
        khoThiSinh = ThiSinhRepository()
        for stNumber in lstStudentNumber:
            try:
                khoThiSinh.xoaBanGhi(" ID = %s "%(stNumber))
            except:
                pass
    
    def __DeleteAllStudent(self):
        khoThiSinh = ThiSinhRepository()
        khoThiSinh.xoaBanGhi(" 1 = 1 ")
           

    def __CatLayPhanDataTrongFrame(self, frameNhan):
        lstChar = []
        j = 0
        for byte in frameNhan:
            lstChar.append("")
            lstChar[j] = chr(byte)
            j += 1
            chuoiDuLieu = ''.join(lstChar)
        return chuoiDuLieu
