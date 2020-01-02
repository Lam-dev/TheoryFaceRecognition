# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ManHinhQuanLyDatabase.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame_containDatabaseScreen(object):
    def setupUi(self, Frame_containDatabaseScreen):
        Frame_containDatabaseScreen.setObjectName("Frame_containDatabaseScreen")
        Frame_containDatabaseScreen.resize(800, 480)
        Frame_containDatabaseScreen.setStyleSheet("background-color: rgb(167, 200, 191);\n"
"")
        Frame_containDatabaseScreen.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Frame_containDatabaseScreen.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_tabarScreen = QtWidgets.QFrame(Frame_containDatabaseScreen)
        self.frame_tabarScreen.setGeometry(QtCore.QRect(0, 0, 801, 45))
        self.frame_tabarScreen.setStyleSheet("background-color: rgb(85, 170, 127);")
        self.frame_tabarScreen.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_tabarScreen.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_tabarScreen.setObjectName("frame_tabarScreen")
        self.pushButton_closeDatabaseScreen = QtWidgets.QPushButton(self.frame_tabarScreen)
        self.pushButton_closeDatabaseScreen.setGeometry(QtCore.QRect(752, 2, 43, 39))
        self.pushButton_closeDatabaseScreen.setStyleSheet("margin: 1px; padding: 7px;\n"
"background-color: rgb(255, 255, 255);\n"
"color: rgba(0,190,255,255);\n"
"border-style: solid;\n"
"border-radius: 3px;\n"
"border-width: 1px;\n"
"border-color: rgba(0,140,255,255);")
        self.pushButton_closeDatabaseScreen.setText("")
        self.pushButton_closeDatabaseScreen.setObjectName("pushButton_closeDatabaseScreen")
        self.frame_2 = QtWidgets.QFrame(Frame_containDatabaseScreen)
        self.frame_2.setGeometry(QtCore.QRect(6, 50, 287, 63))
        self.frame_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-style:solid;\n"
"border-radius:3px;")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label_luaChonKhoaHoc = QtWidgets.QLabel(self.frame_2)
        self.label_luaChonKhoaHoc.setGeometry(QtCore.QRect(64, 4, 207, 17))
        self.label_luaChonKhoaHoc.setObjectName("label_luaChonKhoaHoc")
        self.comboBox_showListCourser = QtWidgets.QComboBox(self.frame_2)
        self.comboBox_showListCourser.setGeometry(QtCore.QRect(12, 30, 265, 27))
        self.comboBox_showListCourser.setStyleSheet("margin: 1px; padding: 7px;\n"
"background-color: rgb(255, 255, 255);\n"
"color: rgba(0,190,255,255);\n"
"border-style: solid;\n"
"border-radius: 3px;\n"
"border-width: 1px;\n"
"border-color: rgba(0,140,255,255);")
        self.comboBox_showListCourser.setObjectName("comboBox_showListCourser")
        self.frame_3 = QtWidgets.QFrame(Frame_containDatabaseScreen)
        self.frame_3.setGeometry(QtCore.QRect(6, 120, 287, 353))
        self.frame_3.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-style:solid;\n"
"border-radius:3px;")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.label_3 = QtWidgets.QLabel(self.frame_3)
        self.label_3.setGeometry(QtCore.QRect(46, 6, 207, 17))
        self.label_3.setObjectName("label_3")
        self.listView_forShowListStudent = QtWidgets.QListView(self.frame_3)
        self.listView_forShowListStudent.setGeometry(QtCore.QRect(12, 30, 265, 267))
        self.listView_forShowListStudent.setStyleSheet("background-color: rgb(182, 182, 182);")
        self.listView_forShowListStudent.setObjectName("listView_forShowListStudent")
        self.lineEdit_forInputTextToSearch = QtWidgets.QLineEdit(self.frame_3)
        self.lineEdit_forInputTextToSearch.setGeometry(QtCore.QRect(56, 310, 219, 27))
        self.lineEdit_forInputTextToSearch.setObjectName("lineEdit_forInputTextToSearch")
        self.label_forShowIconSearch = QtWidgets.QLabel(self.frame_3)
        self.label_forShowIconSearch.setGeometry(QtCore.QRect(14, 308, 31, 29))
        self.label_forShowIconSearch.setObjectName("label_forShowIconSearch")
        self.frame_containAddInformationStep = QtWidgets.QFrame(Frame_containDatabaseScreen)
        self.frame_containAddInformationStep.setGeometry(QtCore.QRect(300, 50, 493, 423))
        self.frame_containAddInformationStep.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-style:solid;\n"
"border-radius:3px;")
        self.frame_containAddInformationStep.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_containAddInformationStep.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_containAddInformationStep.setObjectName("frame_containAddInformationStep")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.frame_containAddInformationStep)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(184, 388, 145, 27))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(15)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_step1HighLight = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_step1HighLight.setObjectName("label_step1HighLight")
        self.horizontalLayout.addWidget(self.label_step1HighLight)
        self.label_step2HighLight = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_step2HighLight.setObjectName("label_step2HighLight")
        self.horizontalLayout.addWidget(self.label_step2HighLight)
        self.label_step3HighLight = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_step3HighLight.setObjectName("label_step3HighLight")
        self.horizontalLayout.addWidget(self.label_step3HighLight)

        self.retranslateUi(Frame_containDatabaseScreen)
        QtCore.QMetaObject.connectSlotsByName(Frame_containDatabaseScreen)

    def retranslateUi(self, Frame_containDatabaseScreen):
        _translate = QtCore.QCoreApplication.translate
        Frame_containDatabaseScreen.setWindowTitle(_translate("Frame_containDatabaseScreen", "Frame"))
        self.label_luaChonKhoaHoc.setText(_translate("Frame_containDatabaseScreen", "Lựa chọn khóa học "))
        self.label_3.setText(_translate("Frame_containDatabaseScreen", "Danh sách học viên khóa học"))
        self.label_forShowIconSearch.setText(_translate("Frame_containDatabaseScreen", "TextLabel"))
        self.label_step1HighLight.setText(_translate("Frame_containDatabaseScreen", "TextLabel"))
        self.label_step2HighLight.setText(_translate("Frame_containDatabaseScreen", "TextLabel"))
        self.label_step3HighLight.setText(_translate("Frame_containDatabaseScreen", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame_containDatabaseScreen = QtWidgets.QFrame()
    ui = Ui_Frame_containDatabaseScreen()
    ui.setupUi(Frame_containDatabaseScreen)
    Frame_containDatabaseScreen.show()
    sys.exit(app.exec_())
