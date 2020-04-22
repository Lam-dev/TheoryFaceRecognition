import socket
from    datetime                import datetime
from    PyQt5.QtCore            import pyqtSlot, pyqtSignal,QTimer, QDateTime,Qt, QObject
import  threading
from    ProcessReciptData.ProcessReciptData       import ProcessReciptData
import  math
import  time
from    SocketConnect.FTPclient import FTPclient
from    GetSettingFromJSON    import GetSetting
import json
import  os
import getmac
import      pytz

SETTING_DICT                                        = GetSetting.LoadSettingFromFile()
try:
    SERVER_IP                                           = SETTING_DICT["serverIP"]
    SERVER_PORT                                         = int(SETTING_DICT["serverPort"])
except:
    SERVER_IP = "0.0.0.0"
    SERVER_PORT = 0

CODE_SEND_PING_PONG                         = 1
CODE_RESULT_RECOGNITION                     = 2
CODE_STUDENT_FEATURE_FILE                   = 4
CODE_SEND_RESULT_DATA_BASE_CHECK            = 6
CODE_SEND_ERROR                             = 20

MAC_ADDRESS                                         = getmac.get_mac_address()
IMAGE_TO_SEND_SERVER_PATH                           = "/StudentRecognize/SocketConnect/"
FTP_FILE_PATH_TO_UPLOAD                             = GetSetting.GetSetting("--ServerImageDir")
FTP_SERVER_SYNC_FILE                                = "files/"

