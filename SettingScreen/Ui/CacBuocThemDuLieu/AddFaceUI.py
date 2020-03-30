# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ThemKhuonMatThiSinh.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Frame_AddFace(object):
    def setupUi(self, Frame_AddFace):
        Frame_AddFace.setObjectName("Frame_AddFace")
        Frame_AddFace.resize(493, 351)
        Frame_AddFace.setStyleSheet("background-color: rgb(255, 255, 255);")
        Frame_AddFace.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Frame_AddFace.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_forShowNameStudent = QtWidgets.QLabel(Frame_AddFace)
        self.label_forShowNameStudent.setGeometry(QtCore.QRect(82, 0, 323, 41))
        self.label_forShowNameStudent.setStyleSheet("color: rgb(35, 35, 35);\n"
"color: rgb(0, 85, 127);\n"
"font: 75 bold 16pt \"Ubuntu\";")
        self.label_forShowNameStudent.setAlignment(QtCore.Qt.AlignCenter)
        self.label_forShowNameStudent.setObjectName("label_forShowNameStudent")
        self.label_forShowCamera = QtWidgets.QLabel(Frame_AddFace)
        self.label_forShowCamera.setGeometry(QtCore.QRect(30, 50, 425, 267))
        self.label_forShowCamera.setText("")
        self.label_forShowCamera.setObjectName("label_forShowCamera")
        self.label_countdownTime = QtWidgets.QLabel(Frame_AddFace)
        self.label_countdownTime.setGeometry(QtCore.QRect(426, 0, 57, 51))
        self.label_countdownTime.setStyleSheet("color: rgb(0, 170, 255);\n"
"font: 75 bold 26pt \"Ubuntu\";")
        self.label_countdownTime.setObjectName("label_countdownTime")

        self.retranslateUi(Frame_AddFace)
        QtCore.QMetaObject.connectSlotsByName(Frame_AddFace)

    def retranslateUi(self, Frame_AddFace):
        _translate = QtCore.QCoreApplication.translate
        Frame_AddFace.setWindowTitle(_translate("Frame_AddFace", "Frame"))
        self.label_forShowNameStudent.setText(_translate("Frame_AddFace", "Thêm khuôn mặt thí sinh"))
        self.label_countdownTime.setText(_translate("Frame_AddFace", "3"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame_AddFace = QtWidgets.QFrame()
    ui = Ui_Frame_AddFace()
    ui.setupUi(Frame_AddFace)
    Frame_AddFace.show()
    sys.exit(app.exec_())

