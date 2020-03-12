import socket
from    datetime                import datetime
from    PyQt5.QtCore            import pyqtSlot, pyqtSignal,QTimer, QDateTime,Qt, QObject
import  threading
import  math
import  time
import json
import  os
import getmac
from CheckVersionScreen.ProcessRecipt     import ProcessRecipt
from CheckVersionScreen          import GetSetting

SETTING_DICT     =  GetSetting.GetSystemSetting()
SERVER_IP  = SETTING_DICT["ecotekIP1"]
SERVER_PORT = SETTING_DICT["ecotekPort1"]

CODE_REQUEST_GET_APP = 0

class SocketClient(QObject):

    SignalServerConnecting = pyqtSignal()
    SignalServerConnected = pyqtSignal()
    SignalServerRequestCloneApp = pyqtSignal(object)
    SignalServerNotConnect = pyqtSignal()
    __SignalRecreateConnect = pyqtSignal()
    SignalServerSettingForDevice = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.waitingForConnect = False
        self.frameToSend = b''
        self.timerCreateConnect = QTimer(self)
        self.timerCreateConnect.timeout.connect(self.__ThreadCreateConnect)
        self.SignalServerConnected.connect(self.__ServerConnected)
        self.processReciptObj = ProcessRecipt()
        self.processReciptObj.SignalServerRequestCloneApp.connect(self.SignalServerRequestCloneApp.emit)
        self.processReciptObj.SignalServerSettingForDevice.connect(self.SignalServerSettingForDevice.emit)

    def CloseSocket(self):
        try:
            self.clientObj.shutdown(socket.SHUT_WR)
            self.clientObj.close()
        except:
            pass

    def __ServerConnected(self):
        self.timerCreateConnect.stop()
        self.ThreadWaitForReciptData()
        self.__SendDataViaSocket(self.BuildMessageSendCurrentVersion())


    def __ThreadCreateConnect(self):
        if(self.waitingForConnect):
            return
        thread = threading.Thread(target=self.CreateConnect, args=(), daemon = True)
        thread.start()

    def SendRequestCloneData(self):

        self.__ThreadCreateConnect()
        self.timerCreateConnect.start(5000)

    def BuildMessageSendCurrentVersion(self):
        with open('version.json') as json_file:
            crVer = json.load(json_file)["crVer"]
        message = {
            "MAC": getmac.get_mac_address(), 
            "CrStt":"DR",
            "CrVer": crVer,
            "Dv":"ELT",
        }
        return self.__DungKhungGiaoTiep(json.dumps(message), CODE_REQUEST_GET_APP)


    def __SendDataViaSocket(self, data):
        try:
            self.clientObj.send(data)

        except:
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
                    # self.__FlagSendPingPong = False
                    # lstCacKhungNhan = self.__TachCacKhungTruyen(recvData)
                    # for khung in lstCacKhungNhan:
                    #     self.__PhanTichKhungNhan(khung)
                    self.processReciptObj.SwitchRequest(recvData)
            except:
                self.__SignalRecreateConnect.emit()
                return

    def CreateConnect(self):
        global SERVER_IP, SERVER_PORT
        self.waitingForConnect = True
        try:
            if(not self.FlagServerISconnect):
                self.clientObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.clientObj.connect((SERVER_IP, SERVER_PORT))
                self.SignalServerConnected.emit()

        except:
            self.SignalServerNotConnect.emit()
            print("khong the ket noi") #test
            self.FlagServerISconnect = False
        self.waitingForConnect = False


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





