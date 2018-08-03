'自动生成考勤日报并发布到微信群中'

import CONFIGS
import requests
import json
"**********************************README**************************************"
'-API调用须知-'
'调用API前需获取Access_Token'
'Access_Token有效期为7200秒，到期请重新获取，未到期重新获取将自动续期'

'当企业应用服务调用钉钉开放平台接口时'
'需使用https协议、Json数据格式、UTF8编码'
'域名为https://oapi.dingtalk.com'
'POST请求请在HTTP Header中设置 Content-Type:application/json，否则接口调用失败'
'*/LEO 2018.7.30/'
'******************************************************************************'

'********************************常量配置***************************************'
'CORP_ID 是公司识别码'
CORP_ID = "dingc7fb31db15999b4435c2f4657eb6378f"

'CORP_SECRET 钉钉中考勤日报这个应用的识别码'
CORP_SECRET = "FWGnzL06BnOh8S7vOctAYgvSumOuxQpE7Bc6wqdwCc4qdyP2uSRO0w7C9ggstocO"

'接口域名'
URL = 'https://oapi.dingtalk.com/'
'*******************************************************************************'

'******函数*******'
def getAPI_URL(api):
    return URL + api
'*****************'

print('开始获取access_token')
'构建GET请求参数'
payload = {'corpid' : CORP_ID, 'corpsecret' : CORP_SECRET}
'发起GET请求'
response = requests.get(getAPI_URL('gettoken'), params = payload)
print('access_token获取结果:' + response.text)
dict_response = response.json()
'提取AccessToken'
access_token = dict_response['access_token']
print('解析得到access_token: '  + access_token)

print('开始获取部门id_list')
payload = {'access_token' : access_token, 'id' : '1'}
response = requests.get(getAPI_URL('department/list_ids'), params=payload)
print('部门id获取结果')
dict_response = response.json()
dapartment_listIds = dict_response['sub_dept_id_list']
print(dapartment_listIds)

userLists = []
for dapartment_id in dapartment_listIds:
    payload = {'access_token' : access_token, 'department_id' : dapartment_id}
    response = requests.get(getAPI_URL('user/simplelist'),params=payload)
    userList = (response.json())['userlist']
    userLists = userLists + userList

print(userLists)