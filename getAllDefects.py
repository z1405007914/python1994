# coding=utf-8
import hashlib
import hmac
import base64
import time
import requests
import json

# 测试环境
# 40a273f661bd4850f9f9790914950eea
# 23ca2f3bce44385b4eb740a302318288

clientId = '40a273f661bd4850f9f9790914950eea'
key = '23ca2f3bce44385b4eb740a302318288'
url = 'http://rnd-codedex-api.huawei.com/apiCenter/api/v2/defect/getAllDefectsBaseInfo'

# 生产环境
# clientId = ''
# key = ''
# url = 'http://rnd-codedex-api.huawei.com/apiCenter/api/v1/defect/getAllDefects'


timestamp = str(int(time.time() * 1000))
#print(timestamp)


def get_sign():
    msg = "clientId=" + clientId + "&key=" + key + "&timestamp=" + timestamp + '&uri=/api/v2/defect/getAllDefectsBaseInfo'
    m = hmac.new(bytes(key, 'utf-8'), bytes(msg, 'utf-8'), hashlib.sha1).digest()
    #print("MSG---------" + msg)
    return base64.b64encode(m)


def get_headers(sign):
    headers = {
        "clientId": clientId,
        #'uri': '/api/v1/defect/getAllDefects',
        'uri':'/api/v2/defect/getAllDefectsBaseInfo',
        "timestamp": timestamp,
        "sign": sign,
        "Content-Type": "application/json",
        "charset": "UTF-8"
    }
    return headers

# 获取所有new状态的告警CID   
def get_AllCid(response):
    NewID = []
    AllInfo = response['result']['defects']
    for info in AllInfo:
        if info['defectStatus'] == 'New':
            NewID.append(info['defectId'])
    save_cid(NewID)
    
    
def save_cid(NewID):
    f = open("hw_liteos_Hi3556v200_CodeDEX.txt", "w")
    for i in NewID:
        f.write(str(i)+' ')
    f.close()
    
def send():
    sign = get_sign()
    #print("sign--------------", sign)
    headers = get_headers(sign)
    data = {
        "projectName": "hw_liteos_Hi3556v200_CodeDEX",
        "pageSpec": {
            "pageSize": 5000,
            "startIndex": 0
        }
    }

    response = requests.post(url=url, data=json.dumps(data), headers=headers)
    print("response:", response)
    content = response.json()
    get_AllCid(content)
    


if __name__ == '__main__':
    send()







