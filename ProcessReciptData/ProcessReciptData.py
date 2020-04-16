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
import getmac

CODE_RECIPT_DATA_FROM_SERVER = 3
CODE_UPLOAD_DATA_TO_SERVER = "2"
CODE_PING_PING = 1

SERVER_REQUEST_GET_LIST_COURSE                      = 7
SERVER_REQUEST_GET_LIST_STUDENT                     = 8
SERVER_REQUEST_DELETE_A_COURSE                      = 9
SERVER_REQUEST_DELETE_A_STUDENT                     = 10
SERVER_REQUEST_GET_LIST_HISTORY                     = 11

LOCAL_PATH_CONTAIN_DATA_UPDATE                      = "DataUpdate/"
FTP_FILE_PATH_TO_UPLOAD                             = GetSetting.GetSetting("--ServerImageDir")
FTP_SERVER_SYNC_DIR                                = "files/"

MAC                              =  getmac.get_mac_address()

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
    SignalSendResultDeleteAndCheck = pyqtSignal(str, int)
    SignalStopForUpdateData = pyqtSignal()
    SignalWaitForRecitpEnoughSyncData = pyqtSignal()
    SignalSyncComplete = pyqtSignal()
    SignalDeleteFGPofStudent = pyqtSignal(str)
    __FlagTimeUpdated = False
    SignalErrorOrSuccess = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.lstFeatureFileNameForSync = []

        # self.ftpObj = FTPclient()

    def _json_object_hook(self, d): return namedtuple('X', d.keys())(*d.values())

    def json2obj(self, data): return json.loads(data, object_hook=self._json_object_hook, encoding= "utf-8")
    
    def ProcessDataFrame(self, khungNhan):
        try:
            data, code = self.__CatLayPhanDataTrongFrame(khungNhan)
            reciptObj = self.json2obj(data)

            if(code == CODE_RECIPT_DATA_FROM_SERVER):
                self.SignalStopForUpdateData.emit()
                self.__ProcessRequestUpdateDatabase(reciptObj)
            
            elif(code == CODE_UPLOAD_DATA_TO_SERVER):
                self.ServerRequestTakePicture.emit()
                
            elif(code == CODE_PING_PING):
                self.__ServerAcceptConnect(reciptObj)
                
            elif(code == SERVER_REQUEST_GET_LIST_COURSE):
                self.SendListCourse()
            
            elif(code == SERVER_REQUEST_GET_LIST_STUDENT):
                self.SendListStudent(reciptObj)

            elif(code == SERVER_REQUEST_DELETE_A_COURSE):
                self.SignalStopForUpdateData.emit()
                self.DeleteCourse(reciptObj)

            elif(code == SERVER_REQUEST_DELETE_A_STUDENT):
                self.SignalStopForUpdateData.emit()
                self.DeleteStudent(reciptObj)
            
            elif(code == SERVER_REQUEST_GET_LIST_HISTORY):
                self.GetListHistory(reciptObj)    
        except:

            pass
    
    def SendListCourse(self):
        courseRepo = KhoaThiRepository()
        lstCourse = courseRepo.layDanhSach(" 1 = 1 ")
        lstCourseInfo = []
        for course in lstCourse:
            courseInfor = {
                "courseID": course.IDKhoaThi,
                "numStudent": 0,
            }
            lstCourseInfo.append(courseInfor)
        messageSendToSocket = {
            "MAC": MAC,
            "listCouse": lstCourseInfo
        }
        self.SignalSendResultDeleteAndCheck.emit(json.dumps(messageSendToSocket), SERVER_REQUEST_GET_LIST_COURSE)
        
    def SendListStudent(self, objectInfo):
        studentRepo = ThiSinhRepository()
        lstStudent = studentRepo.layDanhSach( " IDKhoaThi = %s "%(objectInfo.courseID))
        lst10student = []
        numFrame = int(len(lstStudent) / 10) + 1
        frameNum = 1
        while(True):
            if(len(lst10student) > 10):
                lst10student = lstStudent[0:9]
                self.Send10Student(lst10student, objectInfo.courseID, "%s/%s"%(frameNum, numFrame))
                lstStudent = lstStudent[10:(len(lstStudent) - 1)]
                frameNum += 1
            else:
                self.Send10Student(lstStudent, objectInfo.courseID, "%s/%s"%(frameNum, numFrame))
                return


    def Send10Student(self,lstStudent, courseID, frameNum):
        lstStudentID = []
        for student in lstStudent:
            lstStudentID.append(student.ID)
        messageSendToSocket = {
            "MAC":MAC,
            "courseID":courseID,
            "listStudent": lstStudentID,
            "frameNum":frameNum
        }
        self.SignalSendResultDeleteAndCheck.emit(json.dumps(messageSendToSocket), SERVER_REQUEST_GET_LIST_STUDENT)

    def DeleteCourse(self, objectInfo):
        try:
            # studentRepo = ThiSinhRepository()
            # studentRepo.xoaBanGhi(" IDKhoaThi = %s "%(objectInfo.courseID))
            # courseRepo = KhoaThiRepository()
            # courseRepo.xoaBanGhi( " IDKhoaThi = %s "%(objectInfo.courseID))
            lstStudentOfCourse = ThiSinhRepository().layDanhSach(" IDKhoaThi = %s"%(objectInfo.courseID))
            for student in lstStudentOfCourse:
                self.DeleteStudentByID(student.ID)
            courseRepo = KhoaThiRepository()
            courseRepo.xoaBanGhi( " IDKhoaThi = %s "%(objectInfo.courseID))
            messageSendToSocket = {
                "MAC":MAC,
                "curseID":objectInfo.courseID,
            }
            self.SignalSendResultDeleteAndCheck.emit(json.dumps(messageSendToSocket), SERVER_REQUEST_DELETE_A_COURSE)
            
        except Exception as ex:
            self.SignalErrorOrSuccess.emit("er >>delCourseER >>"+ str(ex.args))

    
    def DeleteStudent(self, objectInfo):

        self.DeleteStudentByID(objectInfo.studentID)

    def DeleteStudentByID(self, ID):

        try:
            studentRepo = ThiSinhRepository()
            studentRepo.xoaBanGhi(" ID = '%s' "%(ID))
            messageSendToSocket = {
                "MAC":MAC,
                "studentID":ID,
            }
            idAndFGPrepo = IDvaVanTayRepository()
            idAndFGPrepo.xoaBanGhi(" ID = '%s' "%(ID))
            self.SignalDeleteFGPofStudent.emit(ID)
            self.SignalSendResultDeleteAndCheck.emit(json.dumps(messageSendToSocket), SERVER_REQUEST_DELETE_A_STUDENT)
        except:
            pass

    def GetListHistory(self, objectInfo):
        historyRepo = LichSuRepository()
        lstHistory = historyRepo.layDanhSach(" 1 = 1 ")
        lstHistoryInfo = []
        for history in lstHistory:
            dictInfo = {
                "studentID":history.IDThiSinh,
                "checkTime":history.ThoiGian
            }
            lstHistoryInfo.append(dictInfo)
        jsonToFile = {
            "MAC":MAC,
            "courseID":objectInfo.courseID,
            "his":lstHistoryInfo
        }
        fileName  = "HIS_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".json"
        with open(fileName, 'w') as outfile:
            json.dump(jsonToFile, outfile)

        messageSendToSocket = {
            "MAC":MAC,
            "fileName":fileName
        }
        self.SignalSendFile.emit(fileName)
        self.SignalSendResultDeleteAndCheck.emit(json.dumps(messageSendToSocket), SERVER_REQUEST_GET_LIST_HISTORY)

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

        except:
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
                self.SignalSendMessage.emit(messageForSendToServer, SERVER_REQUEST_GET_LIST_HISTORY)
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
            # self.SignalWaitForRecitpEnoughSyncData.emit()
            # self.lstFeatureFileNameForSync.insert(0, reciptObj.data.fileName)
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

    # def QueueUpdateData(self, fileName):
    #     if(not self.timerUpdateSyncData.isActive):
    #         self.timerUpdateSyncData.start(1500)
    #     self.lstFeatureFileNameForSync.

    def TimerUpdateDataTimeout(self):
        self.SignalStopForUpdateData.emit()
        if(self.lstFeatureFileNameForSync.__len__() == 0):
            self.SignalSyncComplete.emit()
        else:
            featureFileName = self.lstFeatureFileNameForSync.pop()
            self.__UpdateSyncData(featureFileName)

    def __UpdateSyncData(self, fileName):
        try:
            lstFileName = []
            lstFileName.append(fileName)
            ftpObj = FTPclient()
            result = ftpObj.GetListFileFromServer(lstFile = lstFileName, ftpFilePath = FTP_SERVER_SYNC_DIR)
            if(type(result) is bool):
                raise Exception("")
            updateFilePath = LOCAL_PATH_CONTAIN_DATA_UPDATE + fileName
            with open(updateFilePath, encoding='utf-8-sig') as json_file:
                jsonDict = json.load(json_file)
            khoThiSinh = ThiSinhRepository()
            khoThiSinh.capNhatTruong(("NhanDienKhuonMatThem", "NhanDienVanTay"),(jsonDict["FaceEncoding"], jsonDict["FGPEncoding"]), " ID = '%s' "%(jsonDict["ID"]))
            try:
                faceEncodingStringArr = jsonDict["FaceEncoding"].split(",")
                faceEncodingArr = [float(elem) for elem in faceEncodingStringArr]
            except:
                faceEncodingArr = []
            try:
                lstMultiFGPfeatureStr = jsonDict["FGPEncoding"].split(";")
                lstFGP = []
                for FGPfeatureStr in lstMultiFGPfeatureStr:
                    FGPfeatureStrArr = FGPfeatureStr.split(",")
                    FGPfeatureArr = [int(elem) for elem in FGPfeatureStrArr]
                    lstFGP.append(FGPfeatureArr)
            # FGPencodingStringArr = jsonDict["FGPEncoding"].split(",")
            # FGPencodingArr = [int(elem) for elem in FGPencodingStringArr]
            except:
                lstFGP = []
            faceInfoDict = {
                "faceEncodingArr": faceEncodingArr,
                "FGPencoding":lstFGP,
                "idStudent" : jsonDict["ID"],
            }
            self.SignalUpdateOrSyncStudentInfo.emit(faceInfoDict)
        except Exception as e:
            self.SignalSendMessage.emit("er >> addRecEr>> IDst = ")

    def __CreateAndAddNewCourse(self, dataObj):
        try:
            khoaThi = ThongTinKhoaThi()
            khoaThi.IDKhoaThi = dataObj.data.CourseInfo.IDKhoaThi
            khoaThi.TenKhoaThi = dataObj.data.CourseInfo.TenKhoaThi
            khoaThi.DuongDanLuuAnh = ""
            khoaThi.NgayTao = dataObj.data.CourseInfo.NgayTao
            khoKhoaThi = KhoaThiRepository()
            khoKhoaThi.ghiDuLieu(khoaThi)
            self.SignalErrorOrSuccess.emit("suc >> addedCourse >> "+"ID = "+str(khoaThi.IDKhoaThi)+"T"+str(khoaThi.TenKhoaThi))
        except Exception as ex:
            self.SignalErrorOrSuccess.emit("er >> errAddCourse >> "+str(ex.args))
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

        except:
            pass
        ftpObj = FTPclient()
        lstImageGrapped = ftpObj.GetListFileFromServer(lstImage)
        khoThiSinh = ThiSinhRepository()
        i = 0
        for image in lstImage:
            try:
                student = ThongTinThiSinh()
                try:
                    fp = open(LOCAL_PATH_CONTAIN_DATA_UPDATE + image, 'rb')
                    student.ID = image.split(".")[0]
                    student.AnhDangKy = fp.read()
                except:
                    self.SignalErrorOrSuccess.emit("er > stAddEr>> not image")
                #imagePil = Image.open(io.BytesIO(student.AnhDangKy))
                #imagePil = imagePil.convert("RGB")
                #npArrayImage = numpy.array(imagePil)
                student.NhanDienKhuonMatStr = ""#GetFaceEncodingFromImage().GetFaceEncodingStr(npArrayImage)[0]
                student.HoVaTen = self.__ConvertStringToUTF8String(lstStudentNumber[i].TraineeName)
                student.SoCMTND = lstStudentNumber[i].SoCMT
                student.IDKhoaThi = IDCourse
                khoThiSinh.ghiDuLieu(student)
                del student
                self.SignalErrorOrSuccess.emit("suc > stAdded>> "+ lstStudentNumber[i].TraineeName)
            except:
                self.SignalErrorOrSuccess.emit("er > stAddEr>> "+ lstStudentNumber[i].TraineeName)
    
    def __DeleteStudentByNumber(self, lstStudentNumber):
        khoThiSinh = ThiSinhRepository()
        for stNumber in lstStudentNumber:
            try:
                khoThiSinh.xoaBanGhi(" ID = %s "%(stNumber))
                self.SignalErrorOrSuccess.emit("suc > deleted>> "+ stNumber)
            except:
                self.SignalErrorOrSuccess.emit("err > deleteEr>> "+ stNumber)
    
    def __DeleteAllStudent(self):
        khoThiSinh = ThiSinhRepository()
        khoThiSinh.xoaBanGhi(" 1 = 1 ")

    def __CatLayPhanDataTrongFrame(self, frameNhan):
        code = frameNhan[3]
        chieuDaiDl = frameNhan[4] + frameNhan[5] * math.pow(2, 8)
        duLieu = []
        j = 0
        for i in range(6, int(chieuDaiDl)+6):
            duLieu.append("")
            duLieu[j] = chr(frameNhan[i])
            j += 1
            chuoiDuLieu = ''.join(duLieu)
        return chuoiDuLieu, code