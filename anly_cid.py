# coding=utf-8
import hashlib
import hmac
import base64
import time
import requests
import json
import sys
# 测试环境
# 40a273f661bd4850f9f9790914950eea
# 23ca2f3bce44385b4eb740a302318288

clientId = '40a273f661bd4850f9f9790914950eea'
key = '23ca2f3bce44385b4eb740a302318288'
url = 'http://rnd-codedex-api.huawei.com/apiCenter/api/v1/defect/getDefectsDetail'
url2 = 'http://rnd-codedex-api.huawei.com/apiCenter/api/v2/defect/getAllDefectsBaseInfo'
# 生产环境
# clientId = ''
# key = ''
# url = 'http://rnd-codedex-api.huawei.com/apiCenter/api/v1/defect/getAllDefects'


timestamp = str(int(time.time() * 1000))



#获取cid
def cid_get_sign():
    msg = "clientId=" + clientId + "&key=" + key + "&timestamp=" + timestamp + '&uri=/api/v2/defect/getAllDefectsBaseInfo'
    m = hmac.new(bytes(key, 'utf-8'), bytes(msg, 'utf-8'), hashlib.sha1).digest()
    #print("MSG---------" + msg)
    return base64.b64encode(m)


def cid_get_headers(sign):
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
    return NewID
    
    
def cid_send():
    sign = cid_get_sign()
    #print("sign--------------", sign)
    headers = cid_get_headers(sign)
    data = {
        "projectName": "hw_liteos_Hi3556v200_CodeDEX",
        "pageSpec": {
            "pageSize": 5000,
            "startIndex": 0
        }
    }

    response = requests.post(url=url2, data=json.dumps(data), headers=headers)
    print("response:", response)
    content = response.json()
    NewID = get_AllCid(content)
    return NewID




#PART 2
def get_sign():
    msg = "clientId=" + clientId + "&key=" + key + "&timestamp=" + timestamp + '&uri=/api/v1/defect/getDefectsDetail'
    m = hmac.new(bytes(key, 'utf-8'), bytes(msg, 'utf-8'), hashlib.sha1).digest()
    #print("MSG---------" + msg)
    return base64.b64encode(m)


def get_headers(sign):
    headers = {
        "clientId": clientId,
        #'uri': '/api/v1/defect/getAllDefects',
        'uri':'/api/v1/defect/getDefectsDetail',
        "timestamp": timestamp,
        "sign": sign,
        "Content-Type": "application/json",
        "charset": "UTF-8"
    }
    return headers

    
def get_cid():
    f = open("/usr1/jenkins/jenkinsSlave/workspace/LiteOS_Main_Job/hw_liteos_inc_codedex/hw_liteos_Hi3556v200_CodeDEX.txt", 'r')
    content = f.read()
    f.close()
    return content
    
   
def main():
    new_cid = []
    
    old_list = []
    old_content = get_cid()
    old_content = old_content.split(' ')
    old_content.pop(-1)

    for i in old_content:
        old_list.append(int(i))
    
    NewID = cid_send()
    print('old_list')
    print(old_list)
    print('NewID')
    print(NewID)
    if set(old_list) == set(NewID):
        print('没有新增状态为new的告警')
    elif len(set(old_list)) >= len(set(NewID)):
        print('没有新增状态为new的告警')
    else:
        print('有新增状态为new的告警')
        len_num = len(NewID) - len(old_list)
        for i in range(len_num):
            new_cid.append(NewID[-i])
    
    #sign = get_sign()
    
    # headers = get_headers(sign)
    # data = {
        # "projectName": "hw_liteos_Hi3556v200_CodeDEX",
        # "cids":new_cid,

        # }
    # response = requests.post(url=url, data=json.dumps(data), headers=headers).json()
    
    #整理邮件数据
        codex_url_list = []
        for i in new_cid:
            codex_url = "https://rnd-secsolar.huawei.com/portal/workspace/projectDefectsView?projectName=hw_liteos_Hi3556v200_CodeDEX&cid={}&curCid={}&curTool=All&count=50&currentPage=1".format(i,i)
            codex_url_list.append(codex_url)
            
        print(codex_url_list)
        
        print(sys.argv[1])
        
        print(new_cid)
        
        f = open("report.txt", "w")
        for i in range(len(new_cid)):
            f.write('新增告警CID：' + str(new_cid[i-0]) + '\n')
            f.write('codex详情页面: ' + codex_url_list[i-0] + '\n')
            f.write('工程jenkins链接: ' + sys.argv[1] + '\n')
        f.close()
        
        f = open("log.txt", "a+")
        f.write('此提交为：' + sys.argv[2] +  '  新增告警CID：' + str(new_cid) + '\n')
        f.close()
        sys.exit(1)
    
if __name__ == '__main__':
    main()







