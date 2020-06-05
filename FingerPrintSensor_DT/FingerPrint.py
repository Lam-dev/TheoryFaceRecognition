from    FingerPrintSensor.FingerprintLib    import PyFingerprint
from    PyQt5.QtCore       import QRect, QPropertyAnimation, QTimer, pyqtSignal, pyqtSlot, QObject
import  time
from    PIL import Image
import  _thread
import  threading
import  os
from    datetime import datetime
import enum


class Fingerprint(QObject):
    SignalNewFGPadded = pyqtSignal(int, list)
    SignalRecognizedFGP = pyqtSignal(int)
    SignalFGPnotFind = pyqtSignal()
    SignalHandPushed = pyqtSignal()
    SignalDowloadedImage = pyqtSignal(str)
    SignalFGPget = pyqtSignal(str)
    SignalFGPputOnIsTheSame = pyqtSignal()
    SignalPlayBip = pyqtSignal()
    SignalRequestPushOn = pyqtSignal()
    SignalRequestPushOff = pyqtSignal()
    SignalStepSuccess = pyqtSignal(int)
    SignalNotify = pyqtSignal(object)

    def __init__(self, port = '/dev/ttyACM0', baudRate = 57600, address = 0xFFFFFFFF, password = 0xFFFFFFFF):
        super().__init__()
        self.port = port
        self.baudRate = baudRate
        self.address = address
        self.password = password
        try:
            self.fingerprintObj = PyFingerprint(port, baudRate, address, password)
            self.fingerprintObj.verifyPassword()
        except Exception as ex:
            print(str(ex.args))
            self.fingerprintObj = False
        self.timerDownloadFGPimage = QTimer()
        self.timerDownloadFGPimage.timeout.connect(self.ThreadDownloadFGPimage)

        self.timerGetFGPfeature = QTimer()
        self.timerGetFGPfeature.timeout.connect(self.ThreadGetFGPfeature)

        self.lstIDvaVanTay = []
        self.viTriDaChonChuaLuu = []
        self.FlagFGPfree = True
        self.__FlagLockFGPsensor = False
        self.__addFGPstep = 1
        self.__fingerPrintHoldOn = False
        self.__numberWrongPrePos = 0

    def ThreadGetFGPfeature(self):
        #thread = threading.Thread(target = self.GetFGPfeature)
        thread = threading.Thread(target = self.AddFGPstepByStep)
        thread.start()
    
    def StartGetFGP(self):
        self.timerGetFGPfeature.start(700)
    
    def StopGetFGP(self):
        self.timerGetFGPfeature.stop()

    # def StartDownloadImage(self):
    #     self.timerDownloadFGPimage.start(1000)
    
    # def StopDownloadImage(self):
    #     self.timerDownloadFGPimage.stop()

    def ThreadDownloadFGPimage(self):
        if(self.FlagFGPfree):
            self.FlagFGPfree = False
            thread = threading.Thread(target = self.GetFGPfeature, args=(), daemon= True)
            thread.start()

    def DownloadFGPimage(self):
        try:
            if(type(self.fingerprintObj) is not bool):
                if(self.fingerprintObj.readImage()):
                    imageName = datetime.now().strftime("%H_%M_%S")+".bmp"
                    imageDir = os.getcwd() + "/" + imageName
                    self.fingerprintObj.downloadImage(imageDir)
                    self.SignalDowloadedImage.emit(imageName)
            else:
                self.fingerprintObj = PyFingerprint(self.port, self.baudRate, self.address, self.password)
                self.fingerprintObj.verifyPassword()
        except:
            self.fingerprintObj = False
        self.FlagFGPfree = True        

    def ClearFGPfeatureSaveOnSensor(self):
        try:
            self.fingerprintObj.clearDatabase()
            self.__addFGPstep = 1
        except:
            pass
    
    def AddFGPstepByStep(self):
        if(self.__FlagLockFGPsensor):
            return
        self.__FlagLockFGPsensor = True
        if(self.__addFGPstep  == 1):
            print("buoc 1")
            try:
                if(self.fingerprintObj.readImage()):        # nếu đọc được ảnh vân tay(tức là có ngón tay)
                    try:
                        self.fingerprintObj.convertImage(0x01)
                        self.SignalStepSuccess.emit(1)
                    except:
                        self.__fingerPrintHoldOn = True
                    self.__fingerPrintHoldOn = True
                    self.__addFGPstep = 2
                else:
                    self.__fingerPrintHoldOn = False
            except Exception as ex:
                
                print(ex.args)

        elif(self.__addFGPstep == 2):
            print("buoc 2")
            try:
            
                if(self.fingerprintObj.readImage()):
                    if(self.__fingerPrintHoldOn):
                        self.SignalNotify.emit(AddFingerNotify.PushOff)
                        self.SignalRequestPushOff.emit()
                    else:
                        try:
                            self.fingerprintObj.convertImage(0x02)
                        except:
                            self.__fingerPrintHoldOn = True
                        if(not self.fingerprintObj.createTemplate()):
                            self.__numberWrongPrePos += 1
                            if(self.__numberWrongPrePos == 4):
                                self.SignalStepSuccess.emit(1)
                                self.__addFGPstep = 1
                                self.__numberWrongPrePos = 0
                            
                            self.SignalNotify.emit(AddFingerNotify.WrongPose)
                        else:
                            self.SignalStepSuccess.emit(2)
                            self.__fingerPrintHoldOn = True
                            self.__addFGPstep = 3
                else:
                    self.__fingerPrintHoldOn = False
                    self.SignalRequestPushOn.emit()
                    self.SignalNotify.emit(AddFingerNotify.PushOn)
            except Exception as ex:
                print("LTVTB2"+ str(ex.args))
        elif(self.__addFGPstep == 3):
            print("buoc 3")
            try:
                if(self.fingerprintObj.readImage()):
                    if(self.__fingerPrintHoldOn):
                        self.SignalNotify.emit(AddFingerNotify.PushOff)
                        self.SignalRequestPushOff.emit()

                    else:
                        try:
                            self.fingerprintObj.convertImage(0x02)
                        except:
                            self.__fingerPrintHoldOn = True
                        if(not self.fingerprintObj.createTemplate()):
                            self.__numberWrongPrePos += 1
                            if(self.__numberWrongPrePos == 4):
                                self.SignalStepSuccess.emit(2)
                                self.__addFGPstep = 1
                                self.__numberWrongPrePos = 0

                            self.SignalNotify.emit(AddFingerNotify.WrongPose)
                        else:
                            self.SignalNotify.emit(AddFingerNotify.Ok)
                            self.SignalStepSuccess.emit(3)
                            self.DownloadCharacteristic()
                            self.__fingerPrintHoldOn = True
                            self.__addFGPstep = 3
                            
                else:
                    self.__fingerPrintHoldOn = False
                    self.SignalRequestPushOn.emit()
                    self.SignalNotify.emit(AddFingerNotify.PushOn)
            except Exception as ex:
                print("LTVTB3"+ str(ex.args))
                
        self.__FlagLockFGPsensor = False
            
    def DownloadCharacteristic(self):
        try:
            lstFGPfeature = self.fingerprintObj.downloadCharacteristics(0x01) #Đọc mẫu lên
            lstFGPfeatureStrElem = [str(elem) for elem in lstFGPfeature]
            FGPfeatureString = ",".join(lstFGPfeatureStrElem)
            self.SignalFGPget.emit(FGPfeatureString)
        except Exception as ex:
            raise ex
            

    def GetFGPfeature(self):
        if(self.__FlagLockFGPsensor):
            return
        self.__FlagLockFGPsensor = True
        try:
            if(self.fingerprintObj.readImage()):        # nếu đọc được ảnh vân tay(tức là có ngón tay)
                self.fingerprintObj.convertImage(0x01)  # Chuyển ảnh vân tay thành đặc trưng lưu vào Charbuffer1
                self.fingerprintObj.readImage()         # Tiếp tục đọc ảnh vân tay
                self.fingerprintObj.convertImage(0x02)  # Chuyển thành đặc trưng lưu vào Charbuffer2
                result = self.fingerprintObj.createTemplate()  #Chập 2 vân tay thành 1 mẫu
                self.fingerprintObj.readImage()
                self.fingerprintObj.convertImage(0x02)
                result = self.fingerprintObj.createTemplate()
                if(result):                             
                
                    lstFGPfeature = self.fingerprintObj.downloadCharacteristics(0x01) #Đọc mẫu lên
                    lstFGPfeatureStrElem = [str(elem) for elem in lstFGPfeature]
                    FGPfeatureString = ",".join(lstFGPfeatureStrElem)
                    self.SignalFGPget.emit(FGPfeatureString)
                
                
        except Exception as ex:
            print(ex.args)
            self.__FlagLockFGPsensor = False
        self.__FlagLockFGPsensor = False
    

class AddFingerNotify(enum.Enum):
    WrongPose = 0
    PushOn = 1
    PushOff = 2
    Ok = 3
    