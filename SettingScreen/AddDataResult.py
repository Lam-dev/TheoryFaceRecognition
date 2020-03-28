from PyQt5                  import QtCore, QtGui, QtWidgets
from PyQt5                  import QtCore, QtGui, QtWidgets
from PyQt5.QtGui            import QIcon, QPixmap
from PyQt5.QtCore           import pyqtSlot, pyqtSignal,QTimer, QDateTime, Qt, QObject, QPointF, QPropertyAnimation, pyqtProperty
from SettingScreen.AddDataResultUI                  import Ui_Frame_containAddResult

class AddDataResults(QObject, Ui_Frame_containAddResult):
    SignalCloseResultDialog = pyqtSignal()
    def __init__(self, frameContain):
        Ui_Frame_containAddResult.__init__(self)
        QObject.__init__(self)
        self.setupUi(frameContain)
        frameContain.setGeometry((800-frameContain.width())/2, (480-frameContain.height())/2, frameContain.width(), frameContain.height())
        self.timerCloseResultsDialog = QTimer(self)
        self.timerCloseResultsDialog.timeout.connect(self.SignalCloseResultDialog.emit)

    def ShowDialog(self, success = False, addFace = False, addFGP = False):
        if(success):
            self.label_showIcon.setPixmap(QtGui.QPixmap("icon/iconOk.png"))
        
        if(addFace):
            self.label_addFaceEncodeResuls.setText("Thêm khuôn mặt thành công")
        
        if(addFGP):
            self.label_addFGPresult.setText("Thêm vân tay thành công")
        
        self.timerCloseResultsDialog.start(3000)

        