# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CaiDatIPtinh.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(410, 291)
        Frame.setStyleSheet("background-color: rgb(221, 221, 221);\n"
"border-style: solid;\n"
"border-radius:5px;")
        Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label = QtWidgets.QLabel(Frame)
        self.label.setGeometry(QtCore.QRect(10, 20, 111, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Frame)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 111, 17))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Frame)
        self.label_3.setGeometry(QtCore.QRect(10, 100, 111, 17))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Frame)
        self.label_4.setGeometry(QtCore.QRect(10, 140, 111, 17))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Frame)
        self.label_5.setGeometry(QtCore.QRect(10, 180, 111, 17))
        self.label_5.setObjectName("label_5")
        self.lineEdit_ip = QtWidgets.QLineEdit(Frame)
        self.lineEdit_ip.setGeometry(QtCore.QRect(130, 10, 221, 31))
        self.lineEdit_ip.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-style:solid;\n"
"border-radius:3px;\n"
"font: 75 bold 14pt \"Ubuntu\";")
        self.lineEdit_ip.setText("")
        self.lineEdit_ip.setObjectName("lineEdit_ip")
        self.lineEdit_subnetMask = QtWidgets.QLineEdit(Frame)
        self.lineEdit_subnetMask.setGeometry(QtCore.QRect(130, 50, 221, 31))
        self.lineEdit_subnetMask.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-style:solid;\n"
"border-radius:3px;\n"
"font: 75 bold 14pt \"Ubuntu\";")
        self.lineEdit_subnetMask.setText("")
        self.lineEdit_subnetMask.setObjectName("lineEdit_subnetMask")
        self.lineEdit_gateWay = QtWidgets.QLineEdit(Frame)
        self.lineEdit_gateWay.setGeometry(QtCore.QRect(130, 90, 221, 31))
        self.lineEdit_gateWay.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-style:solid;\n"
"border-radius:3px;\n"
"font: 75 bold 14pt \"Ubuntu\";")
        self.lineEdit_gateWay.setText("")
        self.lineEdit_gateWay.setObjectName("lineEdit_gateWay")
        self.lineEdit_preDNSeDNS = QtWidgets.QLineEdit(Frame)
        self.lineEdit_preDNSeDNS.setGeometry(QtCore.QRect(130, 130, 221, 31))
        self.lineEdit_preDNSeDNS.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-style:solid;\n"
"border-radius:3px;\n"
"font: 75 bold 14pt \"Ubuntu\";")
        self.lineEdit_preDNSeDNS.setText("")
        self.lineEdit_preDNSeDNS.setObjectName("lineEdit_preDNSeDNS")
        self.lineEdit_alterDNSalterDNS = QtWidgets.QLineEdit(Frame)
        self.lineEdit_alterDNSalterDNS.setGeometry(QtCore.QRect(130, 170, 221, 31))
        self.lineEdit_alterDNSalterDNS.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-style:solid;\n"
"border-radius:3px;\n"
"font: 75 bold 14pt \"Ubuntu\";")
        self.lineEdit_alterDNSalterDNS.setText("")
        self.lineEdit_alterDNSalterDNS.setObjectName("lineEdit_alterDNSalterDNS")
        self.pushButton_saveAndRestartaveAndRestart = QtWidgets.QPushButton(Frame)
        self.pushButton_saveAndRestartaveAndRestart.setGeometry(QtCore.QRect(190, 220, 131, 41))
        self.pushButton_saveAndRestartaveAndRestart.setStyleSheet("background-color: rgb(0, 170, 255);\n"
"border-radius:3px;\n"
"border-style:solid")
        self.pushButton_saveAndRestartaveAndRestart.setObjectName("pushButton_saveAndRestartaveAndRestart")
        self.pushButton_exit = QtWidgets.QPushButton(Frame)
        self.pushButton_exit.setGeometry(QtCore.QRect(330, 220, 71, 41))
        self.pushButton_exit.setStyleSheet("background-color: rgb(255, 123, 125);\n"
"border-radius:3px;\n"
"border-style:solid")
        self.pushButton_exit.setObjectName("pushButton_exit")
        self.label_6 = QtWidgets.QLabel(Frame)
        self.label_6.setGeometry(QtCore.QRect(10, 210, 171, 61))
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.label_iconCheckIP = QtWidgets.QLabel(Frame)
        self.label_iconCheckIP.setGeometry(QtCore.QRect(370, 10, 23, 29))
        self.label_iconCheckIP.setText("")
        self.label_iconCheckIP.setPixmap(QtGui.QPixmap("../../../../../../../../icon/iconCheckFail.png"))
        self.label_iconCheckIP.setObjectName("label_iconCheckIP")
        self.label_iconCheckSubnetMaskubnetMask = QtWidgets.QLabel(Frame)
        self.label_iconCheckSubnetMaskubnetMask.setGeometry(QtCore.QRect(370, 50, 23, 29))
        self.label_iconCheckSubnetMaskubnetMask.setText("")
        self.label_iconCheckSubnetMaskubnetMask.setPixmap(QtGui.QPixmap("../../../../../../../../icon/iconCheckFail.png"))
        self.label_iconCheckSubnetMaskubnetMask.setObjectName("label_iconCheckSubnetMaskubnetMask")
        self.label_iconCheckGateway = QtWidgets.QLabel(Frame)
        self.label_iconCheckGateway.setGeometry(QtCore.QRect(370, 90, 23, 29))
        self.label_iconCheckGateway.setText("")
        self.label_iconCheckGateway.setPixmap(QtGui.QPixmap("../../../../../../../../icon/iconCheckFail.png"))
        self.label_iconCheckGateway.setObjectName("label_iconCheckGateway")
        self.label_iconCheckDNS1 = QtWidgets.QLabel(Frame)
        self.label_iconCheckDNS1.setGeometry(QtCore.QRect(370, 130, 23, 29))
        self.label_iconCheckDNS1.setText("")
        self.label_iconCheckDNS1.setPixmap(QtGui.QPixmap("../../../../../../../../icon/iconCheckFail.png"))
        self.label_iconCheckDNS1.setObjectName("label_iconCheckDNS1")
        self.label_iconCheckDNS2 = QtWidgets.QLabel(Frame)
        self.label_iconCheckDNS2.setGeometry(QtCore.QRect(370, 170, 23, 29))
        self.label_iconCheckDNS2.setText("")
        self.label_iconCheckDNS2.setPixmap(QtGui.QPixmap("../../../../../../../../icon/iconCheckFail.png"))
        self.label_iconCheckDNS2.setObjectName("label_iconCheckDNS2")

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.label.setText(_translate("Frame", "IP:"))
        self.label_2.setText(_translate("Frame", "Subnet Mask:"))
        self.label_3.setText(_translate("Frame", "Gateway:"))
        self.label_4.setText(_translate("Frame", "Pre DNS:"))
        self.label_5.setText(_translate("Frame", "Alter DNS:"))
        self.pushButton_saveAndRestartaveAndRestart.setText(_translate("Frame", "Lưu"))
        self.pushButton_exit.setText(_translate("Frame", "Hủy"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame = QtWidgets.QFrame()
    ui = Ui_Frame()
    ui.setupUi(Frame)
    Frame.show()
    sys.exit(app.exec_())
