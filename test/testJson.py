import json
import codecs

with open("DataUpdate/TTND_2020_02_19_CN.json", encoding='utf-8-sig') as json_file:
    jsonDict = json.load(json_file)


print(jsonDict["ID"])