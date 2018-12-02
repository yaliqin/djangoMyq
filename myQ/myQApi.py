from constants import Const
import requests

class MyQAPI:

    securityToken = 0
    #   get the user name and pwd and login
    def _init_(self, usr, pwd):
        self.usr = usr
        self.pwd = pwd

    def login(self):
        h = {"MyQApplicationId":Const.appId}
        para = {"username":self.usr, "password":self.pwd}
        login_url = Const.endpoint+'/api/v4/User/Validate'
        r=requests.post(login_url,data=para, headers=h)
        if r.status_code == 200: #Get the right response
            json_data = r.json()
            MyQAPI.securityToken = json_data['SecurityToken']
        else:
            return Const.errorMessages['13']

    #   get devices list
    def getDevices(self):
        appid = Const.appId
        h = {"MyQApplicationId":appid, "securityToken":MyQAPI.securityToken}
        get_devices_id_url =Const.endpoint+'/api/v4/userdevicedetails/get'
        r = requests.get(get_devices_id_url, headers=h)
        if r.status_code == 200:
            json_data=r.json()
            devices_info = json_data["Devices"]
            devices =[]
            for item in devices_info:
                device = (item['MyQDeviceId'],item["MyQDeviceTypeId"], item["MyQDeviceTypeName"], item['Attributes'])
                devices.append(device)
        return devices


    ########
    # get all devices id and return the doors' id
    def get_door_info(self):
        devices_info = self.getDevices()
        doorId ={}
        doorName ={}
        doorState ={}
        doorInfo=[]

        for item in devices_info:
            #   devices_info has the key field as deviceId,deviceTypeId, deviceTypeName,attributes
            if item[1] == Const.MyQDeviceTypeName['GarageDoorOpener']:
                doorId =item[0]
                for attribute in item[3]:
                    if(attribute['AttributeDisplayName'] == 'doorstate'):
                        doorState = attribute['Value']
                    if(attribute['AttributeDisplayName'] == 'desc'):
                        doorName = attribute['Value']
                doorInfo.append([doorId,doorName,doorState])
        return doorInfo

    # set device state. e.g. close the door
    def setDeviceState(self, attributeName,attributeValue,deviceId):
        h ={"MyQApplicationId": Const.appId, "SecurityToken": MyQAPI.securityToken}
        url = Const.endpoint+'/api/v4/deviceattribute/putdeviceattribute'
        payload ={"MyQDeviceId": deviceId,"AttributeName": attributeName,"AttributeValue": attributeValue}
        r=requests.put(url,headers=h,data=payload)

        if(r.status_code==200):
            print('Set state successfully')
            return r
        else:
            print('Set state failed')
