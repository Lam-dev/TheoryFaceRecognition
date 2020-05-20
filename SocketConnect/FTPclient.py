
import ftplib
from    PyQt5.QtCore            import pyqtSlot, pyqtSignal,QTimer, QDateTime,Qt, QObject
import  os
import shutil
from   GetSettingFromJSON       import GetSetting
# ftp = ftplib.FTP("192.168.1.46")
# ftp.login("etm", "1")
# file = []


# def getFile(ftp, filename):
#     try:
#         x = ftp.retrbinary("RETR " + filename ,open(""+filename, 'wb').write)
#         print(x)
#     except:
#         print ("Error")

# data = []
# ftp.cwd('/files/raspi_3g/')         # change directory to /pub/
# # getFile(ftp, "TTDD_29A-999999_2019-11-05_16-47-05.json")
# files = ftp.nlst()
# for f in files:
#     print(f)

# files = ftp.nlst()
# for f in files:
#     print(f)

SETTING_DICT = GetSetting.LoadSettingFromFile()
try:
    FTP_IP       =  SETTING_DICT["ftpIP"]
    FTP_PORT     =  SETTING_DICT["ftpPort"]
    FTP_ACCOUNT  =  SETTING_DICT["ftpAccount"]
    FTP_PASSWORD =  SETTING_DICT["ftpPassword"]
except:
    FTP_IP = "192.168.0.0"
    FTP_PORT = 0
    FTP_ACCOUNT = ""
    FTP_PASSWORD = ""

LOCAL_PATH_CONTAIN_DATA_UPDATE = "DataUpdate/"
FTP_SERVER_DOWLOAD_IMAGE_FILE_PATH = "syncimage/"
FTP_FILE_PATH_TO_UPLOAD            = GetSetting.GetSetting("--ServerImageDir")

class FTPclient(QObject):
    SignalFTPnotConnect = pyqtSignal()
    SignalFolderNotExist = pyqtSignal()
    SignalWaitForDeleteFile = pyqtSignal()
    SignalError = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.__CreateConnect()
        self.localImageFile = ""
        # self.timerDeleteLocalFile = QTimer(self)
        # self.timerDeleteLocalFile.timeout.connect(self.__DeleteLocalImageFile)
    def __CreateConnect(self):
        try:
            self.ftpObj = ftplib.FTP(host = FTP_IP, timeout = 4)
            self.ftpObj.login(FTP_ACCOUNT, FTP_PASSWORD)
            return True

        except Exception as ex:
            return str(ex.args)

    def DeleteLocalImageFile(self):
        try:
            print("da xoa = %s"%(self.localImageFile))
            os.remove(self.localImageFile)
        except:
            pass

    def ConnectNewFTPserver(self, inforDict):
        global FTP_IP, FTP_PORT, FTP_ACCOUNT, FTP_PASSWORD
        FTP_IP = inforDict["ftpIP"]
        FTP_PORT = int(inforDict["ftpPort"])
        FTP_ACCOUNT = inforDict["ftpAccount"]
        FTP_PASSWORD  = inforDict["ftpPassword"]
        return self.__CreateConnect()


    def GetListStudentImage(self, fileDir):
        self.SignalError.emit("war >>  " + fileDir)
        for i in range(0, 3):
            try:
                self.ftpObj.cwd(fileDir)
                lstFile = self.ftpObj.nlst()
                lstImage = []
                for f in lstFile:
                    
                    if(f.__contains__("jpg")):
                        lstImage.append(f)
                self.GetListFileFromServer(lstImage)
                return lstImage
            except Exception as ex:
                self.SignalError.emit("er >>getIm>> "+ str(ex.args))
                self.__CreateConnect()
    

    
    def SendImageToFTPserver(self, localfile, remotefile):
        self.localImageFile = localfile
        fp = open(localfile, 'rb')
        try:
            self.__CreateConnect()
            self.ftpObj.storbinary('STOR %s' % remotefile, fp, 1024)
            self.SignalWaitForDeleteFile.emit()
        except Exception as ex:
            self.SignalError.emit("er >>sendIm_ftp> "+ str(ex.args))
            try:
                print("remotefile not exist error caught" + remotefile)
                path,filename = os.path.split(remotefile)
                print("creating directory: " + remotefile)
                self.ftpObj.mkd(path)
                self.ftpObj.storbinary('STOR %s' % remotefile, fp, 1024)
                self.SignalWaitForDeleteFile.emit()
                fp.close()
                return
            except:
                pass

        self.SignalWaitForDeleteFile.emit()
        fp.close()
                    
    def GetListFileFromServer(self, lstFile, ftpFilePath = FTP_SERVER_DOWLOAD_IMAGE_FILE_PATH):
        
        numberFileGraped = 0
        lstImageGraped = []
        # os.removedirs(LOCAL_PATH_CONTAIN_DATA_UPDATE)
        # os.makedirs(LOCAL_PATH_CONTAIN_DATA_UPDATE)
        try:
            shutil.rmtree(LOCAL_PATH_CONTAIN_DATA_UPDATE)
        except Exception as ex:
            pass
        os.mkdir("DataUpdate")
        try:
            self.ftpObj.cwd(ftpFilePath)
        except:
            try:
                self.__CreateConnect()
                self.ftpObj.cwd(ftpFilePath)
            except Exception as ex:
                raise ConnectionError("er>>>ftpNotConnect>>  "+str(ex.args))
        try:
            
            for f in lstFile:
                self.SignalError.emit("war >> ftp" + f)
                if((not f.__contains__(".jpg")) & (not f.__contains__(".json"))):
                    continue
                try:
                    self.ftpObj.retrbinary("RETR " + f ,open(LOCAL_PATH_CONTAIN_DATA_UPDATE + f, 'wb').write)
                    numberFileGraped += 1
                    lstImageGraped.append(f)
                    self.SignalError.emit(">>> da lay anh >> " + f)
                except Exception as ex:
                    raise Exception("er >>ftp_getf> "+ str(ex.args))

            return lstImageGraped
        except Exception as ex:
            raise Exception("er >>ftp_getf> "+ str(ex.args))



# x = FTPclient()
# x.GetListStudentImage("/files/")
# x.SendImageToFTPserver("/home/lam/AppLoadXml/aaa.jpg", "files/aaa.jpg")

# x = FTPclient()
# x.GetListFileFromServer(['1.jpg', '2.jpg'])
