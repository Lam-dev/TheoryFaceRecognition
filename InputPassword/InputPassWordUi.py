# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'InputAccount.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(374, 449)
        Frame.setStyleSheet("background-color: rgb(199, 199, 199);\n"
"")
        Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.pushButton_1 = QtWidgets.QPushButton(Frame)
        self.pushButton_1.setGeometry(QtCore.QRect(28, 96, 87, 79))
        self.pushButton_1.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 170, 127);\n"
"font: 75 bold 26pt \"Ubuntu\";")
        self.pushButton_1.setObjectName("pushButton_1")
        self.pushButton_2 = QtWidgets.QPushButton(Frame)
        self.pushButton_2.setGeometry(QtCore.QRect(136, 96, 87, 79))
        self.pushButton_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 170, 127);\n"
"font: 75 bold 26pt \"Ubuntu\";")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Frame)
        self.pushButton_3.setGeometry(QtCore.QRect(242, 96, 87, 79))
        self.pushButton_3.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 170, 127);\n"
"font: 75 bold 26pt \"Ubuntu\";")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(Frame)
        self.pushButton_4.setGeometry(QtCore.QRect(28, 184, 87, 79))
        self.pushButton_4.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 170, 127);\n"
"font: 75 bold 26pt \"Ubuntu\";")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(Frame)
        self.pushButton_5.setGeometry(QtCore.QRect(136, 184, 87, 79))
        self.pushButton_5.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 170, 127);\n"
"font: 75 bold 26pt \"Ubuntu\";")
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(Frame)
        self.pushButton_6.setGeometry(QtCore.QRect(242, 184, 87, 79))
        self.pushButton_6.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 170, 127);\n"
"font: 75 bold 26pt \"Ubuntu\";")
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(Frame)
        self.pushButton_7.setGeometry(QtCore.QRect(28, 272, 87, 79))
        self.pushButton_7.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 170, 127);\n"
"font: 75 bold 26pt \"Ubuntu\";")
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(Frame)
        self.pushButton_8.setGeometry(QtCore.QRect(136, 272, 87, 79))
        self.pushButton_8.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 170, 127);\n"
"font: 75 bold 26pt \"Ubuntu\";")
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_9 = QtWidgets.QPushButton(Frame)
        self.pushButton_9.setGeometry(QtCore.QRect(242, 272, 87, 79))
        self.pushButton_9.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 170, 127);\n"
"font: 75 bold 26pt \"Ubuntu\";")
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_OK = QtWidgets.QPushButton(Frame)
        self.pushButton_OK.setGeometry(QtCore.QRect(28, 364, 87, 79))
        self.pushButton_OK.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 170, 127);\n"
"font: 75 bold 26pt \"Ubuntu\";")
        self.pushButton_OK.setObjectName("pushButton_OK")
        self.pushButton_0 = QtWidgets.QPushButton(Frame)
        self.pushButton_0.setGeometry(QtCore.QRect(136, 364, 87, 79))
        self.pushButton_0.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 170, 127);\n"
"font: 75 bold 26pt \"Ubuntu\";")
        self.pushButton_0.setObjectName("pushButton_0")
        self.pushButton_del = QtWidgets.QPushButton(Frame)
        self.pushButton_del.setGeometry(QtCore.QRect(242, 364, 87, 79))
        self.pushButton_del.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 170, 127);\n"
"font: 75 bold 26pt \"Ubuntu\";")
        self.pushButton_del.setObjectName("pushButton_del")
        self.label_forShowNumber = QtWidgets.QLineEdit(Frame)
        self.label_forShowNumber.setGeometry(QtCore.QRect(10, 10, 351, 71))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(40)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(7)
        self.label_forShowNumber.setFont(font)
        self.label_forShowNumber.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 57 italic 40pt \"Ubuntu\";")
        self.label_forShowNumber.setInputMask("")
        self.label_forShowNumber.setMaxLength(6)
        self.label_forShowNumber.setEchoMode(QtWidgets.QLineEdit.Password)
        self.label_forShowNumber.setAlignment(QtCore.Qt.AlignCenter)
        self.label_forShowNumber.setObjectName("label_forShowNumber")

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.pushButton_1.setText(_translate("Frame", "1"))
        self.pushButton_2.setText(_translate("Frame", "2"))
        self.pushButton_3.setText(_translate("Frame", "3"))
        self.pushButton_4.setText(_translate("Frame", "4"))
        self.pushButton_5.setText(_translate("Frame", "5"))
        self.pushButton_6.setText(_translate("Frame", "6"))
        self.pushButton_7.setText(_translate("Frame", "7"))
        self.pushButton_8.setText(_translate("Frame", "8"))
        self.pushButton_9.setText(_translate("Frame", "9"))
        self.pushButton_OK.setText(_translate("Frame", "OK"))
        self.pushButton_0.setText(_translate("Frame", "0"))
        self.pushButton_del.setText(_translate("Frame", "DEL"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame = QtWidgets.QFrame()
    ui = Ui_Frame()
    ui.setupUi(Frame)
    Frame.show()
    sys.exit(app.exec_())
