# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ManHinhChonHocVien.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(800, 429)
        Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame = QtWidgets.QFrame(Frame)
        self.frame.setGeometry(QtCore.QRect(5, 5, 785, 417))
        self.frame.setStyleSheet("background-color: rgb(191, 191, 191);\n"
"border-radius:7px")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_forScroll = QtWidgets.QFrame(self.frame)
        self.frame_forScroll.setGeometry(QtCore.QRect(-240, 10, 1021, 411))
        self.frame_forScroll.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_forScroll.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_forScroll.setObjectName("frame_forScroll")
        self.pushButton_hideOrShowListCourse = QtWidgets.QPushButton(self.frame_forScroll)
        self.pushButton_hideOrShowListCourse.setGeometry(QtCore.QRect(245, 0, 30, 400))
        self.pushButton_hideOrShowListCourse.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius:0px")
        self.pushButton_hideOrShowListCourse.setText("")
        self.pushButton_hideOrShowListCourse.setIconSize(QtCore.QSize(28, 28))
        self.pushButton_hideOrShowListCourse.setObjectName("pushButton_hideOrShowListCourse")
        self.frame_containListStudent = QtWidgets.QFrame(self.frame_forScroll)
        self.frame_containListStudent.setGeometry(QtCore.QRect(280, 0, 431, 401))
        self.frame_containListStudent.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame_containListStudent.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_containListStudent.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_containListStudent.setObjectName("frame_containListStudent")
        self.tableWidget_forShowListStudent = QtWidgets.QTableWidget(self.frame_containListStudent)
        self.tableWidget_forShowListStudent.setGeometry(QtCore.QRect(10, 60, 411, 331))
        self.tableWidget_forShowListStudent.setStyleSheet("background-color: rgb(189, 189, 189);")
        self.tableWidget_forShowListStudent.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget_forShowListStudent.setDragEnabled(False)
        self.tableWidget_forShowListStudent.setAlternatingRowColors(True)
        self.tableWidget_forShowListStudent.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget_forShowListStudent.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget_forShowListStudent.setObjectName("tableWidget_forShowListStudent")
        self.tableWidget_forShowListStudent.setColumnCount(0)
        self.tableWidget_forShowListStudent.setRowCount(0)
        self.tableWidget_forShowListStudent.verticalHeader().setDefaultSectionSize(30)
        self.tableWidget_forShowListStudent.verticalHeader().setMinimumSectionSize(25)
        self.textEdit_inputTextForSearch = QtWidgets.QTextEdit(self.frame_containListStudent)
        self.textEdit_inputTextForSearch.setGeometry(QtCore.QRect(80, 10, 261, 41))
        self.textEdit_inputTextForSearch.setStyleSheet("background-color: rgb(198, 198, 198);\n"
"border-color: rgb(0, 0, 0);\n"
"border-radius:0px;\n"
"border-width:2px;")
        self.textEdit_inputTextForSearch.setObjectName("textEdit_inputTextForSearch")
        self.label_showIconSearch = QtWidgets.QLabel(self.frame_containListStudent)
        self.label_showIconSearch.setGeometry(QtCore.QRect(20, 10, 51, 41))
        self.label_showIconSearch.setStyleSheet("")
        self.label_showIconSearch.setText("")
        self.label_showIconSearch.setPixmap(QtGui.QPixmap("../../icon/iconSearch.png"))
        self.label_showIconSearch.setObjectName("label_showIconSearch")
        self.pushButton = QtWidgets.QPushButton(self.frame_containListStudent)
        self.pushButton.setGeometry(QtCore.QRect(350, 10, 71, 41))
        self.pushButton.setObjectName("pushButton")
        self.frame_3 = QtWidgets.QFrame(self.frame_forScroll)
        self.frame_3.setGeometry(QtCore.QRect(715, 0, 301, 401))
        self.frame_3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.label_studentImageudentImage = QtWidgets.QLabel(self.frame_3)
        self.label_studentImageudentImage.setGeometry(QtCore.QRect(20, 10, 141, 181))
        self.label_studentImageudentImage.setText("")
        self.label_studentImageudentImage.setPixmap(QtGui.QPixmap("../../icon/noCamera.png"))
        self.label_studentImageudentImage.setObjectName("label_studentImageudentImage")
        self.label_studentName = QtWidgets.QLabel(self.frame_3)
        self.label_studentName.setGeometry(QtCore.QRect(10, 200, 281, 51))
        self.label_studentName.setStyleSheet("color: rgb(0, 0, 255);\n"
"font: 75 bold 12pt \"Ubuntu\";")
        self.label_studentName.setAlignment(QtCore.Qt.AlignCenter)
        self.label_studentName.setObjectName("label_studentName")
        self.label_3 = QtWidgets.QLabel(self.frame_3)
        self.label_3.setGeometry(QtCore.QRect(10, 250, 101, 31))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.frame_3)
        self.label_4.setGeometry(QtCore.QRect(10, 280, 101, 31))
        self.label_4.setObjectName("label_4")
        self.label_dateOfBird = QtWidgets.QLabel(self.frame_3)
        self.label_dateOfBird.setGeometry(QtCore.QRect(120, 250, 171, 31))
        self.label_dateOfBird.setText("")
        self.label_dateOfBird.setObjectName("label_dateOfBird")
        self.label_identNumber = QtWidgets.QLabel(self.frame_3)
        self.label_identNumber.setGeometry(QtCore.QRect(120, 280, 171, 31))
        self.label_identNumber.setText("")
        self.label_identNumber.setObjectName("label_identNumber")
        self.pushButton_addFGP = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_addFGP.setGeometry(QtCore.QRect(170, 20, 123, 47))
        self.pushButton_addFGP.setStyleSheet("background-color: rgba(85, 255, 255, 70);\n"
"font: 75 bold 12pt \"Ubuntu\";\n"
"border-radius:5px;\n"
"border-color:rgb(33, 148, 255);\n"
"border-width:1px;\n"
"border-style:solid;")
        self.pushButton_addFGP.setObjectName("pushButton_addFGP")
        self.pushButton_addFace = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_addFace.setGeometry(QtCore.QRect(170, 80, 123, 47))
        self.pushButton_addFace.setStyleSheet("background-color: rgba(85, 255, 255, 70);\n"
"font: 75 bold 12pt \"Ubuntu\";\n"
"border-radius:5px;\n"
"border-color:rgb(33, 148, 255);\n"
"border-width:1px;\n"
"border-style:solid;")
        self.pushButton_addFace.setObjectName("pushButton_addFace")
        self.pushButton_addCard = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_addCard.setGeometry(QtCore.QRect(170, 140, 123, 47))
        self.pushButton_addCard.setStyleSheet("background-color: rgba(85, 255, 255, 70);\n"
"font: 75 bold 12pt \"Ubuntu\";\n"
"border-radius:5px;\n"
"border-color:rgb(33, 148, 255);\n"
"border-width:1px;\n"
"border-style:solid;")
        self.pushButton_addCard.setObjectName("pushButton_addCard")
        self.frame_containListCourse = QtWidgets.QFrame(self.frame_forScroll)
        self.frame_containListCourse.setGeometry(QtCore.QRect(10, 0, 230, 400))
        self.frame_containListCourse.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame_containListCourse.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_containListCourse.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_containListCourse.setObjectName("frame_containListCourse")
        self.listView_showListCourse = QtWidgets.QListWidget(self.frame_containListCourse)
        self.listView_showListCourse.setGeometry(QtCore.QRect(10, 60, 211, 331))
        self.listView_showListCourse.setStyleSheet("background-color: rgb(202, 202, 202);")
        self.listView_showListCourse.setObjectName("listView_showListCourse")
        self.label = QtWidgets.QLabel(self.frame_containListCourse)
        self.label.setGeometry(QtCore.QRect(10, 10, 201, 41))
        self.label.setStyleSheet("font: 75 bold 11pt \"Ubuntu\";")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.pushButton.setText(_translate("Frame", "XÓA"))
        self.label_studentName.setText(_translate("Frame", "NGUYỄN HỒNG LÂM"))
        self.label_3.setText(_translate("Frame", "NGÀY SINH: "))
        self.label_4.setText(_translate("Frame", "SỐ CMTND:"))
        self.pushButton_addFGP.setText(_translate("Frame", "VÂN TAY"))
        self.pushButton_addFace.setText(_translate("Frame", "KHUÔN MẶT"))
        self.pushButton_addCard.setText(_translate("Frame", "THẺ"))
        self.label.setText(_translate("Frame", "CHỌN MỘT KHÓA HỌC"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame = QtWidgets.QFrame()
    ui = Ui_Frame()
    ui.setupUi(Frame)
    Frame.show()
    sys.exit(app.exec_())
