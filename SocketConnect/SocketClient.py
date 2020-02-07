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

SETTING_DICT                                        = GetSetting.LoadSettingFromFile()
SERVER_IP                                           = SETTING_DICT["serverIP"]
SERVER_PORT                                         = int(SETTING_DICT["serverPort"])

MAC                                                 = "1234"

CODE_RECIPT_DATA_FROM_SERVER = "3"
CODE_UPLOAD_DATA_TO_SERVER = "2"
CODE_PING_PING = "1"

MAC_ADDRESS                                         = "11111"#[0xC8, 0X93, 0X46, 0X4E,0X5D,0XD9]C8-93-46-4E-5D-D9
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
    SignalUpdateOrSyncStudentInfo = pyqtSignal(dict)
    __SignalConnected = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ftpObj = FTPclient()
        self.timerPingPong = QTimer(self)
        self.timerPingPong.timeout.connect(self.__PingPong)

        self.__SignalConnected.connect(self.__ServerConnected)

        self.processReciptDataObj = ProcessReciptData()
        self.processReciptDataObj.ShowStudentForConfirm.connect(self.__ShowStudentForConfirmSlot)
        self.processReciptDataObj.ServerConfirmedConnect.connect(self.__ServerConfirmedConnect)
        self.processReciptDataObj.ResponseRequestUpdataFromServer.connect(self.__ResponseResquestUpdateDatabaseFromServer)
        self.processReciptDataObj.SignalUpdateDataBaseSuccess.connect(self.__UpdateDataBaseSuccess)
        self.processReciptDataObj.SignalNumberStudentParsed.connect(self.__NumberStudentParsed)
        self.processReciptDataObj.SignalUpdateOrSyncStudentInfo.connect(self.SignalUpdateOrSyncStudentInfo.emit)
        self.chuaXuLy = b''

        self.TimerWaitForServerConfirm = QTimer(self)
        self.TimerWaitForServerConfirm.timeout.connect(self.__ThreadCreateConnect)
        self.TimerWaitForServerConfirm.start(2000)

        self.FlagServerConfirmedForConnect = False
        self.FlagServerISconnect = False
        self.clientObj = ""
        
        self.ThreadWaitForReciptData()
        self.__TimerSendPingPong = QTimer(self)
        self.__TimerSendPingPong.timeout.connect(self.__SendPingPong)
        self.__SignalRecreateConnect.connect(self.__RecreateConnect)
        self.__FlagSendPingPong = True
        self.waitingForConnect = False
    
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
        global SERVER_IP, SERVER_PORT
        SERVER_IP = serverInfoDict["serverIP"]
        SERVER_PORT = int(serverInfoDict["serverPort"])
        self.FlagServerISconnect = False
        self.CreateConnect()

    def CreateConnect(self):
        global SERVER_IP, SERVER_PORT
        self.waitingForConnect = True
        try:
            if(not self.FlagServerISconnect):
                self.clientObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.clientObj.settimeout(0.5)
                self.clientObj.setblocking(1)
                self.clientObj.connect((SERVER_IP, SERVER_PORT))
                self.clientObj.send(self.__DungKhungGiaoTiep(MAC_ADDRESS, CLIENT_REQUEST_CONNECT)[0])
                self.SignalServerConnected.emit()
                self.__SignalConnected.emit()

        except:
            self.SignalServerNotConnect.emit()
            print("khong the ket noi") #test
            self.FlagServerISconnect = False
        self.waitingForConnect = False

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
        self.FlagServerISconnect = False
        if(not self.TimerWaitForServerConfirm.isActive()):
            self.TimerWaitForServerConfirm.start(2000)

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
                print(recvData)
                len(recvData)
                if(recvData == b''):
                    self.__SignalRecreateConnect.emit()
                    return
                else: 
                    self.__FlagSendPingPong = False
                    self.__PhanTichKhungNhan(recvData)
            
            except:
                self.__SignalRecreateConnect.emit()
                return
                         
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

    def CreateConnect(self):
        global SERVER_IP, SERVER_PORT
        self.waitingForConnect = True
        try:
            if(not self.FlagServerISconnect):
                self.clientObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
            framePing = self.__ConvertJsonStringToByteArr(self.__BuildFramePingPong())
            self.clientObj.sendall(framePing)

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

        dictData = {
            "cardNumber":studentNumberCard,
            "time":datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
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

   
#region nhom ham gui thong tin cho server

    def SendResultsFaceRecognize(self, ID ,confirmTrueOrFalse, nameOfPhotoTaked):
        imageFileName = FTP_FILE_PATH_TO_UPLOAD +"/"+ datetime.now().strftime("%Y%m%d") + '/' + str(ID)+"_"+datetime.now().strftime("%H%M%S")+ ".jpg"
        resultFrame = self.__ConvertJsonStringToByteArr(self.__BuildResultToSend(ID, imageFileName, "Face"))
        self.__SendDataViaSocket(bytes(resultFrame))
        thread = threading.Thread(target = self.ftpObj.SendImageToFTPserver, args = (nameOfPhotoTaked, imageFileName), daemon= True)
        thread.start()
        # self.ftpObj.SendImageToFTPserver(nameOfPhotoTaked, FTP_FILE_PATH_TO_UPLOAD +"/"+ datetime.now().strftime("%Y%m%d") + '/' + str(ID)+"_"+datetime.now().strftime("%H%M%S")+ ".jpg")


    def SendResultsFGPrecognition(self, ID):
        resultFrame = self.__ConvertJsonStringToByteArr(self.__BuildResultToSend(ID, "", "FGP"))
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
        resultFrame = self.__ConvertJsonStringToByteArr(jsonStr)
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

