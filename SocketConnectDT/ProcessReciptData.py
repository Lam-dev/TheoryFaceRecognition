from    PyQt5.QtCore            import pyqtSlot, pyqtSignal,QTimer, QDateTime,Qt, QObject
import  math

CODE_RICIPT_INFOMATION              = 1
CODE_GO_TO_ADD_FGP                  = 3
CODE_GO_TO_ADD_FACE                 = 2
CODE_REQUEST_WRITE_CARD             = 0

class ProcessReciptData(QObject):

    SignalGoToAddFace = pyqtSignal(str)
    SignalGoToAddFGP = pyqtSignal(str)
    SignalShowInformation = pyqtSignal(str)
    SignalRequestWriteCard = pyqtSignal(str)

    def __init__(self):
        QObject.__init__(self)

    def DetermineRequiment(self, frame):
        if((chr(frame[0]) == 'E') & (chr(frame[1]) == 'S') & (chr(frame[2]) == 'M')):
            code = frame[3]
        else:
            return
        
        if(code == CODE_RICIPT_INFOMATION):
            self.SignalShowInformation.emit(self.__CatLayPhanDataTrongFrame(frame))

        elif(code == CODE_GO_TO_ADD_FGP):
            self.SignalGoToAddFGP.emit(self.__CatLayPhanDataTrongFrame(frame))

        elif(code == CODE_GO_TO_ADD_FACE):
            self.SignalGoToAddFace.emit(self.__CatLayPhanDataTrongFrame(frame))
            
        elif(code == CODE_REQUEST_WRITE_CARD):
            self.SignalRequestWriteCard.emit(self.__CatLayPhanDataTrongFrame(frame))

    def __CatLayPhanDataTrongFrame(self, frameNhan):
        try:
            chieuDaiDl = frameNhan[4] + frameNhan[5] * math.pow(2, 8)
            duLieu = []
            j = 0
            for i in range(6, int(chieuDaiDl)+6):
                duLieu.append("")
                duLieu[j] = chr(frameNhan[i])
                j += 1
                chuoiDuLieu = ''.join(duLieu)
            return chuoiDuLieu
        except:
            return ""