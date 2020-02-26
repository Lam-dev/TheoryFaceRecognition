from    FingerPrintSensor.FingerprintLib    import PyFingerprint
import time           
fingerprintObj = PyFingerprint(port = '/dev/ttyACM0', baudRate = 57600, address = 0xFFFFFFFF, password = 0xFFFFFFFF)
fingerprintObj.deleteTemplate(1)
fingerprintObj.deleteTemplate(2)
# fingerprint = "4,6,93,0,173,106,134,146,130,24,254,223,209,50,134,23,65,250,195,254,54,243,135,32,1,200,123,255,97,211,135,152,1,216,121,231,109,203,136,150,2,249,193,239,98,188,135,146,65,248,59,248,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,18,33,22,83,88,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,224,28,255,255,255,255,255,255,255,255,255,255,255,255,255,255;4,17,80,0,82,154,134,11,74,86,199,253,85,42,135,122,200,103,242,15,114,2,135,129,9,86,236,215,181,114,133,94,135,118,246,31,242,218,132,210,132,246,9,248,22,27,134,228,202,136,143,230,70,43,136,142,198,69,176,168,157,99,134,89,136,184,118,215,162,195,135,134,204,120,236,136,242,219,134,91,138,219,48,136,254,27,134,211,134,152,211,231,34,36,133,72,197,70,254,31,53,196,135,47,149,76,255,225,73,44,135,91,219,12,63,248,86,100,135,65,37,45,191,192,109,4,133,188,133,245,199,248,118,124,133,67,68,85,254,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,166,82,53,132,36,65,104,100,98,84,99,130,73,50,65,35,177,35,20,83,82,69,86,50,83,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,81,136,150,2,249,193,239,98,188,135,146,65,248,59,248;4,7,92,0,38,186,134,34,134,248,121,248,105,34,133,167,196,167,63,255,113,74,133,42,3,248,247,231,149,242,133,161,196,184,63,239,134,227,132,153,65,198,63,248,150,59,134,148,129,218,5,0,154,211,135,148,132,248,1,239,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,68,54,98,38,66,120,115,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,13,34,132,210,132,246,9,248,22,27,134,228,202,136,143,230;4,5,110,0,114,138,136,90,196,254,251,255,142,2,135,213,2,11,126,255,157,90,135,94,65,250,193,239,114,107,133,217,194,62,120,255,121,180,135,213,195,248,251,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,34,178,49,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,84,25,132,153,65,198,63,248,150,59,134,148,129,218,5,0"
#fgpListStr = fingerprint.split(";")
# dem = 1;
# fingerprintObj.clearDatabase()
# for fgpList in fgpListStr:
#     fgpStr = fgpListStr[0].split(",")
#     fgp = [int(elem) for elem in fgpStr]   
#     print(fingerprintObj.uploadCharacteristics(0x01,fgp))
#     print(fingerprintObj.storeTemplate(1))
#     dem +=1
#     # pass

# for i in range (1,4):
#     fingerprintObj.loadTemplate(i,0x01)
#     feature = fingerprintObj.downloadCharacteristics(0x01)
#     print(feature)


# dem = 1
# while True:
#     try:
#         if(fingerprintObj.readImage()):
#             fingerprintObj.convertImage(0x01)
#             fingerprintObj.readImage()
#             fingerprintObj.convertImage(0x02)
#             if(fingerprintObj.compareCharacteristics() > 0):
#                 fingerprintObj.storeTemplate(dem)
#                 dem += 1
#     except:
#         pass


#     if(dem == 4):
#         break

while True:
    try:
        if(fingerprintObj.readImage()):
            fingerprintObj.convertImage(0x01)
            print(fingerprintObj.searchTemplate())
#             # char1 = fingerprintObj.downloadCharacteristics(0x01)
#             # print(char1)
#             # fingerprintObj.uploadCharacteristics(0x01, char1)
#             # fingerprintObj.storeTemplate(2, 0x01)
#             # break

#             # print(char1)
#             # pass
#             # print(fingerprintObj.searchTemplate())
#             # # # break;
#             # char2 = fingerprintObj.downloadCharacteristics(0x01)
#             # print(char2)
#             # print(char1 == char2)

#             # for i in range(0, 512):
#             #     print(str(char1[i])+"  "+str(char2[i]))
#             #     if(char1[i] != char2[i]):
#             #         print(str(i) + "   "+ str(char1[i]) + "   " + str(char2[i]))

    except :
        pass