class SocketClient(QObject):
    
    ShowStudentForConfirm = pyqtSignal(str)
    __SignalRecreateConnect = pyqtSignal()
    SignalServerNotConnect = pyqtSignal()
    SignalServerConnected = pyqtSignal()
    SignalWaitForUpdateDatabase = pyqtSignal(str)
    SignalUpdateDatabaseSuccess = pyqtSignal(list)
    SignalNumberStudentParsed = pyqtSignal(int, int)
    SignalConnectNewServer = pyqtSignal(dict)
    SignalConnectNewFTP = pyqtSignal(dict)
    SignalUpdateOrSyncStudentInfo = pyqtSignal(dict)
    __SignalConnected = pyqtSignal()
    __SignalReciptEnounghData = pyqtSignal(bytes)
    SignalStopForUpdateData = pyqtSignal()
    SignalDeleteFGPofStudent = pyqtSignal(str)
    

    def __init__(self):
        super().__init__()
        self.ftpObj = FTPclient()
        self.timerPingPong = QTimer(self)
        self.timerPingPong.timeout.connect(self.__PingPong)

        self.timerDeleteFTPsendedFile = QTimer(self)
        self.timerDeleteFTPsendedFile.timeout.connect(self.DeleteFTPsendedFile)

        self.ftpObj.SignalWaitForDeleteFile.connect(lambda:self.timerDeleteFTPsendedFile.start(2100))
        self.ftpObj.SignalError.connect(self.SendLogError)

        self.timerWaitForReciptEnoughSyncData = QTimer(self)# cho nhan du du lieu dac trung,\
        self.timerSyncData = QTimer(self)
        self.timerWaitForReciptEnoughSyncData.timeout.connect(self.ReciptEnoughData)


        self.__SignalConnected.connect(self.__ServerConnected)


        self.processReciptDataObj = ProcessReciptData()
        self.processReciptDataObj.SignalErrorOrSuccess.connect(self.SendLogError)
        self.processReciptDataObj.ShowStudentForConfirm.connect(self.__ShowStudentForConfirmSlot)
        self.processReciptDataObj.ServerConfirmedConnect.connect(self.__ServerConfirmedConnect)
        self.processReciptDataObj.ResponseRequestUpdataFromServer.connect(self.__ResponseResquestUpdateDatabaseFromServer)
        self.processReciptDataObj.SignalUpdateDataBaseSuccess.connect(self.__UpdateDataBaseSuccess)
        self.processReciptDataObj.SignalNumberStudentParsed.connect(self.__NumberStudentParsed)
        self.processReciptDataObj.SignalUpdateOrSyncStudentInfo.connect(self.SignalUpdateOrSyncStudentInfo.emit)
        self.processReciptDataObj.SignalStopForUpdateData.connect(self.SignalStopForUpdateData.emit)
        self.processReciptDataObj.SignalWaitForRecitpEnoughSyncData.connect(self.WaitForReciptEnoughSyncData)
        self.processReciptDataObj.SignalSendFile.connect(self.SendFileDataBaseCheck)
        self.processReciptDataObj.SignalSendResultDeleteAndCheck.connect(self.SendMessageDatabaseCheck)
        self.processReciptDataObj.SignalSyncComplete.connect(self.StopSyncData)
        self.processReciptDataObj.SignalDeleteFGPofStudent.connect(self.SignalDeleteFGPofStudent.emit)
        self.chuaXuLy = b''

        self.timerSyncData.timeout.connect(self.processReciptDataObj.TimerUpdateDataTimeout)

        self.TimerWaitForServerConfirm = QTimer(self)
        self.TimerWaitForServerConfirm.timeout.connect(self.__ThreadCreateConnect)
        self.TimerWaitForServerConfirm.start(5000)

        self.FlagServerConfirmedForConnect = False
        self.FlagServerISconnect = False
        self.clientObj = ""
        
        self.ThreadWaitForReciptData()
        self.__TimerSendPingPong = QTimer(self)
        self.__TimerSendPingPong.timeout.connect(self.__SendPingPong)
        self.__SignalRecreateConnect.connect(self.__RecreateConnect)
        self.__FlagSendPingPong = True
        self.waitingForConnect = False
        self.__FlagBusyProcessingData = False
        self.__DataWaitForProcess = b''
        self.__FlagNeedProcessData = False
        self.__DataProcessing = b'';
        self.__SignalReciptEnounghData.connect(self.__ThreadTachVaPhanTichKhungNhan)
    

    def SendLogError(self, strErr):
        # for logLine in self.log.ReadLog():
        self.__SendDataViaSocket(self.__DungKhungGiaoTiep(strErr, CODE_SEND_ERROR))
        #pass


    def GetCurrentIP(self):
        gw = os.popen("ip -4 route show default").read().split()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setblocking(1)
        s.settimeout(1)
        s.connect((gw[2], 0))
        ipaddr = s.getsockname()[0]
        gateway = gw[2]
        host = socket.gethostname()

    def DeleteFTPsendedFile(self):
        self.timerDeleteFTPsendedFile.stop()
        self.ftpObj.DeleteLocalImageFile()

    def ReciptEnoughData(self):
        self.timerWaitForReciptEnoughSyncData.stop()
        self.timerSyncData.start(1100)

    def StopSyncData(self):
        self.timerSyncData.stop()

    def WaitForReciptEnoughSyncData(self):
        self.timerWaitForReciptEnoughSyncData.stop()
        self.timerWaitForReciptEnoughSyncData.start(5000)

    def SendFileDataBaseCheck(self, fileName):
        self.ftpObj.SendImageToFTPserver(fileName, FTP_SERVER_SYNC_FILE + "/" +fileName)
    
    def SendMessageDatabaseCheck(self, message, code):
        self.__SendDataViaSocket(self.__DungKhungGiaoTiep(message, code))


    def __ServerConnected(self):
        try:
            self.FlagServerISconnect = True
            self.TimerWaitForServerConfirm.stop()
            self.ThreadWaitForReciptData()
            self.timerPingPong.start(30000)
        except:
            pass

    def __ThreadCreateConnect(self):
        if(self.waitingForConnect):
            return
        thread = threading.Thread(target=self.CreateConnect, args=(), daemon = True)
        thread.start()

    def __RecreateConnect(self):
        self.FlagServerISconnect = False
        if(not self.TimerWaitForServerConfirm.isActive()):
            self.TimerWaitForServerConfirm.start(2000)

    def ConnectNewServer(self, serverInfoDict):
        try:
            global SERVER_IP, SERVER_PORT
            SERVER_IP = serverInfoDict["serverIP"]
            SERVER_PORT = int(serverInfoDict["serverPort"])
            self.FlagServerISconnect = False
            self.CreateConnect()
        except:
            pass

    def __SendPingPong(self):
        if(self.__FlagSendPingPong):
            self.__PingPong()
        else:
            self.__FlagSendPingPong = True

    def __NumberStudentParsed(self, number, all):
        self.SignalNumberStudentParsed.emit(number, all)

    def __UpdateDataBaseSuccess(self, lstStudent):
        self.SignalUpdateDatabaseSuccess.emit(lstStudent)

    def __ResponseResquestUpdateDatabaseFromServer(self, remoteFilePath):
        global FTP_FILE_PATH_TO_UPLOAD
        FTP_FILE_PATH_TO_UPLOAD = remoteFilePath + "AnhNhanDien/"
        
        self.__SendDataViaSocket(self.__DungKhungGiaoTiep(remoteFilePath + ";"+ MAC_ADDRESS, 4))
        self.SignalWaitForUpdateDatabase.emit(remoteFilePath)

    def __RecreateConnect(self):
        self.FlagServerISconnect = False
        if(not self.TimerWaitForServerConfirm.isActive()):
            self.TimerWaitForServerConfirm.start(5000)

    def __SendDataViaSocket(self, data):
        try:
            
            self.clientObj.send(data)
            self.__FlagSendPingPong = False
        except:
            self.FlagServerISconnect
            self.__SignalRecreateConnect.emit()

    def __ShowStudentForConfirmSlot(self, maDK):
        self.ShowStudentForConfirm.emit(maDK)


    def ThreadWaitForReciptData(self):
        threadReciptData = threading.Thread(target= self.__ListenResponseFromServer, args=(), daemon= True) 
        threadReciptData.start()

    def __ListenResponseFromServer(self):
        while True:
            try:
                recvData = self.clientObj.recv(1024)
                # if(recvData.__str__().__contains__("TTND")):
                #     print(datetime.now())
                print(recvData)
                len(recvData)
                if(recvData == b''):
                    self.__SignalRecreateConnect.emit()
                    return
                else:
                    # self.__FlagSendPingPong = False
                    self.__SignalReciptEnounghData.emit(recvData)

            except:
                self.__SignalRecreateConnect.emit()
                return


    def __ThreadTachVaPhanTichKhungNhan(self, revData):
        self.__DataWaitForProcess += revData
        if(self.__FlagBusyProcessingData):
            self.__FlagNeedProcessData = True
            return
        self.__FlagNeedProcessData = False
        self.__FlagBusyProcessingData = True
        self.__DataProcessing = self.__DataWaitForProcess
        self.__DataWaitForProcess = b''
        threadTachPhanTich = threading.Thread(target= self.__TachVaPhanTichKhungNhan, args=(self.__DataProcessing,), daemon= True) 
        threadTachPhanTich.start()
        

    def __TachVaPhanTichKhungNhan(self, data):
        lstCacKhungNhan = self.__TachCacKhungTruyen(data)
        for khung in lstCacKhungNhan:
            self.__PhanTichKhungNhan(khung)
        if(self.__DataWaitForProcess != b''):
            self.__SignalReciptEnounghData.emit(b'')
        self.__FlagBusyProcessingData = False
        
    def __PhanTichKhungNhan(self, khungNhan):
        try:
            # if(not self.__CheckSumKhungTruyen(khungNhan)):
            #     return
            self.processReciptDataObj.ProcessDataFrame(khungNhan)
                    
        except:
            print("khung trong")

    def __CheckSumKhungTruyen(self, frameNhan):
        # return True ## test
        try:
            tong = 0
            for i in range (3, len(frameNhan) - 1):
                tong = tong + frameNhan[i]
            tong = -(~tong) % 256
            # print("sum = ", tong) #test
            if(tong == frameNhan[len(frameNhan)-1]):
                # print("checksum dung")
                return True
            else:
                # print("checksum sai")
                return False
        except:
            return False

    def __TachCacKhungTruyen(self, duLieu):
        if(duLieu == b''):
            return []
        self.chuaXuLy = self.chuaXuLy + duLieu
        lstKhungDL = []
        i = 0
        while True:
            if(i == len(self.chuaXuLy)):
                break
            if( self.chuaXuLy[i:i+3].__str__().__contains__("ELT")):
                try:
                    chieuDaiDl = self.chuaXuLy[i+4] + self.chuaXuLy[i+5] * math.pow(2, 8)
                    chieuDaiKhung = i + int(chieuDaiDl) + 7
                    if(chieuDaiKhung + i <= len(self.chuaXuLy)):
                        lstKhungDL.append(self.chuaXuLy[i:chieuDaiKhung])
                        self.chuaXuLy = self.chuaXuLy[chieuDaiKhung: len(self.chuaXuLy)]
                        i = -1
                    else:
                        self.chuaXuLy = self.chuaXuLy[i: len(self.chuaXuLy)]
                        break
                except:
                    self.chuaXuLy = self.chuaXuLy[i: len(self.chuaXuLy)]
                    break
            i = i + 1
        return lstKhungDL

    def CreateConnect(self):
        global SERVER_IP, SERVER_PORT
        self.waitingForConnect = True
        try:
            if(not self.FlagServerISconnect):
                self.clientObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # self.clientObj.setblocking(0)
                # self.clientObj.settimeout(2)
                self.clientObj.connect((SERVER_IP, SERVER_PORT))
                self.__SendPingPong()
                self.SignalServerConnected.emit()
                self.__SignalConnected.emit()

        except:
            self.SignalServerNotConnect.emit()
            print("khong the ket noi") #test
            self.FlagServerISconnect = False
        self.waitingForConnect = False

    def __ServerConfirmedConnect(self):
        self.FlagServerConfirmedForConnect = True
        self.TimerWaitForServerConfirm.stop()


    def __PingPong(self):
        framePing = self.__DungKhungGiaoTiep(self.__BuildFramePingPong(), CODE_SEND_PING_PONG)
        try:
            self.clientObj.sendall(framePing)
        except:
            pass
    def __BuildFramePingPong(self):
        dictData = {
            "ping":"1"
        }
        dictToSend = {
            "mac":MAC_ADDRESS,
            "success":"true",
            "code":1,
            "message":"",
            "checksum":len(json.dumps(dictData)),
            "data":dictData
        }
        return json.dumps(dictToSend)
        
    def __BuildResultToSend(self, studentNumberCard, imageFileName, RecBy):
        tz_HCM = pytz.timezone('Asia/Ho_Chi_Minh') 
        datetime_HCM = datetime.now(tz_HCM)
        time_string = datetime_HCM.strftime("%d/%m/%Y %H:%M:%S")
        dictData = {
            "cardNumber":studentNumberCard,
            "time":time_string,
            "imageLength":0,
            "imageDir": imageFileName,
            "recBy": RecBy
        }
        dictToSend = {
            "mac":MAC_ADDRESS,
            "success":"true",
            "code":2,
            "massage":"",
            "checksum":len(json.dumps(dictData)),
            "data":dictData
        }
        return json.dumps(dictToSend)
        
    
    def __ConvertJsonStringToByteArr(self, jsonString):
        jsonCharArr = []
        jsonString = jsonString + "\n"
        for i in range(0, len(jsonString)):
            jsonCharArr.append(ord(jsonString[i]))
        return bytes(jsonCharArr)

    """
    khung truyen uart yeu cau module 3g gui file
    tham so
        tenFile: ten cua file can gui
    tra ve
        khungTruyen: khong truyen de gui cho ETM module
        tong : checksum cua khung truyen 
    """

    def __DungKhungGiaoTiep(self, noiDung, maLenh):
        if(type(noiDung) is not str): 
            return False, False
        highChieuDaiTen = int(len(noiDung) / 256)
        lowChieuDaiTen = int(len(noiDung) % 256)
        khungTruyen = [0x45, 0x4C, 0x54, maLenh, lowChieuDaiTen, highChieuDaiTen]
        tong = maLenh + highChieuDaiTen + lowChieuDaiTen
        j = 0
        for i in range (len(khungTruyen), len(khungTruyen) + len(noiDung)):
            khungTruyen.append('')
            khungTruyen[i] = ord(noiDung[j])
            tong = tong + ord(noiDung[j])
            j = j+ 1
            
        tong = -(~tong) % 256
        khungTruyen.append(0x00)
        khungTruyen[len(khungTruyen)-1] = tong
        return bytes(khungTruyen)

   
