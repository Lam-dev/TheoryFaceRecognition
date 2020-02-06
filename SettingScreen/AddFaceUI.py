
# Form implementation generated from reading ui file 'ThemKhuonMatThiSinh.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
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
        self.label_themKhuonMatThiSinh = QtWidgets.QLabel(Frame_AddFace)
        self.label_themKhuonMatThiSinh.setGeometry(QtCore.QRect(82, 12, 323, 17))
        self.label_themKhuonMatThiSinh.setStyleSheet("color: rgb(35, 35, 35);\n"
"font: 75 bold 16pt \"Ubuntu\";")
        self.label_themKhuonMatThiSinh.setAlignment(QtCore.Qt.AlignCenter)
        self.label_themKhuonMatThiSinh.setObjectName("label_themKhuonMatThiSinh")
        self.label_forShowCamera = QtWidgets.QLabel(Frame_AddFace)
        self.label_forShowCamera.setGeometry(QtCore.QRect(36, 62, 425, 267))
        self.label_forShowCamera.setText("")
        self.label_forShowCamera.setObjectName("label_forShowCamera")
        self.label_countdownTime = QtWidgets.QLabel(Frame_AddFace)
        self.label_countdownTime.setGeometry(QtCore.QRect(428, 0, 49, 47))
        self.label_countdownTime.setStyleSheet("color: rgb(0, 170, 255);\n"
"font: 75 bold 26pt \"Ubuntu\";")
        self.label_countdownTime.setObjectName("label_countdownTime")

        self.retranslateUi(Frame_AddFace)
        QtCore.QMetaObject.connectSlotsByName(Frame_AddFace)

    def retranslateUi(self, Frame_AddFace):
        _translate = QtCore.QCoreApplication.translate
        Frame_AddFace.setWindowTitle(_translate("Frame_AddFace", "Frame"))
        self.label_themKhuonMatThiSinh.setText(_translate("Frame_AddFace", "Thêm khuôn mặt thí sinh"))
        self.label_countdownTime.setText(_translate("Frame_AddFace", "3"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame_AddFace = QtWidgets.QFrame()
    ui = Ui_Frame_AddFace()
    ui.setupUi(Frame_AddFace)
    Frame_AddFace.show()
    sys.exit(app.exec_())
