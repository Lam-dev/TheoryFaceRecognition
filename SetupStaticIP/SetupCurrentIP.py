from        SetupStaticIP.SetupCurrentIPui   import Ui_Frame
from        PyQt5.QtCore    import pyqtSlot, pyqtSignal,QTimer, QDateTime,Qt, QObject
from        PyQt5.QtGui     import QPixmap
from        PyQt5           import QtWidgets, QtGui, QtCore
from        PIL             import Image, ImageQt



class SetupStaticIP(QObject, Ui_Frame):
    SignalShowKeyBoard = pyqtSignal(object)
    def __init__(self, frame):
        QObject.__init__(self)
        Ui_Frame.__init__(self)
        self.frameContain = frame
        self.setupUi(frame)
        frame.setGeometry((800 - frame.width())/2, (480 - frame.height())/30, frame.width(), frame.height())
        frame.show()
        self.checkFailPixmap = QtGui.QPixmap("icon/iconCheckFail.png")
        self.checkOKpixmap = QtGui.QPixmap("icon/iconCheckOk.png")
        self.lineEdit_ip.mouseReleaseEvent = lambda event: self.SignalShowKeyBoard.emit(self.lineEdit_ip)
        self.lineEdit_subnetMask.mouseReleaseEvent = lambda event: self.SignalShowKeyBoard.emit(self.lineEdit_subnetMask)
        self.lineEdit_gateWay.mouseReleaseEvent = lambda event: self.SignalShowKeyBoard.emit(self.lineEdit_gateWay)
        self.lineEdit_preDNSeDNS.mouseReleaseEvent = lambda event: self.SignalShowKeyBoard.emit(self.lineEdit_preDNSeDNS)
        self.lineEdit_alterDNSalterDNS.mouseReleaseEvent = lambda event: self.SignalShowKeyBoard.emit(self.lineEdit_alterDNSalterDNS)
        self.pushButton_exit.clicked.connect(self.__CloseScreen)
        self.pushButton_saveAndRestartaveAndRestart.clicked.connect(self.__SaveAndRestart)
        self.lineEdit_ip.textChanged.connect(lambda:self.__CheckIPrule(self.lineEdit_ip.text(), self.label_iconCheckIP))
        self.lineEdit_gateWay.textChanged.connect(lambda:self.__CheckIPrule(self.lineEdit_gateWay.text(), self.label_iconCheckGateway))
        self.lineEdit_subnetMask.textChanged.connect(lambda:self.__CheckIPrule(self.lineEdit_subnetMask.text(), self.label_iconCheckSubnetMaskubnetMask))
        self.lineEdit_preDNSeDNS.textChanged.connect(lambda:self.__CheckIPrule(self.lineEdit_preDNSeDNS.text(), self.label_iconCheckDNS1))
        self.lineEdit_alterDNSalterDNS.textChanged.connect(lambda:self.__CheckIPrule(self.lineEdit_alterDNSalterDNS.text(), self.label_iconCheckDNS2))        

    def __SaveAndRestart(self):
        try:
            dataToSaveFile = ""
            dataToSaveFile += "auto eth0\nallow-hotplug eth0\niface eth0 inet static\n"
            dataToSaveFile += "address " + self.lineEdit_ip.text() + "\n"
            dataToSaveFile += "netmask " + self.lineEdit_subnetMask.text() + "\n"
            dataToSaveFile += "gateway" + self.lineEdit_gateWay.text() + "\n"
            dataToSaveFile += "dns-nameServers " + self.lineEdit_preDNSeDNS.text() + " "+ self.lineEdit_alterDNSalterDNS.text() + "\n"
            interfaceFile = open("/etc/network/interfaces", "w")
            interfaceFile.write(dataToSaveFile)
        except:
            pass

    def __CheckIPrule(self, ipText, labelForShowIcon):
        try:
            ipArr = ipText.split(".")
            if(len(ipArr) == 4):
                for number in ipArr:
                    if(not self.__CheckNumberRule(number)):
                        labelForShowIcon.setPixmap(self.checkFailPixmap)
                        return
                labelForShowIcon.setPixmap(self.checkOKpixmap)
                
            else:
                labelForShowIcon.setPixmap(self.checkFailPixmap)
        except:
            labelForShowIcon.setPixmap(self.checkFailPixmap)

        
    def __CheckNumberRule(self, numberText):
        try:
            intNumber = int(numberText)
            if((intNumber >= 0) & (intNumber <= 255)):
                return True
            else:
                return False
        except:
            return False

    def __CloseScreen(self):
        self.frameContain.hide()
        self.deleteLater()
        self.frameContain.parent().hide()
        self.frameContain.parent().deleteLater()

    
    