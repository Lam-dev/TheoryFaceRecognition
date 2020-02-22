# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WaitForUpdate.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame_ContainWaitForSync(object):
    def setupUi(self, Frame_ContainWaitForSync):
        Frame_ContainWaitForSync.setObjectName("Frame_ContainWaitForSync")
        Frame_ContainWaitForSync.resize(408, 188)
        Frame_ContainWaitForSync.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Frame_ContainWaitForSync.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label = QtWidgets.QLabel(Frame_ContainWaitForSync)
        self.label.setGeometry(QtCore.QRect(26, 54, 57, 67))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../icon/iconReadFace.png"))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Frame_ContainWaitForSync)
        self.label_2.setGeometry(QtCore.QRect(92, 52, 293, 67))
        self.label_2.setStyleSheet("font: 57 bold 16pt \"Ubuntu\";\n"
"color: rgb(0, 170, 127);")
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Frame_ContainWaitForSync)
        QtCore.QMetaObject.connectSlotsByName(Frame_ContainWaitForSync)

    def retranslateUi(self, Frame_ContainWaitForSync):
        _translate = QtCore.QCoreApplication.translate
        Frame_ContainWaitForSync.setWindowTitle(_translate("Frame_ContainWaitForSync", "Frame"))
        self.label_2.setText(_translate("Frame_ContainWaitForSync", "Đang đồng bộ dữ liệu"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame_ContainWaitForSync = QtWidgets.QFrame()
    ui = Ui_Frame_ContainWaitForSync()
    ui.setupUi(Frame_ContainWaitForSync)
    Frame_ContainWaitForSync.show()
    sys.exit(app.exec_())
