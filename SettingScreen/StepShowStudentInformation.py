from PyQt5                  import QtCore, QtGui, QtWidgets
from PyQt5                  import QtCore, QtGui, QtWidgets
from PyQt5.QtGui            import QIcon, QPixmap
from PIL                    import Image, ImageQt
from PyQt5.QtCore           import pyqtSlot, pyqtSignal,QTimer, QDateTime, Qt, QObject, QPointF, QPropertyAnimation, pyqtProperty
import                      io
from DatabaseAccess.DatabaseAccess   import IDvaVanTayRepository

from SettingScreen.StepShowStudentInformationUI                  import Ui_Frame

class StepShowStudentInformation(QObject, Ui_Frame):

    SignalRequestDeleteFaceAdded = pyqtSignal()
    SignalRequestDeleteFGPadded = pyqtSignal()

    def __init__(self, frameContain):
        Ui_Frame.__init__(self)
        QObject.__init__(self)
        self.frameContainCurrentStep = frameContain
        self.setupUi(self.frameContainCurrentStep)
        self.label_faceIcon.setPixmap(QtGui.QPixmap("icon/iconFace30x30.png"))
        self.label_FGPicon.setPixmap(QtGui.QPixmap("icon/iconFGP30x30.png"))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/iconDelete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_deleteFaceAdded.setIcon(icon)
        self.pushButton_deleteFaceAdded.setIconSize(QtCore.QSize(38, 38))

        self.pushButton_deleteFGPadded.setText("")
        self.pushButton_deleteFGPadded.setIcon(icon)
        self.pushButton_deleteFGPadded.setIconSize(QtCore.QSize(38, 38))

        self.pushButton_deleteFaceAdded.clicked.connect(self.SignalRequestDeleteFaceAdded.emit)
        self.pushButton_deleteFGPadded.clicked.connect(self.SignalRequestDeleteFGPadded.emit)
        
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
        if(student.NhanDienKhuonMatThem == None):
            self.label_forShowNumberFaceAdded.setStyleSheet("color:rgb(200, 0, 0)")
            self.label_forShowNumberFaceAdded.setText("Chưa thêm")
        else:
            self.label_forShowNumberFaceAdded.setStyleSheet("color:rgb(30, 30, 30)")
            self.label_forShowNumberFaceAdded.setText("Đã thêm")
        khoIDvaVanTay = IDvaVanTayRepository()
        lstIDvaVanTay = khoIDvaVanTay.layDanhSach(" IDThiSinh = %s "%(student.ID))
        if(len(lstIDvaVanTay) == 0):
            self.label_forShowNumberFGPadded.setStyleSheet("color:rgb(200, 0, 0)")
            self.label_forShowNumberFGPadded.setText("Chưa thêm")
        else:
            self.label_forShowNumberFGPadded.setStyleSheet("color:rgb(30, 30, 30)")
            self.label_forShowNumberFGPadded.setText("Đã thêm")
            
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

    