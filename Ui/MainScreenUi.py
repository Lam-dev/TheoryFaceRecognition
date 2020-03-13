# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainScreen.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame_MainScreen(object):
    def setupUi(self, Frame_MainScreen):
        Frame_MainScreen.setObjectName("Frame_MainScreen")
        Frame_MainScreen.resize(800, 480)
        Frame_MainScreen.setStyleSheet("background-color: rgb(167, 200, 191);\n"
"")
        Frame_MainScreen.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Frame_MainScreen.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_containName = QtWidgets.QFrame(Frame_MainScreen)
        self.frame_containName.setGeometry(QtCore.QRect(0, 2, 799, 59))
        self.frame_containName.setStyleSheet("border-style:solid;\n"
"border-width:0px")
        self.frame_containName.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_containName.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_containName.setObjectName("frame_containName")
        self.label_cty = QtWidgets.QLabel(self.frame_containName)
        self.label_cty.setGeometry(QtCore.QRect(82, -2, 555, 27))
        self.label_cty.setStyleSheet("color: rgb(0, 0, 255);\n"
"font: 75 bold 14pt \"Ubuntu\";")
        self.label_cty.setAlignment(QtCore.Qt.AlignCenter)
        self.label_cty.setIndent(-1)
        self.label_cty.setObjectName("label_cty")
        self.label_7 = QtWidgets.QLabel(self.frame_containName)
        self.label_7.setGeometry(QtCore.QRect(654, 4, 155, 37))
        self.label_7.setText("")
        self.label_7.setPixmap(QtGui.QPixmap("../icon/iconEcotek.png"))
        self.label_7.setObjectName("label_7")
        self.pushButton_shutdown = QtWidgets.QPushButton(self.frame_containName)
        self.pushButton_shutdown.setGeometry(QtCore.QRect(8, 2, 65, 51))
        self.pushButton_shutdown.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"border-radius:2px;")
        self.pushButton_shutdown.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../icon/iconShutdown.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_shutdown.setIcon(icon)
        self.pushButton_shutdown.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_shutdown.setObjectName("pushButton_shutdown")
        self.label_cty_2 = QtWidgets.QLabel(self.frame_containName)
        self.label_cty_2.setGeometry(QtCore.QRect(112, 24, 531, 27))
        self.label_cty_2.setStyleSheet("color: rgb(200, 0, 0);\n"
"font: 75 bold 12pt \"Ubuntu\";")
        self.label_cty_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_cty_2.setIndent(-1)
        self.label_cty_2.setObjectName("label_cty_2")
        self.label_cty.raise_()
        self.label_7.raise_()
        self.pushButton_shutdown.raise_()
        self.label_cty_2.raise_()
        self.line = QtWidgets.QFrame(Frame_MainScreen)
        self.line.setGeometry(QtCore.QRect(132, 50, 487, 17))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.frame = QtWidgets.QFrame(Frame_MainScreen)
        self.frame.setGeometry(QtCore.QRect(350, 66, 441, 405))
        self.frame.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-style:solid;\n"
