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
        Frame_AddFGP.setStyleSheet("background-color: rgb(255, 255, 255);")
        Frame_AddFGP.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Frame_AddFGP.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_ThemVanTayThiSinh = QtWidgets.QLabel(Frame_AddFGP)
        self.label_ThemVanTayThiSinh.setGeometry(QtCore.QRect(70, 6, 335, 33))
        self.label_ThemVanTayThiSinh.setStyleSheet("color: rgb(29, 29, 29);\n"
"font: 57 bold 16pt \"Ubuntu\";")
        self.label_ThemVanTayThiSinh.setObjectName("label_ThemVanTayThiSinh")
        self.label_forShowIconAddFingerPrint = QtWidgets.QLabel(Frame_AddFGP)
        self.label_forShowIconAddFingerPrint.setGeometry(QtCore.QRect(102, 50, 287, 209))
        self.label_forShowIconAddFingerPrint.setObjectName("label_forShowIconAddFingerPrint")
        self.label_forShowAnoument = QtWidgets.QLabel(Frame_AddFGP)
        self.label_forShowAnoument.setGeometry(QtCore.QRect(60, 264, 375, 41))
        self.label_forShowAnoument.setStyleSheet("color: rgb(216, 0, 0);\n"
"font: 75 bold 14pt \"Ubuntu\";")
        self.label_forShowAnoument.setObjectName("label_forShowAnoument")
        self.label_skipAddFGP = QtWidgets.QLabel(Frame_AddFGP)
        self.label_skipAddFGP.setGeometry(QtCore.QRect(394, 308, 85, 31))
        self.label_skipAddFGP.setObjectName("label_skipAddFGP")

        self.retranslateUi(Frame_AddFGP)
        QtCore.QMetaObject.connectSlotsByName(Frame_AddFGP)

    def retranslateUi(self, Frame_AddFGP):
        _translate = QtCore.QCoreApplication.translate
        Frame_AddFGP.setWindowTitle(_translate("Frame_AddFGP", "Frame"))
        self.label_ThemVanTayThiSinh.setText(_translate("Frame_AddFGP", "THÊM VÂN TAY CHO THÍ SINH"))
        self.label_forShowIconAddFingerPrint.setText(_translate("Frame_AddFGP", "TextLabel"))
        self.label_forShowAnoument.setText(_translate("Frame_AddFGP", "ĐẶT TAY LÊN CẢM BIẾN"))
        self.label_skipAddFGP.setText(_translate("Frame_AddFGP", "Bỏ qua"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame_AddFGP = QtWidgets.QFrame()
    ui = Ui_Frame_AddFGP()
    ui.setupUi(Frame_AddFGP)
    Frame_AddFGP.show()
    sys.exit(app.exec_())
