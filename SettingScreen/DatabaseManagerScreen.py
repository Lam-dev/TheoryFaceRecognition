from PyQt5                  import QtCore, QtGui, QtWidgets
from PyQt5                  import QtCore, QtGui, QtWidgets
from PyQt5.QtGui            import QIcon, QPixmap
from PyQt5.QtCore           import pyqtSlot, pyqtSignal,QTimer, QDateTime, Qt, QObject, QPointF, QPropertyAnimation, pyqtProperty
from SettingScreen.DatabaseManagerScreenUI    import Ui_Frame_containDatabaseScreen
from DatabaseAccess.DatabaseAccess            import *  
from SettingScreen.StepShowStudentInformation import StepShowStudentInformation
from SettingScreen.AddFace                    import AddFaceScreen
from SettingScreen.AddFGP                     import AddFGP
from SettingScreen.AddDataResult              import AddDataResults


class DatabaseManagerScreen(Ui_Frame_containDatabaseScreen, QObject):
    SignalCloseDatabaseScreen = pyqtSignal()
    SignalAddFaceEncodeAndFGP = pyqtSignal(dict, dict)

    def __init__(self, frameContain):
        Ui_Frame_containDatabaseScreen.__init__(self)
        QObject.__init__(self)
        frameContain.setGeometry(0, 0, 800, 480)
        self.frameContainDatabaseScreen = frameContain
        self.setupUi(frameContain)
        self.pushButton_closeDatabaseScreen.clicked.connect(self.SignalCloseDatabaseScreen.emit)
        self.pushButton_nextStep.clicked.connect(self.NextStep)
        self.pushButton_nextStep.hide()
        self.comboBox_showListCourser.currentIndexChanged.connect(self.ChooserCourse)
        self.lstStudent = []
        self.lstKhoaThi = []
        self.entry = QtGui.QStandardItemModel()
        self.GetAndShowListCourse()
        self.listWidget_showListStudent.currentRowChanged.connect(self.ChooseStudent)
        self.studentInfoObj = StepShowStudentInformation(self.frame)

        self.frameContainAddFGP = QtWidgets.QFrame(self.frame_containAddInformationStep)
        self.frameContainAddFGP.setGeometry(QtCore.QRect(self.frame_containAddInformationStep.width(), 0, 0, 0))
        self.addFGPobj = AddFGP(self.frameContainAddFGP)

        self.frameContainAddFace = QtWidgets.QFrame(self.frame_containAddInformationStep)
        self.frameContainAddFace.setGeometry(QtCore.QRect(self.frame_containAddInformationStep.width(), 0, 0, 0))
        self.addFaceObj = AddFaceScreen(self.frameContainAddFace)
        self.addFaceObj.SignalGrappedImage.connect(self.GrappedFaceImage)
        self.choseStudent = object


        self.faceAdded = object
        self.FGPadded = object

        self.currentStep = 1

    def AddFGPtoDatabase(self, pos, feature):
        idVaVanTay = IDvaVanTayRepository()
        idVaVanTay.IDThiSinh = self.choseStudent.ID
        idVaVanTay.ViTriVanTay = pos
        featureStrArr = [str(elem) for elem in feature]
        featureStr = ",".join(featureStrArr)
        idVaVanTay.DacTrungVanTay = featureStr
        khoIDvaVanTay = IDvaVanTayRepository()
        khoIDvaVanTay.ghiDuLieu(idVaVanTay)


    def ShowAddDataDialog(self):
        self.dialogShadow = QtWidgets.QFrame(self.frameContainDatabaseScreen )
        self.dialogShadow.setGeometry(QtCore.QRect(0, 0, 800, 480))
        self.dialogShadow.setStyleSheet("background-color: rgba(0, 0, 0, 100);")
        self.frameContainDialog = QtWidgets.QFrame(self.dialogShadow)
        self.dialogObj = AddDataResults(self.frameContainDialog)
        self.dialogObj.ShowDialog(success=True, addFace = True, addFGP=True)
        self.dialogObj.SignalCloseResultDialog.connect(self.HideResultDialog)
        self.dialogShadow.show()
        self.dialogShadow.raise_()

    def HideResultDialog(self):
        self.dialogShadow.hide()
        self.frameContainDialog.deleteLater()
        self.dialogObj.deleteLater()
        self.dialogShadow.deleteLater()
        self.currentStep = 1
        self.studentInfoObj.ShowStepStudentInformationAnim(self.frameContainAddFace)

    def GrappedFaceImage(self, iamgeDict):
        
        self.pushButton_nextStep.setText("Hoàn tất")

    def GrappedFGP(self, FGPdict):
        self.FGPadded = FGPdict

    def NextStep(self):
        if(self.currentStep == 1):
            self.addFGPobj.ShowStepStudentInformationAnim(self.frame)
            self.currentStep = 2
            self.Step2HightLight()
            self.addFGPobj.StartReciptFGP()
            self.pushButton_nextStep.setText("Thêm khuôn mặt")

        elif(self.currentStep == 2):
            self.addFaceObj.ShowStepStudentInformationAnim(self.frameContainAddFGP)
            self.currentStep = 3
            self.Step3HightLight()
            self.FGPsensorObj.TatThemVanTay()
            self.pushButton_nextStep.setText("Hoàn tất")
            
        else:
            faceEncodeDict = self.addFaceObj.GetFaceEncodingImageGrapped()
            FGPdict = self.addFGPobj.GetFGPsavePosAndFeature()
            self.SignalAddFaceEncodeAndFGP.emit(faceEncodeDict, FGPdict)
            return
            # self.addFaceObj.StopCamera()
            # self.studentInfoObj.ShowStepStudentInformationAnim(self.frameContainAddFace)
            # self.currentStep = 1
            # self.Step1HightLight()

    def Step1HightLight(self):
        self.label_step1HighLight.setStyleSheet("background-color: rgb(0, 170, 127);border-radius:7px")
        self.label_step2HighLight.setStyleSheet("border-radius:7px;border-color:rgb(0, 170, 255);border-width:2px")
        self.label_step3HighLight.setStyleSheet("border-radius:7px;border-color:rgb(0, 170, 255);border-width:2px")

    def Step2HightLight(self):
        self.label_step2HighLight.setStyleSheet("background-color: rgb(0, 170, 127);border-radius:7px")
        self.label_step1HighLight.setStyleSheet("border-radius:7px;border-color:rgb(0, 170, 255);border-width:2px")
        self.label_step3HighLight.setStyleSheet("border-radius:7px;border-color:rgb(0, 170, 255);border-width:2px")

    def Step3HightLight(self):
        self.label_step3HighLight.setStyleSheet("background-color: rgb(0, 170, 127);border-radius:7px")
        self.label_step1HighLight.setStyleSheet("border-radius:7px;border-color:rgb(0, 170, 255);border-width:2px")
        self.label_step2HighLight.setStyleSheet("border-radius:7px;border-color:rgb(0, 170, 255);border-width:2px")

    def ChooseStudent(self):
        row = self.listWidget_showListStudent.currentRow()
        self.studentInfoObj.ShowStudentInformation(self.lstStudent[row])
        self.pushButton_nextStep.show()
        self.addFaceObj.addForStudent = self.lstStudent[row]
        self.addFGPobj.studentForAdd = self.lstStudent[row]
        self.choseStudent = self.lstStudent[row]

    def GetAndShowListCourse(self):
        khoKhoaHoc = KhoaThiRepository()
        self.lstKhoaThi = khoKhoaHoc.layDanhSach(" 1= 1 ")
        for khoaThi in self.lstKhoaThi:
            self.comboBox_showListCourser.addItem(khoaThi.TenKhoaThi)

    def ChooserCourse(self):
        courseIndex = self.comboBox_showListCourser.currentIndex()
        khoThiSinh = ThiSinhRepository()
        self.lstStudent = khoThiSinh.layDanhSach( " IDKhoaThi == %s "%(self.lstKhoaThi[courseIndex].IDKhoaThi))
        self.listWidget_showListStudent.clear()

        for student in self.lstStudent:
            item =QtWidgets.QListWidgetItem()
            item.setText(student.HoVaTen)
            self.listWidget_showListStudent.addItem(item) 



