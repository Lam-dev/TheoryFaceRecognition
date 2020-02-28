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
from    datetime    import datetime
import  io
import  os

CODE_GET_DATABASE = "4"
CODE_RECIPT_DATA_FROM_SERVER = 3
CODE_UPLOAD_DATA_TO_SERVER = "2"
CODE_PING_PING = 1

MAC_ADDRESS_LENGTH                                  = 8
LOCAL_PATH_CONTAIN_DATA_UPDATE                      = "DataUpdate/"
FTP_FILE_PATH_TO_UPLOAD                             = GetSetting.GetSetting("--ServerImageDir")
FTP_SERVER_SYNC_DIR                                = "files/"

class ProcessReciptData(QObject):
    ShowStudentForConfirm = pyqtSignal(str)
    ServerRequestTakePicture = pyqtSignal()
    ServerConfirmedConnect = pyqtSignal()
    ResponseRequestUpdataFromServer = pyqtSignal(str)
    SignalUpdateDataBaseSuccess = pyqtSignal(list)
    SignalNumberStudentParsed = pyqtSignal(int, int)
    SignalSendFile = pyqtSignal(str)
    SignalSendMessage = pyqtSignal(str)
    SignalUpdateOrSyncStudentInfo = pyqtSignal(dict)
    SignalStopForUpdateData = pyqtSignal()
    __FlagTimeUpdated = False

    def __init__(self):
        super().__init__()
        # self.ftpObj = FTPclient()

    def _json_object_hook(self, d): return namedtuple('X', d.keys())(*d.values())

    def json2obj(self, data): return json.loads(data, object_hook=self._json_object_hook, encoding= "utf-8")
    
    def ProcessDataFrame(self, khungNhan):
        try:
            data = self.__CatLayPhanDataTrongFrame(khungNhan)
            reciptObj = self.json2obj(data)

            if(reciptObj.code == CODE_RECIPT_DATA_FROM_SERVER):
                self.SignalStopForUpdateData.emit()
                self.__ProcessRequestUpdateDatabase(reciptObj)
            
            elif(reciptObj.code == CODE_UPLOAD_DATA_TO_SERVER):
                self.ServerRequestTakePicture.emit()
                
            elif(reciptObj.code == CODE_PING_PING):
                self.__ServerAcceptConnect(reciptObj)
                
            elif(reciptObj.code == CODE_GET_DATABASE):
                self.__ServerRequestDatabaseCheck(reciptObj)
        
        except:

            pass

    def __ServerAcceptConnect(self, messageObj):
        self.ServerConfirmedConnect.emit()
        if(not self.__FlagTimeUpdated):
            strTime = messageObj.data.time
            try:
                os.system('date +%Y/%m/%d -s ' + '"%s"'%(strTime.split(" ")[0]))
                os.system('date +%T -s ' +'"%s"'%(strTime.split(" ")[1]))
                self.__FlagTimeUpdated = True
            except:
                pass

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

    def __ServerRequestDatabaseCheck(self, messageObj):
        target = messageObj.target
        if(target == "listCourse"):
            khoKhoaThi = KhoaThiRepository()
            lstKhoaThi = khoKhoaThi.layDanhSach(" 1 = 1 ")
            listCourseID = []
            for khoaThi in lstKhoaThi:
                listCourseID.append(khoaThi.IDKhoaThi)
            jsonSaveIntoFile = {
                "MAC":"12345",
                "ListCourse":listCourseID,
            }
            fileName  = "DSKT_" + datetime.now().strftime("%d_%m%_Y-%H_%M_%S")+".json"
            with open(fileName, 'w') as outfile:
                json.dump(jsonSaveIntoFile, outfile)
            messageForSendToServer = {
                "MAC":"12345",
                "code":CODE_GET_DATABASE,
                "target":target,
                "fileName":fileName,
                "checkSum":""
            }
            self.SignalSendFile.emit(fileName)
            self.SignalSendMessage.emit(json.dumps(messageForSendToServer))
    
        elif(target == "listStudent"):
            try:
                course = messageObj.detail["course"]
                khoThiSinh = ThiSinhRepository()
                lstThiSinh = khoThiSinh.layDanhSach(" IDKhoaThi = %s"%(course))
                listStudentID = []
                for thiSinh in lstThiSinh:
                    listStudentID.append("thiSinh.ID")
                jsonSaveIntoFile = {
                    "MAC":"12345",
                    "Course":"",
                    "ListStudent":listStudentID,
                    }
                fileName  = datetime.now().strftime("%d_%m_%Y-%H_%M_%S")+".json"
                with open(fileName, 'w') as outfile:
                    json.dump(jsonSaveIntoFile, outfile)

                messageForSendToServer = {
                    "MAC":"12345",
                    "code":CODE_GET_DATABASE,
                    "target":target,
                    "fileName":fileName,
                    "checkSum":""
                }
                
                self.SignalSendFile.emit(fileName)
                self.SignalSendMessage(messageForSendToServer)
            except:
                pass

        elif(target == "deleteCourse"):
            course = messageObj.detail["course"]
            khoThiSinh = ThiSinhRepository()
            khoThiSinh.xoaBanGhi(" IDKhoaThi = %s "%(course))
            khoKhoaThi = messageObj.detail["course"]
            khoKhoaThi.xoaBanGhi(" IDKhoaThi = %s"%( "IDKhoaThi  = %s"%(course)))
        
        elif(target == "getHistory"):
            courseID = messageObj.detail["course"]
            lstStudentOfCourse = ThiSinhRepository().layDanhSach(" IDkhoaThi = courseID ")
            historyRepo = LichSuRepository()

            for student in lstStudentOfCourse:
                lstHistoryOfStudent = historyRepo.layDanhSach(" IDThiSinh = student.IDThiSinh ")
            

        
            
        # detailForGetListStudent = {
        #     "course":"id Khoa hoc"
        # }        
                
        # databaseCheck = {
        #     "code" : "4",
        #     "target":"listCourse",
        #     "detail": ,
        #     "checksum":,
        # } 
        

    def __NumberStudentParsed(self, number, all):
        self.SignalNumberStudentParsed.emit(number, all)

    def __ProcessRequestUpdateDatabase(self, reciptObj):
        
        if(reciptObj.data.action == "update"):
            lstStudent = reciptObj.data.CardNumber
            idCourse = reciptObj.data.IDKhoaThi
            if(len(lstStudent) == 0):
                return
            self.__AddStudent(lstStudent, idCourse)
        
        elif(reciptObj.data.action == "sync"):
            self.__UpdateSyncData(reciptObj.data.fileName)

        elif(reciptObj.data.action == "newCourse"):
            self.__CreateAndAddNewCourse(reciptObj)

        elif(reciptObj.data.action == "getBy"):
            pass
        elif(reciptObj.data.action == "getAll"):
            pass
        elif(reciptObj.data.action == "deleteBy"):
            if(len(lstStudent) == 0):
                return
            self.__DeleteStudentByNumber(lstStudent)
        elif(reciptObj.data.action == "deleteAll"):
            self.__DeleteAllStudent()

    def __UpdateSyncData(self, fileName):
        lstFileName = []
        lstFileName.append(fileName)
        ftpObj = FTPclient()
        ftpObj.GetListFileFromServer(lstFile = lstFileName, ftpFilePath = FTP_SERVER_SYNC_DIR)
        updateFilePath = LOCAL_PATH_CONTAIN_DATA_UPDATE + fileName
        with open(updateFilePath, encoding='utf-8-sig') as json_file:
            jsonDict = json.load(json_file)

        khoThiSinh = ThiSinhRepository()
        khoThiSinh.capNhatTruong(("NhanDienKhuonMatThem", "NhanDienVanTay"),(jsonDict["FaceEncoding"], jsonDict["FGPEncoding"]), " ID = '%s' "%(jsonDict["ID"]))
        faceEncodingStringArr = jsonDict["FaceEncoding"].split(",")
        faceEncodingArr = [float(elem) for elem in faceEncodingStringArr]
        lstMultiFGPfeatureStr = jsonDict["FGPEncoding"].split(";")
        lstFGP = []
        for FGPfeatureStr in lstMultiFGPfeatureStr:
            FGPfeatureStrArr = FGPfeatureStr.split(",")
            FGPfeatureArr = [int(elem) for elem in FGPfeatureStrArr]
            lstFGP.append(FGPfeatureArr)
        # FGPencodingStringArr = jsonDict["FGPEncoding"].split(",")
        # FGPencodingArr = [int(elem) for elem in FGPencodingStringArr]

        faceInfoDict = {
            "faceEncodingArr": faceEncodingArr,
            "FGPencoding":lstFGP,
            "idStudent" : jsonDict["ID"],
        }
        self.SignalUpdateOrSyncStudentInfo.emit(faceInfoDict)

    def __CreateAndAddNewCourse(self, dataObj):
        khoaThi = ThongTinKhoaThi()
        khoaThi.IDKhoaThi = dataObj.data.CourseInfo.IDKhoaThi
        khoaThi.TenKhoaThi = dataObj.data.CourseInfo.TenKhoaThi
        khoaThi.DuongDanLuuAnh = ""
        khoaThi.NgayTao = dataObj.data.CourseInfo.NgayTao
        khoKhoaThi = KhoaThiRepository()
        khoKhoaThi.ghiDuLieu(khoaThi)
        self.__AddStudent(dataObj.data.CardNumber, khoaThi.IDKhoaThi)

    def __ConvertStringToUTF8String(self, string):
        x = []
        for elem in string:
            x.append(ord(elem))
        return(bytes(x).decode("utf8", "ignore"))

    def __AddStudent(self, lstStudentNumber, IDCourse):
        
        lstImage = []
        try:
            for stNumber in lstStudentNumber:
                imageName = str(stNumber.CardNumber) + ".jpg"
                lstImage.append(imageName)

        except NameError as e:
            print(e)
            pass
        ftpObj = FTPclient()
        lstImageGrapped = ftpObj.GetListFileFromServer(lstImage)
        khoThiSinh = ThiSinhRepository()
        i = 0
        for image in lstImage:
            try:
                student = ThongTinThiSinh()
                fp = open(LOCAL_PATH_CONTAIN_DATA_UPDATE + image, 'rb')
                student.ID = image.split(".")[0]
                student.AnhDangKy = fp.read()
                imagePil = Image.open(io.BytesIO(student.AnhDangKy))
                imagePil = imagePil.convert("RGB")
                npArrayImage = numpy.array(imagePil)
                student.NhanDienKhuonMatStr = GetFaceEncodingFromImage().GetFaceEncodingStr(npArrayImage)[0]
                student.HoVaTen = self.__ConvertStringToUTF8String(lstStudentNumber[i].TraineeName)
                student.IDKhoaThi = IDCourse
                khoThiSinh.ghiDuLieu(student)
                del student
            except NameError as e:
                print(e)
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
        chieuDaiDl = frameNhan[4] + frameNhan[5] * math.pow(2, 8)
        duLieu = []
        j = 0
        for i in range(6, int(chieuDaiDl)+6):
            duLieu.append("")
            duLieu[j] = chr(frameNhan[i])
            j += 1
            chuoiDuLieu = ''.join(duLieu)
        return chuoiDuLieu
