
from    PyQt5.QtCore            import pyqtSlot, pyqtSignal,QTimer, QDateTime,Qt, QObject
from    collections import namedtuple
import json
import math

CODE_SERVER_ALLOW_CLONE_APP = 0
CODE_SERVER_SETTING_FOR_DEVICE = 1

class ProcessRecipt(QObject):
    SignalCloneNewApplication = pyqtSignal(object)
    SignalServerRequestCloneApp = pyqtSignal(object)
    SignalServerSettingForDevice = pyqtSignal(dict)

    def _json_object_hook(self, d): return namedtuple('X', d.keys())(*d.values())

    def json2obj(self, data): return json.loads(data, object_hook=self._json_object_hook, encoding= "utf-8")
    
    def __init__(self):
        QObject.__init__(self)
        self.chuaXuLy = b''

    def SwitchRequest(self, frameRecipt):
        lstFrame = self.__TachCacKhungTruyen(frameRecipt)
        for frame in lstFrame:
            code, content = self.__CatLayPhanDataTrongFrame(frame)
            if(code == CODE_SERVER_ALLOW_CLONE_APP):
                self.SignalServerRequestCloneApp.emit(self.json2obj(content))
            if(code == CODE_SERVER_SETTING_FOR_DEVICE):
                dictJson = json.loads(content, encoding="unicode")
                self.SignalServerSettingForDevice.emit(dictJson)

    
    """
    cat lay phan noi dung trong frame
    """
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
        return code, chuoiDuLieu

    """
    Tach du lieu nhan ra cac frame rieng re
    """

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
                except NameError as e:
                    self.chuaXuLy = self.chuaXuLy[i: len(self.chuaXuLy)]
                    print(e)
                    break
            i = i + 1
        return lstKhungDL

    """
    check sum khung truyen
    """

    def __CheckSumKhungTruyen(self, frameNhan):
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