#region nhom ham gui thong tin cho server

    def SendResultsFaceRecognize(self, ID ,confirmTrueOrFalse, nameOfPhotoTaked):
        imageFileName = FTP_FILE_PATH_TO_UPLOAD +"/"+ datetime.now().strftime("%Y%m%d") + '/' + str(ID)+"_"+datetime.now().strftime("%H%M%S")+ ".jpg"
        resultFrame = self.__DungKhungGiaoTiep(self.__BuildResultToSend(ID, imageFileName, "Face"), CODE_RESULT_RECOGNITION)
        self.__SendDataViaSocket(bytes(resultFrame))
        thread = threading.Thread(target = self.ftpObj.SendImageToFTPserver, args = (nameOfPhotoTaked, imageFileName), daemon= True)
        thread.start()
        self.ftpObj.SendImageToFTPserver(nameOfPhotoTaked, FTP_FILE_PATH_TO_UPLOAD +"/"+ datetime.now().strftime("%Y%m%d") + '/' + str(ID)+"_"+datetime.now().strftime("%H%M%S")+ ".jpg")


    def SendResultsFGPrecognition(self, ID):
        resultFrame = self.__DungKhungGiaoTiep(self.__BuildResultToSend(ID, "", "FGP"), CODE_RESULT_RECOGNITION)
        self.__SendDataViaSocket(bytes(resultFrame))

    def SendResultsCardrecognition(self, ID):
        resultFrame = self.__DungKhungGiaoTiep(self.__BuildResultToSend(ID, "", "card"), CODE_RESULT_RECOGNITION)
        self.__SendDataViaSocket(bytes(resultFrame))

