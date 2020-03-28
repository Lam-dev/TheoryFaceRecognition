# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'KetQuaThemDuLieu.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame_containAddResult(object):
    def setupUi(self, Frame_containAddResult):
        Frame_containAddResult.setObjectName("Frame_containAddResult")
        Frame_containAddResult.resize(398, 256)
        Frame_containAddResult.setStyleSheet("background-color: rgb(255, 255, 255);")
        Frame_containAddResult.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Frame_containAddResult.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_showIcon = QtWidgets.QLabel(Frame_containAddResult)
        self.label_showIcon.setGeometry(QtCore.QRect(166, 8, 67, 61))
        self.label_showIcon.setText("")
        self.label_showIcon.setObjectName("label_showIcon")
        self.label_addFGPresult = QtWidgets.QLabel(Frame_containAddResult)
        self.label_addFGPresult.setGeometry(QtCore.QRect(26, 90, 341, 31))
        self.label_addFGPresult.setObjectName("label_addFGPresult")
        self.label_addFaceEncodeResuls = QtWidgets.QLabel(Frame_containAddResult)
        self.label_addFaceEncodeResuls.setGeometry(QtCore.QRect(26, 126, 339, 33))
        self.label_addFaceEncodeResuls.setObjectName("label_addFaceEncodeResuls")

        self.retranslateUi(Frame_containAddResult)
        QtCore.QMetaObject.connectSlotsByName(Frame_containAddResult)

    def retranslateUi(self, Frame_containAddResult):
        _translate = QtCore.QCoreApplication.translate
        Frame_containAddResult.setWindowTitle(_translate("Frame_containAddResult", "Frame"))
        self.label_addFGPresult.setText(_translate("Frame_containAddResult", "TextLabel"))
        self.label_addFaceEncodeResuls.setText(_translate("Frame_containAddResult", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame_containAddResult = QtWidgets.QFrame()
    ui = Ui_Frame_containAddResult()
    ui.setupUi(Frame_containAddResult)
    Frame_containAddResult.show()
    sys.exit(app.exec_())
