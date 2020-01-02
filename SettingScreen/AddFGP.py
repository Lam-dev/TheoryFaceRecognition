from PyQt5                      import QtCore, QtGui, QtWidgets
from PyQt5                      import QtCore, QtGui, QtWidgets
from PyQt5.QtGui                import QIcon, QPixmap
from PyQt5.QtCore               import pyqtSlot, pyqtSignal,QTimer, QDateTime, Qt, QObject, QPointF, QPropertyAnimation, pyqtProperty
from SettingScreen.AddFGPUI     import Ui_Frame_AddFGP

class AddFGP(Ui_Frame_AddFGP, QObject):
    def __init__(self, frameContain):
        Ui_Frame_AddFGP.__init__(self)
        QObject.__init__(self)
        self.setupUi(frameContain)
        self.label_forShowIconAddFingerPrint.setPixmap(QtGui.QPixmap("icon/iconFGPtouch.png"))
        self.frameContainCurrentStep = frameContain
        self.frameContainCurrentStep.show()
    
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
    
       