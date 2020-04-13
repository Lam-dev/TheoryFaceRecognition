from AddFGP.AddFGPui     import Ui_Frame_ContainAddFGPscreen
from PyQt5          import QtCore, QtGui
from PyQt5.QtCore   import pyqtSlot, pyqtSignal,QTimer, QDateTime, Qt, QObject, QPointF, QPropertyAnimation, pyqtProperty, QSize
from PyQt5          import QtWidgets
import json
from FingerPrintSensor.FingerPrint   import Fingerprint

class AddFGPscreen(QObject, Ui_Frame_ContainAddFGPscreen):
    SignalSendImageToServer = pyqtSignal(str, str)
    SignalSendFGPGetToServer = pyqtSignal(str, str)
    def __init__(self, frameContain):
        QObject.__init__(self)
        Ui_Frame_ContainAddFGPscreen.__init__(self)
        self.frameContainCurrentStep = frameContain
        self.frameContainCurrentStep.show()
        self.setupUi(frameContain)
        
        

        self.__pixmapUtTraiTrang = QtGui.QPixmap("icon/finger/utTraiTrang.png")
        self.__pixmapNhanTraiTrang = QtGui.QPixmap("icon/finger/nhanTraiTrang.png")
        self.__pixmapGiuaTraiTrang = QtGui.QPixmap("icon/finger/giuaTraiTrang.png")
        self.__pixmapTroTraiTrang = QtGui.QPixmap("icon/finger/troTraiTrang.png")
        self.__pixmapCaiTraiTrang = QtGui.QPixmap("icon/finger/caiTraiTrang.png")
        self.__pixmapTroPhaiTrang = QtGui.QPixmap("icon/fingerRight/troPhaiTrang.png")
        self.__pixmapGiuaPhaiTrang = QtGui.QPixmap("icon/fingerRight/giuaPhaiTrang.png")
        self.__pixmapCaiPhaiTrang = QtGui.QPixmap("icon/fingerRight/caiPhaiTrang.png")
        self.__pixmapUtPhaiTrang = QtGui.QPixmap("icon/fingerRight/utPhaiTrang.png")
        self.__pixmapNhanPhaiTrang = QtGui.QPixmap("icon/fingerRight/nhanPhaiTrang.png")

        self.__pixmapUtTraiXanh = QtGui.QPixmap("icon/finger/utTraiXanh.png")
        self.__pixmapNhanTraiXanh = QtGui.QPixmap("icon/finger/nhanTraiXanh.png")
        self.__pixmapGiuaTraiXanh = QtGui.QPixmap("icon/finger/giuaTraiXanh.png")
        self.__pixmapTroTraiXanh = QtGui.QPixmap("icon/finger/troTraiXanh.png")
        self.__pixmapCaiTraiXanh = QtGui.QPixmap("icon/finger/caiTraiXanh.png")
        self.__pixmapTroPhaiXanh = QtGui.QPixmap("icon/fingerRight/troPhaiXanh.png")
        self.__pixmapGiuaPhaiXanh = QtGui.QPixmap("icon/fingerRight/giuaPhaiXanh.png")
        self.__pixmapCaiPhaiXanh = QtGui.QPixmap("icon/fingerRight/caiPhaiXanh.png")
        self.__pixmapUtPhaiXanh = QtGui.QPixmap("icon/fingerRight/utPhaiXanh.png")
        self.__pixmapNhanPhaiXanh = QtGui.QPixmap("icon/fingerRight/nhanPhaiXanh.png")

        self.label_utTrai.setPixmap(self.__pixmapUtTraiTrang)
        self.label_nhanTrai.setPixmap(self.__pixmapNhanTraiTrang)
        self.label_giuaTrai.setPixmap(self.__pixmapGiuaTraiTrang)
        self.label_troTrai.setPixmap(self.__pixmapTroTraiTrang)
        self.label_caiTrai.setPixmap(self.__pixmapCaiTraiTrang)
        self.label_troPhai.setPixmap(self.__pixmapTroPhaiTrang)
        self.label_giuaPhai.setPixmap(self.__pixmapGiuaPhaiTrang)
        self.label_caiPhai.setPixmap(self.__pixmapCaiPhaiTrang)
        self.label_utPhai.setPixmap(self.__pixmapUtPhaiTrang)
        self.label_nhanPhai.setPixmap(self.__pixmapNhanPhaiTrang)
        
        self.lstFingerNeedAdd = []
        self.timerGetFGP = QTimer(self)
        self.timerGetFGP.timeout.connect(self.GetFGP)


        self.fingerprintObj = Fingerprint()
        self.fingerprintObj.SignalFGPputOnIsTheSame.connect(self.ShowFGPisTheSameWithPre)
        self.fingerprintObj.SignalFGPget.connect(self.FGPget)

        self.imageObjNeedFlipFlop = False

        self.timerFlipFlop = QTimer(self)
        self.timerFlipFlop.timeout.connect(self.FlipFlopImage)



        self.fingerNeedingAddIsWhite = False
        self.__nameFingerGetting = ""
        self.__strNameFingerNeedAdd = ""
        self.__fingerNeedAddWhite = ""
        self.__fingerNeedAddGreen = ""
        self.__FGPgetPercent = 0
        self.__lstFGPofAfinger = []
        self.__lstFGPofAfingerStr = ""
        self.__nameOfFingerAdding = ""
        
    def FGPget(self, FGPfeature):
        # self.__FGPgetPercent += 25
        # self.label_forShowFGPpercent.setText(str(self.__FGPgetPercent) + "%")
        # self.__lstFGPofAfinger.append(FGPfeature)
        # if(self.__FGPgetPercent == 100):
        #     self.__FGPgetPercent = 0
        #     self.label_forShowFGPpercent.setText(str(self.__FGPgetPercent) + "%")
        #     self.StopAll()
        #     __lstFGPofAfingerStr = ";".join(self.__lstFGPofAfinger)
        #     self.SignalSendFGPGetToServer.emit(__lstFGPofAfingerStr, self.__nameOfFingerAdding)
        #     self.GetFGP()

        
        self.__FGPgetPercent += 1
        self.label_forShowFGPpercent.setText(str(self.__FGPgetPercent))
        self.__lstFGPofAfinger.append(FGPfeature)
        if(self.__FGPgetPercent == 3):
            self.__FGPgetPercent = 0
            self.label_forShowFGPpercent.setText(str(self.__FGPgetPercent))
            self.StopAll()
            __lstFGPofAfingerStr = ";".join(self.__lstFGPofAfinger)
            self.SignalSendFGPGetToServer.emit(__lstFGPofAfingerStr, self.__nameOfFingerAdding)
            self.__lstFGPofAfinger = []
            self.GetFGP()
        

    def ShowFGPisTheSameWithPre(self):
        pass

    def FGPdownloaded(self, imageName):
        self.SignalSendImageToServer.emit(imageName, self.__strNameFingerNeedAdd)
        self.imageObjNeedFlipFlop.setPixmap(self.__fingerNeedAddGreen)
        self.GetFGP()

    def ListFingerNeedAdd(self, strData):
        dataObj = json.loads(strData)
        listKey = list(dataObj.keys())
        self.ClearAllFingerNeedAddPre()
        self.lstFingerNeedAdd.clear()

        for key in listKey:
            if(dataObj[key]):
                self.lstFingerNeedAdd.append(key)
                self.ShowFingerNeedAdd(key)

    def FlipFlopImage(self):
        if(self.fingerNeedingAddIsWhite):
            self.imageObjNeedFlipFlop.setPixmap(self.__fingerNeedAddGreen)
            self.fingerNeedingAddIsWhite = False
        else:
            self.imageObjNeedFlipFlop.setPixmap(self.__fingerNeedAddWhite)
            self.fingerNeedingAddIsWhite = True

    def StopAll(self):
        self.fingerprintObj.StopGetFGP()
        self.timerFlipFlop.stop()

    def GetFGP(self):
        self.fingerprintObj.ClearFGPfeatureSaveOnSensor()
        if(self.lstFingerNeedAdd.__len__() == 0):
            self.StopAll()
            return
        self.__nameOfFingerAdding = self.lstFingerNeedAdd.pop()
        self.ShowFingerPutNotify(self.__nameOfFingerAdding)
        self.fingerprintObj.StartGetFGP()
        self.timerFlipFlop.start(500)
    
    def ClearAllFingerNeedAddPre(self):
        self.label_utTrai.setPixmap(self.__pixmapUtTraiTrang)
        self.label_nhanTrai.setPixmap(self.__pixmapNhanTraiTrang)
        self.label_giuaTrai.setPixmap(self.__pixmapGiuaTraiTrang)
        self.label_troTrai.setPixmap(self.__pixmapTroTraiTrang)
        self.label_caiTrai.setPixmap(self.__pixmapCaiTraiTrang)
        self.label_caiPhai.setPixmap(self.__pixmapCaiPhaiTrang)
        self.label_troPhai.setPixmap(self.__pixmapTroPhaiTrang)
        self.label_giuaPhai.setPixmap(self.__pixmapGiuaPhaiTrang)
        self.label_nhanPhai.setPixmap(self.__pixmapNhanPhaiTrang)
        self.label_utPhai.setPixmap(self.__pixmapUtPhaiTrang)

    def ShowFingerNeedAdd(self, fingerName):
        if(fingerName == "utTrai"):
            self.label_utTrai.setPixmap(self.__pixmapUtTraiXanh)
        elif(fingerName == "nhanTrai"):
            self.label_nhanTrai.setPixmap(self.__pixmapNhanTraiXanh)
        elif(fingerName == "giuaTrai"):
            self.label_giuaTrai.setPixmap(self.__pixmapGiuaTraiXanh)
        elif(fingerName == "troTrai"):
            self.label_troTrai.setPixmap(self.__pixmapTroTraiXanh)
        elif(fingerName == "caiTrai"):
            self.label_caiTrai.setPixmap(self.__pixmapCaiTraiXanh)
        elif(fingerName == "caiPhai"):
            self.label_caiPhai.setPixmap(self.__pixmapCaiPhaiXanh)
        elif(fingerName == "troPhai"):
            self.label_troPhai.setPixmap(self.__pixmapTroPhaiXanh)
        elif(fingerName == "giuaPhai"):
            self.label_giuaPhai.setPixmap(self.__pixmapGiuaPhaiXanh)
        elif(fingerName == "nhanPhai"):
            self.label_nhanPhai.setPixmap(self.__pixmapNhanPhaiXanh)
        elif(fingerName == "utPhai"):
            self.label_utPhai.setPixmap(self.__pixmapUtPhaiXanh)

    def ShowFingerPutNotify(self, fingerStr):
        if(fingerStr == "utTrai"):
            
            self.label_forShowNotify.setText("ĐẶT NGÓN ÚT TRÁI LÊN CẢM BIẾN")
            self.imageObjNeedFlipFlop = self.label_utTrai
            self.__fingerNeedAddWhite = self.__pixmapUtTraiTrang
            self.__fingerNeedAddGreen = self.__pixmapUtTraiXanh
            self.__strNameFingerNeedAdd = fingerStr

        elif(fingerStr == "nhanTrai"):
            self.label_forShowNotify.setText("ĐẶT NGÓN NHẪN TRÁI LÊN CẢM BIẾN")
            self.imageObjNeedFlipFlop = self.label_nhanTrai
            self.__fingerNeedAddWhite = self.__pixmapNhanTraiTrang
            self.__fingerNeedAddGreen = self.__pixmapNhanTraiXanh
            self.__strNameFingerNeedAdd = fingerStr

        elif(fingerStr == "giuaTrai"):
            self.label_forShowNotify.setText("ĐẶT NGÓN GIỮA TRÁI LÊN CẢM BIẾN")
            self.imageObjNeedFlipFlop = self.label_giuaTrai
            self.__fingerNeedAddWhite = self.__pixmapGiuaTraiTrang
            self.__fingerNeedAddGreen = self.__pixmapGiuaTraiXanh
            self.__strNameFingerNeedAdd = fingerStr      

        elif(fingerStr == "troTrai"):
            self.label_forShowNotify.setText("ĐẶT NGÓN TRỎ TRÁI LÊN CẢM BIẾN")
            self.imageObjNeedFlipFlop = self.label_troTrai
            self.__fingerNeedAddWhite = self.__pixmapTroTraiTrang
            self.__fingerNeedAddGreen = self.__pixmapTroTraiXanh
            self.__strNameFingerNeedAdd = fingerStr        

        elif(fingerStr == "caiTrai"):
            self.label_forShowNotify.setText("ĐẶT NGÓN CÁI TRÁI LÊN CẢM BIẾN")
            self.imageObjNeedFlipFlop = self.label_caiTrai
            self.__fingerNeedAddWhite = self.__pixmapCaiTraiTrang
            self.__fingerNeedAddGreen = self.__pixmapCaiTraiXanh
            self.__strNameFingerNeedAdd = fingerStr   

        elif(fingerStr == "caiPhai"):
            self.label_forShowNotify.setText("ĐẶT NGÓN CÁI PHẢI LÊN CẢM BIẾN")
            self.imageObjNeedFlipFlop = self.label_caiPhai
            self.__fingerNeedAddWhite = self.__pixmapCaiPhaiTrang
            self.__fingerNeedAddGreen = self.__pixmapCaiPhaiXanh
            self.__strNameFingerNeedAdd = fingerStr    

        elif(fingerStr == "troPhai"):
            self.label_forShowNotify.setText("ĐẶT NGÓN TRỎ PHẢI LÊN CẢM BIẾN")
            self.imageObjNeedFlipFlop = self.label_troPhai
            self.__fingerNeedAddWhite = self.__pixmapTroPhaiTrang
            self.__fingerNeedAddGreen = self.__pixmapTroPhaiXanh
            self.__strNameFingerNeedAdd = fingerStr

        elif(fingerStr == "giuaPhai"):
            self.label_forShowNotify.setText("ĐẶT NGÓN GIỮA PHẢI LÊN CẢM BIẾN")
            self.imageObjNeedFlipFlop = self.label_giuaPhai
            self.__fingerNeedAddWhite = self.__pixmapGiuaPhaiTrang
            self.__fingerNeedAddGreen = self.__pixmapGiuaPhaiXanh
            self.__strNameFingerNeedAdd = fingerStr

        elif(fingerStr == "nhanPhai"):
            self.label_forShowNotify.setText("ĐẶT NGÓN NHẪN PHẢI LÊN CẢM BIẾN")
            self.imageObjNeedFlipFlop = self.label_nhanPhai
            self.__fingerNeedAddWhite = self.__pixmapNhanPhaiTrang
            self.__fingerNeedAddGreen = self.__pixmapNhanPhaiXanh
            self.__strNameFingerNeedAdd = fingerStr
            
        elif(fingerStr == "utPhai"):
            self.label_forShowNotify.setText("ĐẶT NGÓN ÚT PHẢI LÊN CẢM BIẾN")
            self.imageObjNeedFlipFlop = self.label_utPhai
            self.__fingerNeedAddWhite = self.__pixmapUtPhaiTrang
            self.__fingerNeedAddGreen = self.__pixmapUtPhaiXanh
            self.__strNameFingerNeedAdd = fingerStr
        
    def ShowStepStudentInformationAnim(self, frameOfPreStep):
        self.preStepGoToLeftAnim = QPropertyAnimation(frameOfPreStep, b"geometry")
        self.preStepGoToLeftAnim.setDuration(300)
        self.preStepGoToLeftAnim.setStartValue(QtCore.QRect(0 , frameOfPreStep.y() , frameOfPreStep.width(), frameOfPreStep.height()))
        self.preStepGoToLeftAnim.setEndValue(QtCore.QRect(0-frameOfPreStep.width() , frameOfPreStep.y(), frameOfPreStep.width(), frameOfPreStep.height()))
        
        self.currentStepToLeftAnim = QPropertyAnimation(self.frameContainCurrentStep, b"geometry")
        self.currentStepToLeftAnim.setDuration(300)
        self.currentStepToLeftAnim.setStartValue(QtCore.QRect(frameOfPreStep.width() , self.frameContainCurrentStep.y() , self.frameContainCurrentStep.width(), self.frameContainCurrentStep.height()))
        self.currentStepToLeftAnim.setEndValue(QtCore.QRect(0 , self.frameContainCurrentStep.y(), self.frameContainCurrentStep.width(), self.frameContainCurrentStep.height()))
        
        self.preStepGoToLeftAnim.start()
        self.currentStepToLeftAnim.start()