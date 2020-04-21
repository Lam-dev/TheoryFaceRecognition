import socket
from    socket import SHUT_RDWR
from    datetime                import datetime
from    PyQt5.QtCore            import pyqtSlot, pyqtSignal,QTimer, QDateTime,Qt, QObject
import  threading
from    SocketConnectDT.ProcessReciptData   import ProcessReciptData
import  math
import  time
from    SocketConnectDT.FTPclient import FTPclient
from    GetSettingFromJSON    import GetSetting
import json
import  os


try:
    SETTING_DICT                                        = GetSetting.LoadSettingFromFile()
    SERVER_IP                                           = SETTING_DICT["serverIP_DT"]
    SERVER_PORT                                         = int(SETTING_DICT["serverPort_DT"])
except:
    SERVER_IP = "0.0.0.0"
    SERVER_PORT = 0

MAC                                                 = "1234"

CODE_SEND_FGP_FEATURE                 = 5
CODE_SENDED_FINGER_IMAGE              = 3
CODE_SEND_FACE_IMAGE                  = 4
CODE_SEND_NOTIFY_WRITE_CARD_SUCCESS   = 6


MAC_ADDRESS                                         = "123456"#[0xC8, 0X93, 0X46, 0X4E,0X5D,0XD9]C8-93-46-4E-5D-D9
IMAGE_TO_SEND_SERVER_PATH                           = "/StudentRecognize/SocketConnect/"
FTP_FILE_PATH_TO_UPLOAD                             = GetSetting.GetSetting("--ServerImageDir")

