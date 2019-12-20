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
        self.label_cty.setGeometry(QtCore.QRect(114, -6, 539, 37))
        self.label_cty.setStyleSheet("color: rgb(0, 0, 255);\n"
"font: 75 bold 14pt \"Ubuntu\";")
        self.label_cty.setIndent(-1)
        self.label_cty.setObjectName("label_cty")
        self.label_trungTam = QtWidgets.QLabel(self.frame_containName)
        self.label_trungTam.setGeometry(QtCore.QRect(182, 28, 453, 27))
        self.label_trungTam.setStyleSheet("font: 75 bold 12pt \"Ubuntu\";\n"
"color: rgb(255, 0, 0);")
        self.label_trungTam.setObjectName("label_trungTam")
        self.label_7 = QtWidgets.QLabel(self.frame_containName)
        self.label_7.setGeometry(QtCore.QRect(666, 4, 143, 37))
        self.label_7.setText("")
        self.label_7.setPixmap(QtGui.QPixmap("../icon/iconEcotek.png"))
        self.label_7.setObjectName("label_7")
        self.pushButton_shutdown = QtWidgets.QPushButton(self.frame_containName)
        self.pushButton_shutdown.setGeometry(QtCore.QRect(4, 2, 39, 35))
        self.pushButton_shutdown.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"border-radius:2px;")
        self.pushButton_shutdown.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../icon/iconShutdown.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_shutdown.setIcon(icon)
        self.pushButton_shutdown.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_shutdown.setObjectName("pushButton_shutdown")
        self.line = QtWidgets.QFrame(Frame_MainScreen)
        self.line.setGeometry(QtCore.QRect(132, 52, 487, 17))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.frame = QtWidgets.QFrame(Frame_MainScreen)
        self.frame.setGeometry(QtCore.QRect(350, 66, 437, 405))
        self.frame.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-style:solid;\n"
"border-radius:7px")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setLineWidth(5)
        self.frame.setObjectName("frame")
        self.label_forShowName = QtWidgets.QLabel(self.frame)
        self.label_forShowName.setGeometry(QtCore.QRect(166, 44, 263, 103))
        self.label_forShowName.setStyleSheet("font: 75 bold 22pt \"Ubuntu\";\n"
"color: rgb(70, 70, 70);\n"
"border-radius:3px;\n"
"")
        self.label_forShowName.setWordWrap(True)
        self.label_forShowName.setObjectName("label_forShowName")
        self.frame_containLabelShowRegisImage = QtWidgets.QFrame(self.frame)
        self.frame_containLabelShowRegisImage.setGeometry(QtCore.QRect(10, 8, 149, 181))
        self.frame_containLabelShowRegisImage.setStyleSheet("border-style:solid;\n"
"border-width:0px")
        self.frame_containLabelShowRegisImage.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_containLabelShowRegisImage.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_containLabelShowRegisImage.setObjectName("frame_containLabelShowRegisImage")
        self.label_regisImage = QtWidgets.QLabel(self.frame_containLabelShowRegisImage)
        self.label_regisImage.setGeometry(QtCore.QRect(8, 10, 131, 165))
        self.label_regisImage.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"")
        self.label_regisImage.setText("")
        self.label_regisImage.setPixmap(QtGui.QPixmap("../icon/iconImageRepresent.png"))
        self.label_regisImage.setObjectName("label_regisImage")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect(10, 190, 413, 213))
        self.frame_2.setStyleSheet("border-color: rgb(220, 220, 220);\n"
"border-style:solid; \n"
"border-width:1px; \n"
"border-radius:5px;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label_forShowNumberCard = QtWidgets.QLabel(self.frame_2)
        self.label_forShowNumberCard.setGeometry(QtCore.QRect(156, 4, 247, 31))
        self.label_forShowNumberCard.setStyleSheet("font: 75 bold 12pt \"Ubuntu\";\n"
"color: rgb(0, 0, 127);\n"
"border-width:0px")
        self.label_forShowNumberCard.setText("")
        self.label_forShowNumberCard.setObjectName("label_forShowNumberCard")
        self.label_sbd = QtWidgets.QLabel(self.frame_2)
        self.label_sbd.setGeometry(QtCore.QRect(8, 10, 123, 27))
        self.label_sbd.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 57 bold 11pt \"Ubuntu\";\n"
"border-width:0px")
        self.label_sbd.setObjectName("label_sbd")
        self.label_khoaThi = QtWidgets.QLabel(self.frame_2)
        self.label_khoaThi.setGeometry(QtCore.QRect(8, 136, 121, 27))
        self.label_khoaThi.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 57 bold 11pt \"Ubuntu\";\n"
