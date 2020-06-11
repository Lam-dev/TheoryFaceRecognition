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
from   GlobalClass.GlobalClass   import  RequestFromTakeSample

CODE_RECIPT_DATA_FROM_SERVER = 3
CODE_UPLOAD_DATA_TO_SERVER = "2"
CODE_PING_PING = 1

SERVER_REQUEST_GET_LIST_COURSE                      = 7
SERVER_REQUEST_GET_LIST_STUDENT                     = 8
SERVER_REQUEST_DELETE_A_COURSE                      = 9
SERVER_REQUEST_DELETE_A_STUDENT                     = 10
SERVER_REQUEST_GET_LIST_HISTORY                     = 11
SERVER_REQUEST_ADD_TEACHER                          = 20
SERVER_REQUEST_ADD_TEACHER_STUDENT                  = 21    

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
    SignalRequestUpdate = pyqtSignal()
    __FlagTimeUpdated = False
    SignalErrorOrSuccess = pyqtSignal(str)
    SignalRequestDelAllData = pyqtSignal()
    

    def __init__(self):
        super().__init__()
        self.lstFeatureFileNameForSync = []
        self.lstStudentAddErr = []
        self.ftpObj = FTPclient()

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

            elif(code == SERVER_REQUEST_ADD_TEACHER):
                self.__AddTeacher(reciptObj)

            elif(code == SERVER_REQUEST_ADD_TEACHER_STUDENT):
                self.__AddTeacherStudent(reciptObj)
        except:
            pass
    
    def __AddTeacher(self, teacherInfo):
        thisinhRepo = ThiSinhRepository()
        teacherStudentRepo = DanhSachThiSinhTuongUngTaiKhoanRepository()
        try:
            if(teacherInfo.code == RequestFromTakeSample.DelAllTeacher.value):
                thisinhRepo.xoaBanGhi("IDKhoaThi = 0")
                teacherStudentRepo.xoaBanGhi(" 1=1 ")
                return

            elif(teacherInfo.code == RequestFromTakeSample.Reset.value):
                os.system("reboot")
                return
            elif(teacherInfo.code == RequestFromTakeSample.Shutdown.value):
                os.system("shutdown now")
                return
            elif(teacherInfo.code == RequestFromTakeSample.Restore.value):
                self.SignalRequestDelAllData.emit()
                return
            elif(teacherInfo.code == RequestFromTakeSample.CheckVersion.value):
                try:
                    macString = self.SendVersionInfo()
                    version = self.GetCurrentVersion()
                    self.SignalErrorOrSuccess.emit("SERI+VERSION >> "+ macString +"___"+ version)
                except Exception as ex:
                    print("Lay Mac"+ str(ex.args))
                    pass
                return
            elif(teacherInfo.code == RequestFromTakeSample.UpdateFW.value):
                self.SignalRequestUpdate.emit()
                return

        except Exception as ex:
            print(ex.args)
            pass
        try:
            self.SignalStopForUpdateData.emit()
            teacher = ThongTinThiSinh()
            
            teacher.ID = "ELT_" + str(teacherInfo.ID)
            teacher.HoVaTen = teacherInfo.TaiKhoan
            teacher.IDKhoaThi = 0
            teacher.AnhDangKy = b''
            teacher.NhanDienVanTay = teacherInfo.DacTrungVanTay
            teacher.NhanDienKhuonMatThem = teacherInfo.DacTrungKhuonMat
            thisinhRepo.ghiDuLieu(teacher)
            thisinhRepo.capNhatTruong(("NhanDienKhuonMatThem", "NhanDienVanTay"),(teacherInfo.DacTrungKhuonMat, teacherInfo.DacTrungVanTay), " ID = '%s' "%(teacher.ID))
            faceInfoDict = {
                "FaceEncoding": teacherInfo.DacTrungKhuonMat,
                "FGPEncoding":teacherInfo.DacTrungVanTay,
                "ID" : teacher.ID,
            }
            self.__AddRecogntionAtRuntime(faceInfoDict)
        except Exception as ex:
            print(ex.args)

    def SendVersionInfo(self):
        try:
            macString = getmac.get_mac_address()
            if(len(macString) < 2):
                self.SignalErrorOrSuccess.emit("LOI >> CHUA CAM MANG DE LAY MAC")
            lstByteStrType = macString.split(":")
            lstByteMacIntType = [int(elem, 16) for elem in lstByteStrType]
            seriString = ""
            for i in range(3, 6):
                seriElem = lstByteMacIntType[i] ^ 69
                seriString += self.__ToHex8bit(seriElem)
            return seriString
        except Exception as ex:
            print("Loi lay mac"+str(ex.args))
            raise Exception("error")

    def __ToHex8bit(self, number):
        hexStr = hex(number)[2:]
        if(len(hexStr) == 1):
            return "0"+ hexStr
        else:
            return hexStr

    def GetCurrentVersion(self):
        try:
            with open('version.json') as json_file:
                return json.load(json_file)["crVer"]
        except:
            return ""


    def __AddTeacherStudent(self, teacherStudentInfo):
        self.SignalStopForUpdateData.emit()
        teacherStudentRepo = DanhSachThiSinhTuongUngTaiKhoanRepository()
        teacherStudent = HocVienTuongUngTaiKhoanQuanLy()
       
        teacherStudent.IDtaiKhoan = teacherStudentInfo.IDteacher
        teacherStudent.IDthiSinh = teacherStudentInfo.RegisNumber
        teacherStudentRepo.ghiDuLieu(teacherStudent)


    def SendListCourse(self):
        courseRepo = KhoaThiRepository()
        lstCourse = courseRepo.layDanhSach(" 1 = 1 ")
        lstCourseInfo = []
        for course in lstCourse:
            courseInfor = {
                "ID": course.IDKhoaThi,
                "N":course.TenKhoaThi,
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
            studentInfoDict = {
                'IDK':student.IDKhoaThi,
                'ID':student.ID,
                'N':student.HoVaTen,
                'VT': True if len(student.NhanDienVanTay)!=0 else False,
                'KM': True if len(student.NhanDienKhuonMatThem)!=0 else False
            }
            lstStudentID.append(studentInfoDict)
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
            "courseID":objectInfo.data.courseID,
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
            
            result = self.ftpObj.GetListFileFromServer(lstFile = lstFileName, ftpFilePath = FTP_SERVER_SYNC_DIR)
            if(type(result) is bool):
                raise Exception("")
            updateFilePath = LOCAL_PATH_CONTAIN_DATA_UPDATE + fileName
            with open(updateFilePath, encoding='utf-8-sig') as json_file:
                jsonDict = json.load(json_file)
                self.SignalErrorOrSuccess.emit("war >> read "+fileName)

            khoThiSinh = ThiSinhRepository()
            khoThiSinh.capNhatTruong(("NhanDienKhuonMatThem", "NhanDienVanTay"),(jsonDict["FaceEncoding"], jsonDict["FGPEncoding"]), " ID = '%s' "%(jsonDict["ID"]))
            self.__AddRecogntionAtRuntime(jsonDict)
        except Exception as ex:
            self.SignalErrorOrSuccess.emit("LOI >> PHAN TICH VT+KM"+str(ex.args))
    
    def __AddRecogntionAtRuntime(self, jsonDict):
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
        except Exception as ex:
            print(ex.args)
            lstFGP = []
        faceInfoDict = {
            "faceEncodingArr": faceEncodingArr,
            "FGPencoding":lstFGP,
            "idStudent" : jsonDict["ID"],
        }
        self.SignalUpdateOrSyncStudentInfo.emit(faceInfoDict)

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
        self.SignalStopForUpdateData.emit()
        lstImage = []

        for stNumber in lstStudentNumber:
            imageName = str(stNumber.CardNumber) + ".jpg"
            lstImage.append(imageName)

        try:
            lstImageGrapped = self.ftpObj.GetListFileFromServer(lstImage)
        except Exception as ex:
            
            self.SignalErrorOrSuccess.emit("er > ftpErr>> "+ str(ex.args))
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
                student.NhanDienKhuonMatStr = ""#GetFaceEncodingFromImage().GetFaceEncodingStr(npArrayImage)[0]
                student.HoVaTen = self.__ConvertStringToUTF8String(lstStudentNumber[i].TraineeName)
                student.SoCMTND = lstStudentNumber[i].SoCMT
                student.IDKhoaThi = IDCourse
                khoThiSinh.ghiDuLieu(student)
                del student
                self.SignalErrorOrSuccess.emit("TC > THEM HV: >> "+ lstStudentNumber[i].TraineeName)
            except Exception as ex:
                try:
                    if(str(ex.args).__contains__("UNIQUE")):
                        khoThiSinh.xoaBanGhi(" ID = '%s'"%(student.ID))
                        khoThiSinh.ghiDuLieu(student)
                        self.SignalErrorOrSuccess.emit("TC > CAP NHAT HV: >> "+ lstStudentNumber[i].TraineeName)
                    else:
                        self.SignalErrorOrSuccess.emit("LOI > CAP NHAT HV: >> "+ lstStudentNumber[i].TraineeName + ">>" + str(ex.args))
                except Exception as ex:
                        self.SignalErrorOrSuccess.emit("LOI > CAP NHAT HV: >> "+ lstStudentNumber[i].TraineeName + ">>" + str(ex.args))
    
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