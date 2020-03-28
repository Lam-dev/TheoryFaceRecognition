import json
def SaveSystemSetting(settingDict):
    with open('../Setting/systemSetting.json', 'w') as json_file:
        json.dump(settingDict, json_file)