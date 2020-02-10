import      serial
import      time
import      os
import      threading
import      _thread
from        PyQt5.QtCore   import pyqtSlot, pyqtSignal,QTimer, QDateTime,Qt, QObject
import      math
import      json
import      socket

HOST = ''  # Standard loopback interface address (localhost)
PORT = 2020   # Port to listen on (non-privileged ports are > 1023)

class SocketServerForRFID(QObject):
    SignalRFIDputOn = pyqtSignal(str)
    KhongCoGPS = pyqtSignal()
    TinHieuGPS = pyqtSignal(float, float, float)
    ThemThiSinh = pyqtSignal(object)
    YeuCauChupAnhGuiLenServer = pyqtSignal(int)
    YeuCauCapNhatNgayDuLieuDuongDi = pyqtSignal()
    NhanDuocKhuonMatTuUART = pyqtSignal(int, list)
    __SignalGPSconnectAvailable = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.connObject = False# = self.__KhoiTaoSocketPort()
        self.socketObject = False
        self.hangDoiGuiXuongUART = HangDoi()
        self.hangDoiGuiXuongUART.DangCho.connect(self.__BatThreadGuiThongTinXuongUART)
        self.hangDoiXuLyDuLieu = HangDoi()
        self.hangDoiXuLyDuLieu.DangCho.connect(self.__BatThreadXuLyTepGuiXuongTuServer)
        self.hangDoiTraLoi = HangDoi()
        self.flagThreadGuiUART = False
        self.flagThreadXuLyFile = False
        self.chuaXuLy = b''
        self.daHoacKhongCanPhanHoi = True
        self.thoiGianMatGPS = 0
        threadKhoiTaoSocketPort = threading.Thread(target = self.__KhoiTaoSocketPort, args=(), daemon = True)
        threadKhoiTaoSocketPort.start()
        threadLangNgheSerialPort = threading.Thread(target= self.__LangNgheSocketPort, args=(), daemon= True)
        threadLangNgheSerialPort.start()

        self.timerTGmatGPS = QTimer()
        self.timerTGmatGPS.timeout.connect(self.__MatGPS)
        self.timerTGmatGPS.start(5000)
        self.phanThuaKhungTruoc = ''
        # self.Thread_xlTepGuiTuServer = threading.Thread(target = self.ThreadXuLyTepGuiXuongTuServer, args=(), daemon=True)
        # self.Thread_GuiThongTinXuongUART = threading.Thread(target = self.ThreadGuiThongTinXuongUART, args = (), daemon = True)
        self.IDnguoiLai = ""
        self.currentSpeed = 0

        self.__SignalGPSconnectAvailable.connect(self.__GPSavailable)
    
    # def __ThoiGianMatGPS(self):
    #     if(self.thoiGianMatGPS >= 5 ):
    #         self.KhongCoGPS.emit()    
    #     else:
    #         self.thoiGianMatGPS += 1

    def __GPSavailable(self):
        self.timerTGmatGPS.stop()
        self.timerTGmatGPS.start(5000)

    def __MatGPS(self):
        self.KhongCoGPS.emit()

    def __BatThreadGuiThongTinXuongUART(self):
        if(not self.flagThreadGuiUART):
            _thread.start_new_thread(self.__ThreadGuiThongTinSocketPort, ())
            self.flagThreadGuiUART = True

    def __BatThreadXuLyTepGuiXuongTuServer(self):
        if(not self.flagThreadXuLyFile):
            _thread.start_new_thread(self.ThreadXuLyTepGuiXuongTuServer, ())
            self.flagThreadXuLyFile = True
    
    def __ThreadGuiThongTinSocketPort(self):
        khungGui = self.hangDoiGuiXuongUART.ConnectAllFrame() + khungGuiIDthiSinh + self.hangDoiTraLoi.ConnectAllFrameAndClear()
        try:
            self.connObject.sendall(banTinGui['khungGui'])
        except:
            pass
        print("DA GUI:", khungGui)
        
    def ThreadXuLyTepGuiXuongTuServer(self):
        while(self.hangDoiXuLyDuLieu.size() > 0):
            tenFileCanXL = self.hangDoiXuLyDuLieu.dequeue()
            if(tenFileCanXL == "Queue Empty!"):
                return
            else:
                try:
                    self.XuLyTepGuiXuongTuServer(tenFileCanXL)
                    pass
                except:
                    pass
        self.flagThreadXuLyFile = False

    def __KhoiTaoSocketPort(self):
        self.socketObject = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketObject.bind((HOST, PORT))
        self.socketObject.listen()
        # conn, addr = s.accept()
        # self.connObject = conn

    def __LangNgheSocketPort(self):
        while True:
            try:
                if(type(self.socketObject) is not bool):
                    self.connObject, _ =  self.socketObject.accept()
                
                    while True:
                        try:
                            khungNhan = self.connObject.recv(1024)
                            print("Khung Nhan = ", khungNhan)
                            if(not khungNhan):
                                break
                            lstCacKhungNhan = self.__TachCacKhungTruyen(khungNhan)
                            for khung in lstCacKhungNhan:
                                self.__PhanTichKhungNhan(khung)
                            # self.__PhanTichKhungNhan(khungNhan)
                            pass
                        except:
                            break
            except:
                pass
    """
    khung truyen uart yeu cau module 3g gui file
    tham so
        tenFile: ten cua file can gui
    tra ve
        khungTruyen: khong truyen de gui cho ETM module
        tong : checksum cua khung truyen 
    """
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

    """
    Gui ID thi sinh dang lai xe cho server
    """
    
    def SendRequestWriteNumberToCard(self, txtNumber):
        khungGui, tong = self.__DungKhungGiaoTiepUART(txtNumber, 9)
        if(type(khungGui) is bool):
            return
        self.hangDoiGuiXuongUART.enqueue(khungGui)
    
 
    """
    Gui yeu cau gui file xuong UARt
    """
    def GuiFile(self, tenFile):
        khungTruyen, tong = self.__DungKhungGiaoTiepUART(tenFile, 2)
        if(type(khungTruyen) is bool):
            return
        self.hangDoiGuiXuongUART.enqueue(khungTruyen)   

    """
    phan tich khung nhan duoc tu uart va xu ly khung
    tham so
        khungNhan: Khung nhan duoc tu UART
    """
    def __PhanTichKhungNhan(self, khungNhan):
        # khungNhan = b'ETM\x00\x48\x00$GPRMC,173948.823,A,2101.44906,N,10551.851426,E,3.34, 223.95,2sy806,,*04\xe5'
        # khungNhan = b'ETM\x02(\x00TTHV_29A-888888_2019-09-19_14-58-13.json\x28'
        # print(khungNhan)
        try:
            if(not self.__CheckSumKhungTruyen(khungNhan)):
                return
        
            if((chr(khungNhan[0]) == 'E') & (chr(khungNhan[1]) == 'T') & (chr(khungNhan[2]) == 'M')):
                code = khungNhan[3]
                if(code == 0):
                    try:
                        self.XuLyBanTinGPS( self.__CatLayPhanDataTrongFrame(khungNhan))
                    except:
                        pass
                    self.SendIDAndCurrentSpeedToServer("0", "3")
                    
                elif(code == 1):
                    self.hangDoiXuLyDuLieu.enqueue(self.__CatLayPhanDataTrongFrame(khungNhan))
                    self.hangDoiTraLoi.enqueue(khungNhan)
                    # self.hangDoiGuiXuongUART.enqueue(lenhCho)
                elif(code == 2):
                    self.hangDoiGuiXuongUART.remove(khungNhan)
                
                elif(code == 8):
                    self.__XuLyDuLieuRFID(self.__CatLayPhanDataTrongFrame(khungNhan))

                elif(code == 10):
                    self.__XuLyCacLenhServerYeuCau(self.__CatLayPhanDataTrongFrame(khungNhan))
                    
        except:

            print("khung trong")

    def __XuLyDuLieuRFID(self, lenh):
        self.SignalRFIDputOn.emit(lenh)

    """
    Xu ly cac lenh server yeu cau
    """
    def __XuLyCacLenhServerYeuCau(self, lenh):
        if(lenh.__contains__("CA")):
            try:
                lenhArr = lenh.split("_")
                self.YeuCauChupAnhGuiLenServer.emit(int(lenhArr[1]))
            except:
                self.YeuCauChupAnhGuiLenServer.emit(50)
        elif(lenh.__contains__("CNDD")):
            self.YeuCauCapNhatNgayDuLieuDuongDi.emit()
        

    """
    Xu ly tep duoc gui ve tu server
    """
    def XuLyTepGuiXuongTuServer(self, tenTep):
        pass

    """
    Cat lay phan du lieu trong khung truyen. Luoc bo phan ky hieu ETM, code va checksum
    tham so: 
        frameNhan : khung truyen nhan duoc.
    tra ve
        str_data : 
    """
    def __CatLayPhanDataTrongFrame(self, frameNhan):
        chieuDaiDl = frameNhan[4] + frameNhan[5] * math.pow(2, 7)
        duLieu = []
        j = 0
        for i in range(6, int(chieuDaiDl)+6):
            duLieu.append("")
            duLieu[j] = chr(frameNhan[i])
            j += 1
            chuoiDuLieu = ''.join(duLieu)
        return chuoiDuLieu


    """
    tinh sum cua khung truyen va kiem tra voi gia tri check sum di kem
    tham so
        frameNhan: khung nhan duoc server
    tra ve:
        true: neu frame dung
        false: new frame sai
    """
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
    
    """
    Xy ly ban tin GPRMC. 
    """

    def checksum(self, lenh):
        tong = 0
        for i in range (0, len(lenh)):
            tong = tong + ord(lenh[i])
          
        tong = -(~tong) % 256
        #print(tong) #test

    def __TachCacKhungTruyen(self, duLieu):
        if(duLieu == b''):
            return []
        self.chuaXuLy = self.chuaXuLy + duLieu
        lstKhungDL = []
        for i in range(0, len(self.chuaXuLy)):
            if( self.chuaXuLy[i:i+3].__str__().__contains__("ETM")):
                try:
                    chieuDaiDl = self.chuaXuLy[i+4] + self.chuaXuLy[i+5] * math.pow(2, 7)
                    chieuDaiKhung = i + int(chieuDaiDl) + 7
                    if(chieuDaiKhung + i <= len(self.chuaXuLy)):
                        lstKhungDL.append(self.chuaXuLy[i:chieuDaiKhung])
                        #self.chuaXuLy = self.chuaXuLy[chieuDaiKhung: len(self.chuaXuLy)]
                        i = i + chieuDaiKhung
                    else:
                        self.chuaXuLy = self.chuaXuLy[i: len(self.chuaXuLy)]
                        break
                except:
                    self.chuaXuLy = self.chuaXuLy[i: len(self.chuaXuLy)]
                    break
        return lstKhungDL

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
        return connectedFrame
        self.queue.clear()


# x = HangDoi()
# x.enqueue("a")
# x.enqueue("b")
# x.enqueue("c")
# print(x.printQueue())
# x.remove("b")
# print(x.printQueue())
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((HOST, PORT))
# s.listen()
# conn, addr = s.accept()
# with conn as a:
#     while True:
#         data = a.recv(1024)
#         print(len(data))
#         if not data:
#             break
#         a.sendall(b'hay lam day nay')
    