"border-radius:7px")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setLineWidth(5)
        self.frame.setObjectName("frame")
        self.label_forShowName = QtWidgets.QLabel(self.frame)
        self.label_forShowName.setGeometry(QtCore.QRect(184, 44, 245, 103))
        self.label_forShowName.setStyleSheet("font: 75 bold 20pt \"Ubuntu\";\n"
"color: rgb(70, 70, 70);\n"
"border-radius:3px;\n"
"")
        self.label_forShowName.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_forShowName.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_forShowName.setLineWidth(1)
        self.label_forShowName.setMidLineWidth(0)
        self.label_forShowName.setAlignment(QtCore.Qt.AlignCenter)
        self.label_forShowName.setWordWrap(True)
        self.label_forShowName.setObjectName("label_forShowName")
        self.frame_containLabelShowRegisImage = QtWidgets.QFrame(self.frame)
        self.frame_containLabelShowRegisImage.setGeometry(QtCore.QRect(4, 8, 173, 185))
        self.frame_containLabelShowRegisImage.setStyleSheet("border-style:solid;\n"
"border-width:0px")
        self.frame_containLabelShowRegisImage.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_containLabelShowRegisImage.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_containLabelShowRegisImage.setObjectName("frame_containLabelShowRegisImage")
        self.label_regisImage = QtWidgets.QLabel(self.frame_containLabelShowRegisImage)
        self.label_regisImage.setGeometry(QtCore.QRect(6, 10, 167, 171))
        self.label_regisImage.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"")
        self.label_regisImage.setText("")
        self.label_regisImage.setPixmap(QtGui.QPixmap("../icon/iconImageRepresent.png"))
        self.label_regisImage.setObjectName("label_regisImage")
        self.label_showConnectOrDisconnect = QtWidgets.QLabel(self.frame)
        self.label_showConnectOrDisconnect.setGeometry(QtCore.QRect(412, 6, 16, 16))
        self.label_showConnectOrDisconnect.setStyleSheet("background-color: rgb(0, 170, 0);\n"
"border-radius:8")
        self.label_showConnectOrDisconnect.setText("")
        self.label_showConnectOrDisconnect.setObjectName("label_showConnectOrDisconnect")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect(14, 198, 415, 187))
        self.frame_2.setStyleSheet("background-color: rgba(150, 150, 150, 0);\n"
"border-color: rgb(208, 208, 208);\n"
"border-style:solid;\n"
"border-radius:5px; \n"
"border-width:1px;")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.line_2 = QtWidgets.QFrame(self.frame_2)
        self.line_2.setGeometry(QtCore.QRect(0, 46, 415, 1))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self.frame_2)
        self.line_3.setGeometry(QtCore.QRect(0, 93, 415, 1))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(self.frame_2)
        self.line_4.setGeometry(QtCore.QRect(2, 139, 415, 1))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setGeometry(QtCore.QRect(14, 98, 147, 35))
        self.label.setStyleSheet("border-width:0px;\n"
"font: 75 bold 11pt \"Ubuntu\";\n"
"")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setGeometry(QtCore.QRect(14, 56, 147, 29))
        self.label_2.setStyleSheet("border-width:0px;\n"
"font: 75 bold 11pt \"Ubuntu\";")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.frame_2)
        self.label_3.setGeometry(QtCore.QRect(12, 10, 147, 29))
        self.label_3.setStyleSheet("border-width:0px;\n"
"font: 57 bold 11pt \"Ubuntu\";")
        self.label_3.setIndent(-1)
        self.label_3.setObjectName("label_3")
        self.label_dateOfBird = QtWidgets.QLabel(self.frame_2)
        self.label_dateOfBird.setGeometry(QtCore.QRect(152, 54, 247, 35))
        self.label_dateOfBird.setStyleSheet("border-width:0px;\n"
"font: 75 bold 11pt \"Ubuntu\";\n"
"color: rgb(0, 0, 127);\n"
"")
        self.label_dateOfBird.setText("")
        self.label_dateOfBird.setObjectName("label_dateOfBird")
        self.label_forShowIdentNumber = QtWidgets.QLabel(self.frame_2)
        self.label_forShowIdentNumber.setGeometry(QtCore.QRect(156, 4, 247, 35))
        self.label_forShowIdentNumber.setStyleSheet("border-width:0px;\n"
"font: 75 bold 11pt \"Ubuntu\";\n"
"color: rgb(0, 0, 127);\n"
"")
        self.label_forShowIdentNumber.setText("")
        self.label_forShowIdentNumber.setObjectName("label_forShowIdentNumber")
        self.label_8 = QtWidgets.QLabel(self.frame_2)
        self.label_8.setGeometry(QtCore.QRect(14, 150, 103, 29))
        self.label_8.setStyleSheet("border-width:0px;\n"
"font: 57 bold 11pt \"Ubuntu\";")
        self.label_8.setObjectName("label_8")
        self.label_forShowCourse = QtWidgets.QLabel(self.frame_2)
        self.label_forShowCourse.setGeometry(QtCore.QRect(152, 146, 247, 35))
        self.label_forShowCourse.setStyleSheet("border-width:0px;\n"
"font: 75 bold 11pt \"Ubuntu\";\n"
"color: rgb(0, 0, 127);\n"
"")
        self.label_forShowCourse.setText("")
        self.label_forShowCourse.setObjectName("label_forShowCourse")
        self.label_forShowNumberCard = QtWidgets.QLabel(self.frame_2)
        self.label_forShowNumberCard.setGeometry(QtCore.QRect(152, 100, 251, 35))
        self.label_forShowNumberCard.setStyleSheet("border-width:0px;\n"
"font: 75 bold 11pt \"Ubuntu\";\n"
"color: rgb(0, 0, 127);\n"
"")
        self.label_forShowNumberCard.setText("")
        self.label_forShowNumberCard.setObjectName("label_forShowNumberCard")
        self.frame_3 = QtWidgets.QFrame(Frame_MainScreen)
        self.frame_3.setGeometry(QtCore.QRect(10, 66, 329, 405))
        self.frame_3.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-width:5px;\n"
