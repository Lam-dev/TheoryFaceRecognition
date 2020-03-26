# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ThemVanTayThiSinh.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame_AddFGP(object):
    def setupUi(self, Frame_AddFGP):
        Frame_AddFGP.setObjectName("Frame_AddFGP")
        Frame_AddFGP.resize(493, 351)
        Frame_AddFGP.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"")
        Frame_AddFGP.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Frame_AddFGP.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_ThemVanTayThiSinh = QtWidgets.QLabel(Frame_AddFGP)
        self.label_ThemVanTayThiSinh.setGeometry(QtCore.QRect(72, 6, 335, 33))
        self.label_ThemVanTayThiSinh.setStyleSheet("color: rgb(29, 29, 29);\n"
"font: 57 bold 16pt \"Ubuntu\";")
        self.label_ThemVanTayThiSinh.setObjectName("label_ThemVanTayThiSinh")
        self.label_forShowAnoument = QtWidgets.QLabel(Frame_AddFGP)
        self.label_forShowAnoument.setGeometry(QtCore.QRect(64, 298, 375, 41))
        self.label_forShowAnoument.setStyleSheet("color: rgb(216, 0, 0);\n"
"font: 75 bold 14pt \"Ubuntu\";")
        self.label_forShowAnoument.setAlignment(QtCore.Qt.AlignCenter)
        self.label_forShowAnoument.setObjectName("label_forShowAnoument")
        self.label = QtWidgets.QLabel(Frame_AddFGP)
        self.label.setGeometry(QtCore.QRect(50, 72, 273, 57))
        self.label.setStyleSheet("color: rgb(0, 170, 127);\n"
"font: 75 bold 18pt \"Ubuntu\";")
        self.label.setObjectName("label")
        self.label_numberFGPadded = QtWidgets.QLabel(Frame_AddFGP)
        self.label_numberFGPadded.setGeometry(QtCore.QRect(346, 42, 89, 119))
        self.label_numberFGPadded.setStyleSheet("color: rgb(0, 170, 0);\n"
"font: 75 bold 70pt \"Ubuntu\";")
        self.label_numberFGPadded.setObjectName("label_numberFGPadded")
        self.pushButton_addFGP = QtWidgets.QPushButton(Frame_AddFGP)
        self.pushButton_addFGP.setGeometry(QtCore.QRect(310, 194, 81, 73))
        self.pushButton_addFGP.setStyleSheet("background-color: rgba(85, 255, 255, 70);\n"
"font: 75 20pt \"Ubuntu\";\n"
"border-radius:5px;\n"
"border-color:rgb(33, 148, 255);\n"
"border-width:1px;\n"
"border-style:solid;")
        self.pushButton_addFGP.setObjectName("pushButton_addFGP")
        self.pushButton_deleteAllFeature = QtWidgets.QPushButton(Frame_AddFGP)
        self.pushButton_deleteAllFeature.setGeometry(QtCore.QRect(70, 192, 81, 73))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(20)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(9)
        font.setStrikeOut(False)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.pushButton_deleteAllFeature.setFont(font)
        self.pushButton_deleteAllFeature.setMouseTracking(False)
        self.pushButton_deleteAllFeature.setStyleSheet("background-color: rgba(255, 0, 0, 70);\n"
"font: 75 20pt \"Ubuntu\";\n"
"border-radius:5px;\n"
"border-color:rgb(33, 148, 255);\n"
"border-width:1px;\n"
"border-style:solid;")
        self.pushButton_deleteAllFeature.setObjectName("pushButton_deleteAllFeature")

        self.retranslateUi(Frame_AddFGP)
        QtCore.QMetaObject.connectSlotsByName(Frame_AddFGP)

    def retranslateUi(self, Frame_AddFGP):
        _translate = QtCore.QCoreApplication.translate
        Frame_AddFGP.setWindowTitle(_translate("Frame_AddFGP", "Frame"))
        self.label_ThemVanTayThiSinh.setText(_translate("Frame_AddFGP", "THÊM VÂN TAY CHO THÍ SINH"))
        self.label_forShowAnoument.setText(_translate("Frame_AddFGP", "ĐẶT TAY LÊN CẢM BIẾN"))
        self.label.setText(_translate("Frame_AddFGP", "Số vân tay đã thêm:"))
        self.label_numberFGPadded.setText(_translate("Frame_AddFGP", "0"))
        self.pushButton_addFGP.setText(_translate("Frame_AddFGP", "+"))
        self.pushButton_deleteAllFeature.setText(_translate("Frame_AddFGP", "-"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame_AddFGP = QtWidgets.QFrame()
    ui = Ui_Frame_AddFGP()
    ui.setupUi(Frame_AddFGP)
    Frame_AddFGP.show()
    sys.exit(app.exec_())
