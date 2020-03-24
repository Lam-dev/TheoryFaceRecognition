import serial
import time
import os
import threading
from      PyQt5.QtCore   import pyqtSlot, pyqtSignal,QTimer, QDateTime,Qt, QObject
from GetSettingFromJSON    import GetSetting

uartSettingDict = GetSetting.GetUARTsetting()
try:    
    UART_PORT = uartSettingDict["UARTport"]
    UART_SPEED = uartSettingDict["baudrate"]
except:
    pass

class UART(QObject):

    SignalReciptedData = pyqtSignal(bytes)
    
    def __init__(self):
        super().__init__()
        #self.serObj = self.__UARTinit()

    def __UARTinit(self):
        try:
            return serial.Serial(
            port=UART_PORT,
            baudrate = UART_SPEED,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout= 0.8)
        except NameError:
            return False

    def ThreadListenUART(self):
        thread = threading.Thread(target=self.__UARTlisten, args=(), daemon= True)
        thread.start()

    def __UARTlisten(self):
        while True:
            self.serObj = self.__UARTinit()
            print("Khoi Tao uart")
            time.sleep(1)
            if(type(self.serObj)is not bool):
                while True:
                    try:
                        if(self.serObj.inWaiting() > 0):
                            data = self.serObj.read(1024)
                            print("Khung Nhan = ", data)
                            self.SignalReciptedData.emit(data)
                            pass
                    except NameError as e:
                        print(e)

    
    def SendDataToUART(self, frame):
        try:
            self.serObj.write(frame)
        except:
            pass