class SocketClientDT(QObject):
    
    __SignalRecreateConnect = pyqtSignal()
    SignalServerNotConnect = pyqtSignal()
    SignalServerConnected = pyqtSignal()
    SignalConnectNewServer = pyqtSignal(dict)
    SignalConnectNewFTP = pyqtSignal(dict)
    __SignalConnected = pyqtSignal()
    SignalRequestWriteCard = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.ftpObj = FTPclient()
        # self.timerPingPong = QTimer(self)
        # self.timerPingPong.timeout.connect(self.__PingPong)

        self.__SignalConnected.connect(self.__ServerConnected)

        self.callBackShowStatusConnectToSetting = object

        self.processReciptDataObj = ProcessReciptData()
        self.processReciptDataObj.SignalRequestWriteCard.connect(self.SignalRequestWriteCard.emit)

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

    def SendNotifyWriteRFcardSuccessfully(self):
        self.__SendDataViaSocket(self.__DungKhungGiaoTiepUART("", CODE_SEND_NOTIFY_WRITE_CARD_SUCCESS)[0])

    def ConnectNewFTP(self, dictInfor, callbackShowStatus):
        callbackShowStatus(self.ftpObj.ConnectNewFTPserver(dictInfor))

    def SocketConnectNewServer(self, dictInfor, callback):
        global SERVER_IP, SERVER_PORT
        SERVER_IP = dictInfor["serverIP"]
        SERVER_PORT = dictInfor["serverPort"]
        self.FlagServerISconnect = False
        self.callBackShowStatusConnectToSetting = callback
        self.__SignalRecreateConnect.emit()


    def CloseConnect(self):
        try:
            self.clientObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.clientObj.
            self.clientObj.shutdown(SHUT_RDWR)
            self.clientObj.close()


        except Exception as ex:
            print(ex)

    def SendTakedImage(self, featureStr = ""):
        imageNameToServer = "face"+datetime.now().strftime("%Y%m%d%H%M%S")
        self.ftpObj.SendImageToFTPserver("imageToSend.jpg", "/files/FGPimage/"+ imageNameToServer +".jpg")
        if(featureStr == ""):
            findFace = False
        else:
            findFace = True

        dictData = {
            "faceFeature":featureStr
        }
        with open('FaceFeatureFileToSend.txt', 'w') as outfile:
            json.dump(dictData, outfile)

        self.ftpObj.SendImageToFTPserver('FaceFeatureFileToSend.txt', "/files/FGPimage/"+imageNameToServer+'.txt')
        os.remove('FaceFeatureFileToSend.txt')

        dictMessage = {
            "containFace":findFace,
            "imageName":imageNameToServer,
        }
        jsonStr = json.dumps(dictMessage)
        self.__SendDataViaSocket(self.__DungKhungGiaoTiepUART(jsonStr, CODE_SEND_FACE_IMAGE)[0])

    def __ServerConnected(self):
        try:
            self.FlagServerISconnect = True
            self.TimerWaitForServerConfirm.stop()
            self.ThreadWaitForReciptData()
            #self.timerPingPong.start(30000)
            try:
                self.callBackShowStatusConnectToSetting(True)
            except:
                pass
        except NameError:
            pass
    
    def SendFingerFeature(self, featureStr, fingerName):
        FGPfileNameToServer = "FGP"+datetime.now().strftime("%Y%m%d%H%M%S")
        dictMessage = {
            "fingerName":fingerName,
            "fileName":FGPfileNameToServer
        }
        jsonMessage = json.dumps(dictMessage)
        dictData = {
            "fingerName":fingerName,
            "feature":featureStr
        }
        with open('FGPfeatureFileToSend.txt', 'w') as outfile:
            json.dump(dictData, outfile)
        self.ftpObj.SendImageToFTPserver('FGPfeatureFileToSend.txt', "/files/FGPimage/"+FGPfileNameToServer+'.txt')
        os.remove('FGPfeatureFileToSend.txt')
        self.__SendDataViaSocket(self.__DungKhungGiaoTiepUART(jsonMessage ,CODE_SEND_FGP_FEATURE)[0])
        

    def SendFingerImage(self, nameImage, ngon):
        dictMessage = {
            "tenAnh":nameImage,
            "ngon":ngon
        }
        jsonDict = json.dumps(dictMessage)
        self.__SendDataViaSocket(self.__DungKhungGiaoTiepUART(jsonDict ,CODE_SENDED_FINGER_IMAGE)[0])
        self.ftpObj.SendImageToFTPserver(nameImage, "/files/FGPimage/"+nameImage)

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
        self.waitingForConnect = True
        global SERVER_IP, SERVER_PORT
        try:
            if(not self.FlagServerISconnect):
                self.clientObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.clientObj.settimeout(0.5)
                self.clientObj.setblocking(1)
                self.clientObj.connect((SERVER_IP, SERVER_PORT))
                # self.clientObj.send(self.__DungKhungGiaoTiep(MAC_ADDRESS, CLIENT_REQUEST_CONNECT)[0])
                self.SignalServerConnected.emit()
                self.__SignalConnected.emit()

        except:
            try:
                self.callBackShowStatusConnectToSetting(False)
            except:
                pass
            self.SignalServerNotConnect.emit()
            print("khong the ket noi") #test
            self.FlagServerISconnect = False
        self.waitingForConnect = False

    def __SendPingPong(self):
        if(self.__FlagSendPingPong):
            self.__PingPong()
        else:
            self.__FlagSendPingPong = True

    def __SendDataViaSocket(self, data):
        try:
            self.clientObj.send(data)
            self.__FlagSendPingPong = False
        except:
            self.FlagServerISconnect
            self.__SignalRecreateConnect.emit()

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
            self.processReciptDataObj.DetermineRequiment(khungNhan)
                    
        except:
            print("khung trong")

    def __CheckSumKhungTruyen(self, frameNhan):
        # return True ## test
        try:
            tong = 0
            for i in range (3, len(frameNhan) - 1):
                tong = tong + frameNhan[i]
            tong = -(~tong) % 256

            if(tong == frameNhan[len(frameNhan)-1]):
                return True
            else:
                return False
        except:
            return False

    def __DungKhungGiaoTiepUART(self, noiDung, maLenh):
        if(type(noiDung) is not str): 
            return False, False
        highChieuDaiTen = int(len(noiDung) / 256)
        lowChieuDaiTen = int(len(noiDung) % 256)
        khungTruyen = [0x45, 0x54, 0x4D, maLenh, lowChieuDaiTen, highChieuDaiTen]
        tong = 0x02 + highChieuDaiTen + lowChieuDaiTen
        j = 0
        for i in range (len(khungTruyen), len(khungTruyen) + len(noiDung)):
            khungTruyen.append('')
            khungTruyen[i] = ord(noiDung[j])
            tong = tong + ord(noiDung[j])
            j = j+ 1
            
        tong = -(~tong) % 256
        khungTruyen.append(0x00)
        khungTruyen[len(khungTruyen)-1] = tong
        return bytes(khungTruyen), tong

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
                    chieuDaiDl = self.chuaXuLy[i+4] + self.chuaXuLy[i+5] * math.pow(2, 8)
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

    def __ServerConfirmedConnect(self):
        self.FlagServerConfirmedForConnect = True
        self.TimerWaitForServerConfirm.stop()
        
    def SendDatabaseCheckFile(self, fileName):

        thread = threading.Thread(target = self.ftpObj.SendImageToFTPserver, args = (fileName, FTP_FILE_PATH_TO_UPLOAD +"/"+fileName), daemon= True)
        thread.start()
    
    def SendDatabaseCheckMessage(self, message):
        resultFrame = self.__ConvertJsonStringToByteArr(message)
        self.__SendDataViaSocket(bytes(resultFrame))
