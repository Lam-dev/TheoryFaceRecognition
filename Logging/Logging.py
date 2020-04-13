import logging, os

class Logging:
    def __init__(self):
        logging.basicConfig(filename='Logging/log.log',level=logging.DEBUG)

    def WriteLogToFile(self, str):
        logging.info(str)

    def ReadLog(self):
        with open('Logging/log.log') as f:
            while(True):
                line = f.readline()
                if(line.__len__() == 0):
                    os.remove('Logging/log.log')
                    return
                yield line
