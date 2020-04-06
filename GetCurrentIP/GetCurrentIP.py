import netifaces
class GetCurrentIp():

    def __init__(self):
        pass
    def GetIP(self):
        lstInterface = netifaces.interfaces()
        privateIP = False
        gateway = False
        subnetMask = False
        for inter in lstInterface:
            try:
                ip = netifaces.ifaddresses(inter)[2][0]['addr']
                if(self.IsIPv4(ip)):
                    privateIP = ip
                    gateway = self.GetGateway()
                    subnetMask = netifaces.ifaddresses(inter)[2][0]['netmask']
                    break
            except Exception as ex:
                print(ex)
                pass
        
        dict = {
            "privateIP":privateIP,
            "gateway":gateway,
            "subnetMask":subnetMask,
        }
        print(dict)


    def GetGateway(self):
        try:
            gateway = netifaces.gateways()['default'][2][0]
            if(self.IsIPv4(gateway)):
                return gateway
            else:
                return False
        except:
            return False


    def IsIPv4(self, ip):
        if(ip == "127.0.0.1"):
            return False
        if(self.__CheckIPrule):
            return True

        else:
            return False
        

    def __CheckIPrule(self, ipText, labelForShowIcon):
        try:
            ipArr = ipText.split(".")
            if(len(ipArr) == 4):
                for number in ipArr:
                    if(not self.__CheckNumberRule(number)):
                        return False
                return True
            else:
                return False
        except:
            return False

        
    def __CheckNumberRule(self, numberText):

        try:
            intNumber = int(numberText)
            if((intNumber >= 0) & (intNumber <= 255)):
                return True
            else:
                return False
        except:
            return False

crIp = GetCurrentIp()
