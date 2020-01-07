from PyQt5                      import QtCore, QtGui, QtWidgets
from PyQt5                      import QtCore, QtGui, QtWidgets
from PyQt5.QtGui                import QIcon, QPixmap
from PyQt5.QtCore               import pyqtSlot, pyqtSignal,QTimer, QDateTime, Qt, QObject, QPointF, QPropertyAnimation, pyqtProperty
from SettingScreen.AddFGPUI     import Ui_Frame_AddFGP
from FingerPrintSensor.FingerPrint            import Fingerprint

class AddFGP(Ui_Frame_AddFGP, QObject):
    SignalAddedFGP = pyqtSignal()
    def __init__(self, frameContain):
        Ui_Frame_AddFGP.__init__(self)
        QObject.__init__(self)
        self.setupUi(frameContain)
        self.label_forShowIconAddFingerPrint.setPixmap(QtGui.QPixmap("icon/iconFGPtouch.png"))
        self.frameContainCurrentStep = frameContain
        self.frameContainCurrentStep.show()
        
        self.FGPsensorObj = Fingerprint()
        self.FGPsensorObj.SignalNewFGPadded.connect(self.FGPsavedInSensor)
        self.FGPsensorObj.SignalHandPushed.connect(self.HandPushed)

        self.studentForAdd = object
        self.timerHoldHandAnounment = QTimer(self)
        self.timerHoldHandAnounment.timeout.connect(self.HoldHandAnounment)

        self.feature = False
        self.pos = False

    def ClearAddAdded(self):
        self.feature = False
        self.pos = False
     
    def FGPsavedInSensor(self, pos, feature):
        
        self.pos = pos
        self.feature = feature
        self.SignalAddedFGP.emit()
        self.timerHoldHandAnounment.stop()
        self.FGPsensorObj.TatThemVanTay()
        self.label_forShowAnoument.setStyleSheet('color: rgb(0, 170, 0);\nfont: 75 bold 14pt "Ubuntu";')
        self.label_forShowAnoument.setText("ĐÃ NHẬN ĐƯỢC VÂN TAY")


    def GetFGPsavePosAndFeature(self):
        infoDict = {
            "FGPsavePos":self.pos,
            "FGPfeature":self.feature
        }
        return infoDict

    def HandPushed(self):
        self.label_forShowAnoument.setText("GIỮ TAY TRÊN CẢM BIẾN")
        if(self.timerHoldHandAnounment.isActive):
            self.timerHoldHandAnounment.start(1000)


    def HoldHandAnounment(self):
        self.label_forShowAnoument.setText("ĐẶT TAY LÊN CẢM BIẾN")
        self.timerHoldHandAnounment.stop()
        
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

    def StartReciptFGP(self):
        self.FGPsensorObj.BatThemVanTay()

    def StopReciptFGP(self):
        self.FGPsensorObj.TatThemVanTay()