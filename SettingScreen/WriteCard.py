from PyQt5                      import QtCore, QtGui, QtWidgets
from PyQt5                      import QtCore, QtGui, QtWidgets
from PyQt5.QtGui                import QIcon, QPixmap
from PyQt5.QtCore               import pyqtSlot, pyqtSignal,QTimer, QDateTime, Qt, QObject, QPointF, QPropertyAnimation, pyqtProperty
from SettingScreen.WriteCardUi  import Ui_Frame
from GlobalClass.GlobalClass    import DefineWriteCardNotify

class WriteCard(Ui_Frame, QObject):
    
    SignalWriteToCard = pyqtSignal(str, object)
    SignalStopWriteCard = pyqtSignal()
    
    def __init__(self, frameContain):
        Ui_Frame.__init__(self)
        QObject.__init__(self)
        self.frameContainCurrentStep = frameContain
        self.setupUi(frameContain)
        self.label.setPixmap(QtGui.QPixmap("icon/putRFcardIcon.png"))
        self.strNumber = ""
        self.pushButton.clicked.connect(self.WriteToCard)
        self.studentForAdd = object
        self.numberCardWritten = 0

    def StudentChose(self, student):
        self.label_forShowNameStudent.setText(student.HoVaTen)
        self.studentForAdd = student
        self.strNumber = student.SoCMTND

    def SetNumberToWriteCard(self, strNumber):
        self.strNumber = strNumber


    def GetNamberCardWriten(self):
        return self.numberCardWritten

    def StopWriteCard(self):
        self.SignalStopWriteCard.emit()

    def ClearTempData(self):
        self.numberCardWritten = 0

    def WriteToCard(self):
        self.PutCardToDeviceNotify()
        self.SignalWriteToCard.emit(self.strNumber, self.WritedNotify)

    def PutCardToDeviceNotify(self):
        self.label_showNotify.setStyleSheet('color: rgb(200, 0, 0);font: 75 bold 16pt "Ubuntu";')
        self.label_showNotify.setText("ĐẶT THẺ LÊN THIẾT BỊ")

    def WritedNotify(self, flag):
        if(flag == DefineWriteCardNotify().waitCard):
            self.label_showNotify.setStyleSheet('color: rgb(200, 0, 0);font: 75 bold 16pt "Ubuntu";')
            self.label_showNotify.setText("ĐẶT THẺ LÊN THIẾT BỊ")
        if(flag == DefineWriteCardNotify().written):
            self.label_showNotify.setStyleSheet('color: rgb(0, 200, 0);font: 75 bold 16pt "Ubuntu";')
            self.label_showNotify.setText("GHI THẺ THÀNH CÔNG")
            self.numberCardWritten += 1

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