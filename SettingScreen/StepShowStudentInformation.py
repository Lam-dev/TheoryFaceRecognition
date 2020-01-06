from PyQt5                  import QtCore, QtGui, QtWidgets
from PyQt5                  import QtCore, QtGui, QtWidgets
from PyQt5.QtGui            import QIcon, QPixmap
from PIL                    import Image, ImageQt
from PyQt5.QtCore           import pyqtSlot, pyqtSignal,QTimer, QDateTime, Qt, QObject, QPointF, QPropertyAnimation, pyqtProperty
import                      io

from SettingScreen.StepShowStudentInformationUI                  import Ui_Frame

class StepShowStudentInformation(QObject, Ui_Frame):
    def __init__(self, frameContain):
        Ui_Frame.__init__(self)
        QObject.__init__(self)
        self.frameContainCurrentStep = frameContain
        self.setupUi(self.frameContainCurrentStep)
        self.label_faceIcon.setPixmap(QtGui.QPixmap("icon/iconFace30x30.png"))
        self.label_FGPicon.setPixmap(QtGui.QPixmap("icon/iconFGP30x30.png"))
    
    def ShowStudentInformation(self, student):
        image = Image.open(io.BytesIO(student.AnhDangKy))
        qim = ImageQt.ImageQt(image)
        pix = QtGui.QPixmap.fromImage(qim)
        resizePixmap = pix.scaled(150, 200, QtCore.Qt.KeepAspectRatio)
        # self.SetGeometryForLabelShowRegisImage(resizePixmap.width(), resizePixmap.height())
        self.label_forShowStudentImage.setPixmap(resizePixmap)
        self.label_nameOfStudent.setText(student.HoVaTen.upper())
        self.label_forShowIDnumber.setText(student.SoCMTND)
        # self.label_forShowDateOfBird.setText(student.SoCMTND)
        if(len(student.NhanDienKhuonMatThem) == 0):
            self.label_forShowNumberFaceAdded.setStyleSheet("color:rgb(200, 0, 0)")
            self.label_forShowNumberFaceAdded.setText("Chưa thêm")
        else:
            self.label_forShowNumberFaceAdded.setStyleSheet("color:rgb(30, 30, 30)")
            self.label_forShowNumberFaceAdded.setText("Đã thêm")
        



    def ShowStepStudentInformationAnim(self, frameOfPreStep):

        self.preStepGoToLeftAnim = QPropertyAnimation(frameOfPreStep, b"geometry")
        self.preStepGoToLeftAnim.setDuration(300)
        self.preStepGoToLeftAnim.setStartValue(QtCore.QRect(0 , frameOfPreStep.y() , frameOfPreStep.width(), frameOfPreStep.height()))
        self.preStepGoToLeftAnim.setEndValue(QtCore.QRect(0-frameOfPreStep.width() , frameOfPreStep.y(), frameOfPreStep.width(), frameOfPreStep.height()))
        
        self.currentStepToLeftAnim = QPropertyAnimation(self.frameContainCurrentStep, b"geometry")
        self.currentStepToLeftAnim.setDuration(300)
        self.currentStepToLeftAnim.setStartValue(QtCore.QRect(frameOfPreStep.width() , self.frameContainCurrentStep.y() , self.frameContainCurrentStep.width(), self.frameContainCurrentStep.height()))
        self.currentStepToLeftAnim.setEndValue(QtCore.QRect(0 , self.frameContainCurrentStep.y(), self.frameContainCurrentStep.width(), self.frameContainCurrentStep.height()))
        self.frameContainCurrentStep.show()

        self.preStepGoToLeftAnim.start()
        self.currentStepToLeftAnim.start()

    