"border-radius:7px;")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.frame_containLabelShowCamera = QtWidgets.QFrame(self.frame_3)
        self.frame_containLabelShowCamera.setGeometry(QtCore.QRect(18, 8, 297, 391))
        self.frame_containLabelShowCamera.setStyleSheet("border-style:solid;\n"
"border-width:0px")
        self.frame_containLabelShowCamera.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_containLabelShowCamera.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_containLabelShowCamera.setObjectName("frame_containLabelShowCamera")
        self.label_showCamera = QtWidgets.QLabel(self.frame_containLabelShowCamera)
        self.label_showCamera.setGeometry(QtCore.QRect(4, -8, 287, 381))
        self.label_showCamera.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"")
        self.label_showCamera.setText("")
        self.label_showCamera.setObjectName("label_showCamera")
        self.label_forShowIconFaceRecognized = QtWidgets.QLabel(self.frame_containLabelShowCamera)
        self.label_forShowIconFaceRecognized.setGeometry(QtCore.QRect(-4, 0, 301, 169))
        self.label_forShowIconFaceRecognized.setText("")
        self.label_forShowIconFaceRecognized.setPixmap(QtGui.QPixmap("../../../../Downloads/icons8-facial-recognition-100.png"))
        self.label_forShowIconFaceRecognized.setAlignment(QtCore.Qt.AlignCenter)
        self.label_forShowIconFaceRecognized.setObjectName("label_forShowIconFaceRecognized")
        self.label_forShowTimeRecognized = QtWidgets.QLabel(self.frame_containLabelShowCamera)
        self.label_forShowTimeRecognized.setGeometry(QtCore.QRect(-8, 170, 309, 217))
        self.label_forShowTimeRecognized.setStyleSheet("color: rgb(0, 135, 99);\n"
"font: 75 bold 24pt \"Ubuntu\";")
        self.label_forShowTimeRecognized.setLineWidth(1)
        self.label_forShowTimeRecognized.setAlignment(QtCore.Qt.AlignCenter)
        self.label_forShowTimeRecognized.setIndent(5)
        self.label_forShowTimeRecognized.setObjectName("label_forShowTimeRecognized")

        self.retranslateUi(Frame_MainScreen)
        QtCore.QMetaObject.connectSlotsByName(Frame_MainScreen)

    def retranslateUi(self, Frame_MainScreen):
        _translate = QtCore.QCoreApplication.translate
        Frame_MainScreen.setWindowTitle(_translate("Frame_MainScreen", "Frame"))
        self.label_cty.setText(_translate("Frame_MainScreen", "CÔNG TY CỔ PHẦN CÔNG NGHỆ KỸ THUẬT ECOTEK"))
        self.label_cty_2.setText(_translate("Frame_MainScreen", "Thiết bị điểm danh nhận diện khuôn mặt, vân tay"))
        self.label_forShowName.setText(_translate("Frame_MainScreen", "CHƯA NHẬN ĐƯỢC HỌC VIÊN"))
        self.label.setText(_translate("Frame_MainScreen", "SỐ CMTND"))
        self.label_2.setText(_translate("Frame_MainScreen", "NGÀY SINH:"))
        self.label_3.setText(_translate("Frame_MainScreen", "MÃ ĐĂNG KÝ"))
        self.label_8.setText(_translate("Frame_MainScreen", "KHÓA HỌC"))
        self.label_forShowTimeRecognized.setText(_translate("Frame_MainScreen", "25 / 02 / 2020 \n"
" 11 : 34 : 15"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame_MainScreen = QtWidgets.QFrame()
    ui = Ui_Frame_MainScreen()
    ui.setupUi(Frame_MainScreen)
    Frame_MainScreen.show()
    sys.exit(app.exec_())
