from PyQt5                      import QtCore, QtGui, QtWidgets
from PyQt5                      import QtCore, QtGui, QtWidgets
from PyQt5.QtGui                import QIcon, QPixmap
from PyQt5.QtCore               import pyqtSlot, pyqtSignal,QTimer, QDateTime, Qt, QObject, QPointF, QPropertyAnimation, pyqtProperty
from SettingScreen.WriteCardUi  import Ui_Frame


class WriteCard(Ui_Frame, QObject):
    
    SignalWriteToCard = pyqtSignal(str, object)

    def __init__(self, frameContain):
        Ui_Frame.__init__(self)
        QObject.__init__(self)
        self.frameContainCurrentStep = frameContain
        self.setupUi(frameContain)
        self.label.setPixmap(QtGui.QPixmap("icon/putRFcardIcon.png"))
        self.strNumber = ""
        self.pushButton.clicked.connect(self.WriteToCard)

    def SetNumberToWriteCard(self, strNumber):
        self.strNumber = strNumber

    def WriteToCard(self):
        self.PutCardToDeviceNotify()
        self.SignalWriteToCard.emit(self.strNumber, self.WritedNotify)

    def PutCardToDeviceNotify(self):
        self.label_showNotify.setStyleSheet('color: rgb(200, 0, 0);font: 75 bold 16pt "Ubuntu";')
        self.label_showNotify.setText("Đặt thẻ lên thiết bị")

    def WritedNotify(self):
        self.label_showNotify.setStyleSheet('color: rgb(0, 200, 0);font: 75 bold 16pt "Ubuntu";')
        self.label_showNotify.setText("Ghi thẻ thành công")

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
        self.PutCardToDeviceNotify()