"border-width:0px")
        self.label_khoaThi.setObjectName("label_khoaThi")
        self.label_forShowIdentNumber = QtWidgets.QLabel(self.frame_2)
        self.label_forShowIdentNumber.setGeometry(QtCore.QRect(156, 92, 247, 31))
        self.label_forShowIdentNumber.setStyleSheet("font: 75 bold 12pt \"Ubuntu\";\n"
"color: rgb(0, 0, 127);\n"
"border-width:0px")
        self.label_forShowIdentNumber.setText("")
        self.label_forShowIdentNumber.setObjectName("label_forShowIdentNumber")
        self.line_2 = QtWidgets.QFrame(self.frame_2)
        self.line_2.setGeometry(QtCore.QRect(2, 42, 409, 1))
        self.line_2.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self.frame_2)
        self.line_3.setGeometry(QtCore.QRect(2, 84, 409, 1))
        self.line_3.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(self.frame_2)
        self.line_4.setGeometry(QtCore.QRect(0, 128, 409, 1))
        self.line_4.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.label_course = QtWidgets.QLabel(self.frame_2)
        self.label_course.setGeometry(QtCore.QRect(156, 136, 251, 31))
        self.label_course.setStyleSheet("font: 75 bold 12pt \"Ubuntu\";\n"
"color: rgb(0, 0, 127);\n"
"border-width:0px\n"
"\n"
"")
        self.label_course.setText("")
        self.label_course.setObjectName("label_course")
        self.label_soCMTND = QtWidgets.QLabel(self.frame_2)
        self.label_soCMTND.setGeometry(QtCore.QRect(10, 94, 123, 27))
        self.label_soCMTND.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 57 bold 11pt \"Ubuntu\";\n"
"border-width:0px")
        self.label_soCMTND.setObjectName("label_soCMTND")
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setGeometry(QtCore.QRect(8, 56, 101, 17))
        self.label_2.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 57 bold 11pt \"Ubuntu\";\n"
"border-width:0px")
        self.label_2.setObjectName("label_2")
        self.label_dateOfBird = QtWidgets.QLabel(self.frame_2)
        self.label_dateOfBird.setGeometry(QtCore.QRect(156, 46, 247, 31))
        self.label_dateOfBird.setStyleSheet("font: 75 bold 12pt \"Ubuntu\";\n"
"color: rgb(0, 0, 127);\n"
"border-width:0px")
        self.label_dateOfBird.setText("")
        self.label_dateOfBird.setObjectName("label_dateOfBird")
        self.line_5 = QtWidgets.QFrame(self.frame_2)
        self.line_5.setGeometry(QtCore.QRect(2, 170, 409, 1))
        self.line_5.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.label_showConnectOrDisconnect = QtWidgets.QLabel(self.frame)
        self.label_showConnectOrDisconnect.setGeometry(QtCore.QRect(412, 6, 16, 16))
        self.label_showConnectOrDisconnect.setStyleSheet("background-color: rgb(0, 170, 0);\n"
"border-radius:8")
        self.label_showConnectOrDisconnect.setText("")
        self.label_showConnectOrDisconnect.setObjectName("label_showConnectOrDisconnect")
        self.frame_3 = QtWidgets.QFrame(Frame_MainScreen)
        self.frame_3.setGeometry(QtCore.QRect(14, 66, 325, 405))
        self.frame_3.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-width:5px;\n"
"border-radius:7px;")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.frame_containLabelShowCamera = QtWidgets.QFrame(self.frame_3)
        self.frame_containLabelShowCamera.setGeometry(QtCore.QRect(16, 8, 297, 391))
        self.frame_containLabelShowCamera.setStyleSheet("border-style:solid;\n"
"border-width:0px")
        self.frame_containLabelShowCamera.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_containLabelShowCamera.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_containLabelShowCamera.setObjectName("frame_containLabelShowCamera")
        self.label_showCamera = QtWidgets.QLabel(self.frame_containLabelShowCamera)
        self.label_showCamera.setGeometry(QtCore.QRect(0, 0, 283, 381))
        self.label_showCamera.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"")
        self.label_showCamera.setText("")
        self.label_showCamera.setObjectName("label_showCamera")

        self.retranslateUi(Frame_MainScreen)
        QtCore.QMetaObject.connectSlotsByName(Frame_MainScreen)

    def retranslateUi(self, Frame_MainScreen):
        _translate = QtCore.QCoreApplication.translate
        Frame_MainScreen.setWindowTitle(_translate("Frame_MainScreen", "Frame"))
        self.label_cty.setText(_translate("Frame_MainScreen", "TRƯỜNG CAO ĐẲNG CÔNG NGHIỆP VÀ XÂY DỰNG"))
        self.label_trungTam.setText(_translate("Frame_MainScreen", "TRUNG TÂM ĐÀO TẠO VÀ SÁT HẠCH LÁI XE"))
        self.label_forShowName.setText(_translate("Frame_MainScreen", "CHƯA NHẬN ĐƯỢC THÔNG TIN"))
        self.label_sbd.setText(_translate("Frame_MainScreen", "Số báo danh:"))
        self.label_khoaThi.setText(_translate("Frame_MainScreen", "Khóa thi: "))
        self.label_soCMTND.setText(_translate("Frame_MainScreen", "Số CMTND: "))
        self.label_2.setText(_translate("Frame_MainScreen", "Ngày sinh:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame_MainScreen = QtWidgets.QFrame()
    ui = Ui_Frame_MainScreen()
    ui.setupUi(Frame_MainScreen)
    Frame_MainScreen.show()
    sys.exit(app.exec_())
