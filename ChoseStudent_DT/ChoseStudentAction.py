from ChoseStudent_DT.ChoseStudentUi     import Ui_Frame
from PyQt5          import QtCore, QtGui
from PyQt5.QtCore   import pyqtSlot, pyqtSignal,QTimer, QDateTime, Qt, QObject, QPointF, QPropertyAnimation, pyqtProperty, QSize
from PyQt5          import QtWidgets
import json
import time
from PIL                    import Image, ImageQt
import                      io
from DatabaseAccess.DatabaseAccess            import * 
from    PyQt5.QtWidgets             import QTableWidgetItem

class ChoseStudent(QObject, Ui_Frame):

    SignalRequestDirectAddFace = pyqtSignal()
    SignalRequestDirectAddFGP = pyqtSignal(str)
    SignalRequesDirectWriteCard = pyqtSignal(str)
    SignalChoseStudent = pyqtSignal(ThongTinThiSinh)

    def __init__(self, frameContain):
        QObject.__init__(self)
        self.frameContainCurrentStep = frameContain
        self.frameContainCurrentStep.show()
        self.setupUi(frameContain)
        self.__pixmapOffChooseCourse = QtGui.QIcon('icon/offChooseCourse.png')
        self.__pixmapOnChooseCourse = QtGui.QIcon('icon/onChooseCourse.png')
        self.__choseStudent = ThongTinThiSinh
        self.__lstStudent = list
        self.__lstCourse = list
        self.__choseCourse = object
        self.pushButton_hideOrShowListCourse.clicked.connect(self.onOffShowCourse)
        self.listView_showListCourse.currentRowChanged.connect(self.ChoseCouse)

        ####$$
        self.tableWidget_forShowListStudent.setColumnCount(2)
        self.tableWidget_forShowListStudent.setHorizontalHeaderLabels(['HỌ VÀ TÊN', 'CMTND'])
        self.tableWidget_forShowListStudent.showGrid = False
        self.tableWidget_forShowListStudent.verticalHeader().setDefaultSectionSize(40)
        self.tableWidget_forShowListStudent.setColumnWidth(0, 200)
        self.tableWidget_forShowListStudent.setColumnWidth(1, 60)
        self.tableWidget_forShowListStudent.clicked.connect(self.tableWidgetCellClick)
        ########

        self.pushButton_addFace.clicked.connect(lambda: self.SignalRequestDirectAddFace.emit())
        self.pushButton_addFGP.clicked.connect(lambda: self.SignalRequestDirectAddFGP.emit('{"utTrai":false,"nhanTrai":false,"giuaTrai":false,"troTrai":false,"caiTrai":false,"caiPhai":false,"troPhai":false,"giuaPhai":true,"nhanPhai":false,"utPhai":false}'))
        self.pushButton_addCard.clicked.connect(lambda: self.SignalRequesDirectWriteCard.emit(self.__choseStudent.SoCMTND))



        self.__GetAndShowListCourse()

    def ChoseCouse(self):
        self.__choseCourse = self.__lstCourse[self.listView_showListCourse.currentRow()]
        khoThiSinh = ThiSinhRepository()
        self.__lstStudent = khoThiSinh.layDanhSach(" IDKhoaThi =  "+str(self.__choseCourse.IDKhoaThi))
        self.tableWidget_forShowListStudent.setRowCount(len(self.__lstStudent))
        dem = 0
        for student in self.__lstStudent:
            self.tableWidget_forShowListStudent.setItem(dem,0, QTableWidgetItem(str(student.HoVaTen)))
            self.tableWidget_forShowListStudent.setItem(dem,1, QTableWidgetItem(str(student.SoCMTND)))
            # self.tableWidget_forShowListStudent.setItem(dem, 2 , QTableWidgetItem(student.NgaySinh))
            
            # if(len(student.NhanDienKhuonMatThem) != 0):
                
            #     self.tableWidget_forShowListStudent.setItem(dem, 3, QTableWidgetItem("Đã có"))
            # else:
            #     item = QTableWidgetItem("Chưa có")
            #     item.setForeground(QtGui.QColor(255, 0, 0))
            #     self.tableWidget_forShowListStudent.setItem(dem, 3, item)

            # if(len(student.NhanDienVanTay) != 0):
            #     self.tableWidget_forShowListStudent.setItem(dem, 4, QTableWidgetItem("Đã có"))
            # else:
            #     item = QTableWidgetItem("Chưa có")
            #     item.setForeground(QtGui.QColor(255, 0, 0))
            #     self.tableWidget_forShowListStudent.setItem(dem, 4, item)
            # if(dem % 2 == 0):
                # self.tableWidget_forShowListStudent.item(dem, 0).setBackground(QtGui.QColor(255, 255, 255))
                # self.tableWidget_forShowListStudent.item(dem, 1).setBackground(QtGui.QColor(255, 255, 255))
                # self.tableWidget_forShowListStudent.item(dem, 2).setBackground(QtGui.QColor(255, 255, 255))
                # self.tableWidget_forShowListStudent.item(dem, 3).setBackground(QtGui.QColor(255, 255, 255))
                # self.tableWidget_forShowListStudent.item(dem, 4).setBackground(QtGui.QColor(255, 255, 255))
            dem += 1

    def ShowStudentInformation(self, student):
        try:
            self.label_studentImageudentImage.clear()
            image = Image.open(io.BytesIO(student.AnhDangKy))
            qim = ImageQt.ImageQt(image)
            pix = QtGui.QPixmap.fromImage(qim)
            resizePixmap = pix.scaled(150, 200, QtCore.Qt.KeepAspectRatio)
            # self.SetGeometryForLabelShowRegisImage(resizePixmap.width(), resizePixmap.height())
            self.label_studentImageudentImage.setPixmap(resizePixmap)
        except Exception as ex:
            print(ex.args)
            self.label_studentImageudentImage.setText("KHÔNG CÓ ẢNH")

        self.label_studentName.setText(student.HoVaTen.upper())
        self.label_identNumber.setText(student.SoCMTND)


    def __GetAndShowListCourse(self):
        courseRepo = KhoaThiRepository()
        self.__lstCourse = courseRepo.layDanhSach(" 1 = 1 ")
        for course in self.__lstCourse:
            self.listView_showListCourse.addItem(course.TenKhoaThi)

    

    def tableWidgetCellClick(self):
        self.__choseStudent  = self.__lstStudent[self.tableWidget_forShowListStudent.selectedIndexes()[0].row()]
        self.ShowStudentInformation(self.__choseStudent)
        self.SignalChoseStudent.emit(self.__choseStudent)
        
         
    def buttonOnOffShowCourseToggle(self):
        if(self.frame_forScroll.x() == 0):
            self.pushButton_hideOrShowListCourse.setIcon(self.__pixmapOffChooseCourse)
        else:
            self.pushButton_hideOrShowListCourse.setIcon(self.__pixmapOnChooseCourse)

    def onOffShowCourse(self):
        if(self.frame_forScroll.x() == 0):
            self.anim_chooseCourseTab = QPropertyAnimation(self.frame_forScroll, b"geometry")
            self.anim_chooseCourseTab.setDuration(300)
            self.anim_chooseCourseTab.setStartValue(QtCore.QRect(0, 10, 1021, 411))
            self.anim_chooseCourseTab.setEndValue(QtCore.QRect(-240, 10, 1021, 411))
            
        else:
            self.anim_chooseCourseTab = QPropertyAnimation(self.frame_forScroll, b"geometry")
            self.anim_chooseCourseTab.setDuration(300)
            self.anim_chooseCourseTab.setEndValue(QtCore.QRect(0, 10, 1021, 411))
            self.anim_chooseCourseTab.setStartValue(QtCore.QRect(-240, 10, 1021, 411))
        
        self.anim_chooseCourseTab.start()
        self.anim_chooseCourseTab.finished.connect(self.buttonOnOffShowCourseToggle)


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
        