#endregion
    
    def SendAddFaceAndFGP(self, info):
        fileName = "TTND_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".json"
        with open(fileName, 'w') as outfile:
            json.dump(info, outfile)

        self.ftpObj.SendImageToFTPserver(fileName, FTP_FILE_PATH_TO_UPLOAD +"/"+fileName)
        os.remove(fileName)
        dictToServer = {
            "mac":MAC_ADDRESS,
            "code":4,
            "fileName": fileName
        }
        jsonStr = json.dumps(dictToServer)
        resultFrame = self.__DungKhungGiaoTiep(jsonStr, CODE_STUDENT_FEATURE_FILE)
        self.__SendDataViaSocket(bytes(resultFrame))

class HangDoi(QObject):
    DangCho = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.queue = list()
    def enqueue(self,data):
        if data not in self.queue:
            self.queue.insert(0,data)
            self.DangCho.emit()
            # print("hang doi  = ", self.printQueue())
            return True
        return False
        
    def remove(self, data):
        self.queue.remove(data)

    def enqueuePrioty(self, data):
        if data not in self.queue:
            self.queue.append(data)
            self.DangCho.emit()
            # print("hang doi  = ", self.printQueue())
            return True
        return False
    
    def dequeue(self):
        if len(self.queue)>0:
            return self.queue.pop()
        return ("Queue Empty!")
    
    def size(self):
        return len(self.queue)
    
    def printQueue(self):
        return self.queue
    
    def ConnectAllFrame(self):
        connectedFrame = ""
        for frame in self.queue:
            connectedFrame += frame
        return connectedFrame
    
    def ConnectAllFrameAndClear(self):
        connectedFrame = ""
        for frame in self.queue:
            connectedFrame += frame
        return 
        self.queue.clear()

