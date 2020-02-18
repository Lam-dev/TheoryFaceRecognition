import threading
import time
import simpleaudio as sa
import wave
fileXinCamOnPath = 'Sound/AudioFile/xinCamOn.wav'
fileVuiLongThuLaiPath = 'Sound/AudioFile/vuiLongThuLai.wav'

class Sound():

    def __init__(self):
        self.waveXinCamOn = sa.WaveObject.from_wave_file(fileXinCamOnPath)
        self.waveVuiLongThuLai = sa.WaveObject.from_wave_file(fileVuiLongThuLaiPath)

    def __PlayXinCamOn(self):
        playSound = self.waveXinCamOn.play()
        playSound.wait_done()

    def __PlayVuiLongThuLai(self):
        playSound = self.waveVuiLongThuLai.play()
        playSound.wait_done()

    def ThreadPlayXinCamOn(self):
        thread = threading.Thread(target=self.__PlayXinCamOn, args=(), daemon=True)
        thread.start()

    def ThreadPlayVuiLongThuLai(self):
        thread = threading.Thread(target = self.__PlayVuiLongThuLai, args = (), daemon = True)
        thread.start()
