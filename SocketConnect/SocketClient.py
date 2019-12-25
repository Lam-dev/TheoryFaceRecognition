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


# SERVER_IP                                           = "192.168.1.254"
# SERVER_PORT                                         = 6363
SERVER_IP                                           = GetSetting.GetSetting("--SocketServerIP")
SERVER_PORT                                         = GetSetting.GetSetting("--SocketServerPort")

CODE_RECIPT_DATA_FROM_SERVER = "3"
CODE_UPLOAD_DATA_TO_SERVER = "2"
CODE_PING_PING = "1"

MAC_ADDRESS                                         = "123456"#[0xC8, 0X93, 0X46, 0X4E,0X5D,0XD9]C8-93-46-4E-5D-D9
IMAGE_TO_SEND_SERVER_PATH                           = "/StudentRecognize/SocketConnect/"
FTP_FILE_PATH_TO_UPLOAD                             = GetSetting.GetSetting("--ServerImageDir")

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

    def __init__(self):
        super().__init__()
        self.ftpObj = FTPclient()
        self.timerPingPong = QTimer(self)
        self.timerPingPong.timeout.connect(self.__PingPong)

        self.processReciptDataObj = ProcessReciptData()
        self.processReciptDataObj.ShowStudentForConfirm.connect(self.__ShowStudentForConfirmSlot)
        self.processReciptDataObj.ServerConfirmedConnect.connect(self.__ServerConfirmedConnect)
        self.processReciptDataObj.ResponseRequestUpdataFromServer.connect(self.__ResponseResquestUpdateDatabaseFromServer)
        self.processReciptDataObj.SignalUpdateDataBaseSuccess.connect(self.__UpdateDataBaseSuccess)
        self.processReciptDataObj.SignalNumberStudentParsed.connect(self.__NumberStudentParsed)
        self.chuaXuLy = b''

        self.FlagServerConfirmedForConnect = False
        self.FlagServerISconnect = False
        self.clientObj = ""
        self.TimerWaitForServerConfirm = QTimer(self)
        self.TimerWaitForServerConfirm.timeout.connect(self.CreateConnect)
        self.TimerWaitForServerConfirm.start(1000)
        self.ThreadWaitForReciptData()
        self.__TimerSendPingPong = QTimer(self)
        self.__TimerSendPingPong.timeout.connect(self.__SendPingPong)
        self.__TimerSendPingPong.start(10000)
        self.__SignalRecreateConnect.connect(self.__RecreateConnect)
        self.__FlagSendPingPong = True

    def ConnectNewServer(self, serverInfoDict):
        global SERVER_IP, SERVER_PORT
        SERVER_IP = serverInfoDict["serverIP"]
        SERVER_PORT = int(serverInfoDict["serverPort"])
        self.FlagServerISconnect = False
        self.CreateConnect()

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
        
        self.__SendDataViaSocket(self.__DungKhungGiaoTiep(remoteFilePath + ";"+ MAC_ADDRESS, 4)[0])
        self.SignalWaitForUpdateDatabase.emit(remoteFilePath)

    def __RecreateConnect(self):
        if(not self.TimerWaitForServerConfirm.isActive()):
            self.TimerWaitForServerConfirm.start(1000)

    def __SendDataViaSocket(self, data):
        try:
            self.clientObj.send(data)
            self.__FlagSendPingPong = False
        except NameError as e:
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
                print(recvData)
                len(recvData)
                if(recvData == b''):
                    while True:
                        self.FlagServerISconnect = False
                        if(self.CreateConnect()):
                            break
                        time.sleep(1)
                else: 
                    self.__FlagSendPingPong = False
                    self.__PhanTichKhungNhan(recvData)
            
            except:
                self.__SignalRecreateConnect.emit()
                time.sleep(0.5)
                         
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
            if( self.chuaXuLy[i:i+3].__str__().__contains__("ESM")):
                try:
                    chieuDaiDl = self.chuaXuLy[i+4] + self.chuaXuLy[i+5] * math.pow(2, 7)
                    chieuDaiKhung = i + int(chieuDaiDl) + 7
                    if(chieuDaiKhung + i <= len(self.chuaXuLy)):
                        lstKhungDL.append(self.chuaXuLy[i:chieuDaiKhung])
                        self.chuaXuLy = self.chuaXuLy[chieuDaiKhung: len(self.chuaXuLy)]
                        i = -1
                    else:
                        self.chuaXuLy = self.chuaXuLy[i: len(self.chuaXuLy)]
                        break
                except NameError as e:
                    self.chuaXuLy = self.chuaXuLy[i: len(self.chuaXuLy)]
                    print(e)
                    break
            i = i + 1
        return lstKhungDL

    def CreateConnect(self):
        # try:
        #     self.clientObj.send()

        # except:
        #     try:
        #         self.clientObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #         self.clientObj.connect((SERVER_IP, SERVER_PORT))
        #         return False
        #     except:
        #         return False
        try:
            if(not self.FlagServerISconnect):
                self.clientObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.clientObj.settimeout(200)
                self.clientObj.connect((SERVER_IP, SERVER_PORT))
                self.__SendPingPong()
                self.FlagServerISconnect = True
                self.SignalServerConnected.emit()
                return True

        except:
            self.SignalServerNotConnect.emit()
            print("khong the ket noi") #test
            self.FlagServerISconnect = False
            return False

    def __ServerConfirmedConnect(self):
        self.FlagServerConfirmedForConnect = True
        self.TimerWaitForServerConfirm.stop()


    def __PingPong(self):
        try:
            framePing = self.__ConvertJsonStringToByteArr(self.__BuildFramePingPong())
            self.clientObj.sendall(framePing)
        except:
            self.__SignalRecreateConnect.emit()

    def __BuildFramePingPong(self):
        dictData = {
            "ping":"1"
        }
        dictToSend = {
            "success":"true",
            "code":1,
            "message":"",
            "checksum":0,
            "data":dictData
        }
        return json.dumps(dictToSend)
        
    def __BuildResultToSend(self, studentNumberCard):

        dictData = {
            "cardNumber":studentNumberCard,
            "time":datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "imageLength":0
        }
        dictToSend = {
            "success":"true",
            "code":2,
            "massage":"",
            "checksum":0,
            "data":dictData
        }
        return json.dumps(dictToSend)
        
    
    def __ConvertJsonStringToByteArr(self, jsonString):
        jsonCharArr = []
        jsonString = jsonString + "\n"
        for i in range(0, len(jsonString)):
            jsonCharArr.append(ord(jsonString[i]))
        return bytes(jsonCharArr)

   
#region nhom ham gui thong tin cho server

    def SendResultsFaceRecognize(self, ID ,confirmTrueOrFalse, nameOfPhotoTaked):
        resultFrame = self.__ConvertJsonStringToByteArr(self.__BuildResultToSend(ID))
        self.__SendDataViaSocket(bytes(resultFrame))
        self.ftpObj.SendImageToFTPserver(nameOfPhotoTaked, FTP_FILE_PATH_TO_UPLOAD +"/"+ datetime.now().strftime("%Y%m%d") + '/' + str(ID)+"_"+datetime.now().strftime("%H%M%S")+ ".jpg")

#endregion
    

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

