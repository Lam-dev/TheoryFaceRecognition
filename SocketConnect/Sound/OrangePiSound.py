import threading
import time
import simpleaudio as sa
import wave
from    PyQt5.QtCore   import QTimer, QObject
fileXinCamOnPath = 'Sound/AudioFile/xinCamOn.wav'
fileVuiLongThuLaiPath = 'Sound/AudioFile/vuiLongThuLai.wav'
fileTemp = 'Sound/AudioFile/temp.wav'

class Sound(QObject):

    def __init__(self):
        QObject.__init__(self)
        self.waveXinCamOn = sa.WaveObject.from_wave_file(fileXinCamOnPath)
        self.waveVuiLongThuLai = sa.WaveObject.from_wave_file(fileVuiLongThuLaiPath)
        self.waveTemp = sa.WaveObject.from_wave_file(fileTemp)
        self.ThreadPlayTemp()
        self.timerPlayTemp = QTimer(self)
        self.timerPlayTemp.start(240000)
        self.timerPlayTemp.timeout.connect(self.ThreadPlayTemp)


    def __PlayTemp(self):
        playSound = self.waveTemp.play()
        playSound.wait_done()

    def ThreadPlayTemp(self):
        thread = threading.Thread(target=self.__PlayTemp, args=(), daemon=True)
        thread.start()

    def __PlayXinCamOn(self):
        playSound = self.waveXinCamOn.play()
        playSound.wait_done()

    def __PlayVuiLongThuLai(self):
        
        playSound = self.waveVuiLongThuLai.play()
        playSound.wait_done()

    def ThreadPlayXinCamOn(self):
        self.timerPlayTemp.stop()
        self.timerPlayTemp.start(240000)
        thread = threading.Thread(target=self.__PlayXinCamOn, args=(), daemon=True)
        thread.start()

    def ThreadPlayVuiLongThuLai(self):
        self.timerPlayTemp.stop()
        self.timerPlayTemp.start(240000)
        thread = threading.Thread(target = self.__PlayVuiLongThuLai, args = (), daemon = True)
        thread.start()
