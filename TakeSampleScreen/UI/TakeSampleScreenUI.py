# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ManHinhLayMau.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(800, 480)
        Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_containLogoAndDeviceName = QtWidgets.QFrame(Frame)
        self.frame_containLogoAndDeviceName.setGeometry(QtCore.QRect(0, 0, 800, 50))
        self.frame_containLogoAndDeviceName.setStyleSheet("background-color: rgb(150, 220, 170);")
        self.frame_containLogoAndDeviceName.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_containLogoAndDeviceName.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_containLogoAndDeviceName.setObjectName("frame_containLogoAndDeviceName")
        self.label_deviceName = QtWidgets.QLabel(self.frame_containLogoAndDeviceName)
        self.label_deviceName.setGeometry(QtCore.QRect(150, 0, 391, 41))
        self.label_deviceName.setStyleSheet("color: rgb(191, 0, 0);\n"
"font: 75 bold 14pt \"Ubuntu\";")
        self.label_deviceName.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_deviceName.setObjectName("label_deviceName")
        self.pushButton_exit = QtWidgets.QPushButton(self.frame_containLogoAndDeviceName)
        self.pushButton_exit.setGeometry(QtCore.QRect(740, 0, 61, 51))
        self.pushButton_exit.setStyleSheet("background-color: rgb(150, 220, 170);\n"
"font: 75 bold 12pt \"Ubuntu\";")
        self.pushButton_exit.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../icon/closeIcon50.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_exit.setIcon(icon)
        self.pushButton_exit.setIconSize(QtCore.QSize(60, 60))
        self.pushButton_exit.setObjectName("pushButton_exit")
        self.pushButton_choseStudent = QtWidgets.QPushButton(self.frame_containLogoAndDeviceName)
        self.pushButton_choseStudent.setGeometry(QtCore.QRect(0, 0, 141, 51))
        self.pushButton_choseStudent.setStyleSheet("background-color: rgb(150, 220, 170);\n"
"font: 75 bold 12pt \"Ubuntu\";\n"
"")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../../icon/back40.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_choseStudent.setIcon(icon1)
        self.pushButton_choseStudent.setIconSize(QtCore.QSize(40, 40))
        self.pushButton_choseStudent.setObjectName("pushButton_choseStudent")
        self.label_addDataMode = QtWidgets.QLabel(self.frame_containLogoAndDeviceName)
        self.label_addDataMode.setGeometry(QtCore.QRect(550, 0, 161, 41))
        self.label_addDataMode.setStyleSheet("color: rgb(0, 65, 195);\n"
"font: 75 bold 14pt \"Ubuntu\";")
        self.label_addDataMode.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_addDataMode.setObjectName("label_addDataMode")

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.label_deviceName.setText(_translate("Frame", "LẤY MẪU VÂN TAY, KHUÔN MẶT, THẺ"))
        self.pushButton_choseStudent.setText(_translate("Frame", "Chọn học \n"
" viên"))
        self.label_addDataMode.setText(_translate("Frame", "TRỰC TIẾP"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame = QtWidgets.QFrame()
    ui = Ui_Frame()
    ui.setupUi(Frame)
    Frame.show()
    sys.exit(app.exec_())
