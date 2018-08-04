'''
用于获取各项考勤数据的类
BY LEO 2018-8-3
'''

import requests
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

class AttendanceUtil():
    '考勤工具类'

    # 常量
    __API_URL = 'https://oapi.dingtalk.com/'    # 接口域名
    __API_GETTOKEN = 'gettoken'                   # API - 获取accesstoken的api
    __API_DEPARTMENT_LIST_IDS = 'department/list_ids' # API - 获取部门id列表的api
    __PARAM_CORPID = 'corpid'                     # CORP_ID     参数名称
    __PARAM_CORPSECRET = 'corpsecret'             # CORP_SECRET 参数名称
    __PARAM_ACCESS_TOKEN = 'access_token'         # accesstoken 参数名称
    __PARAM_ID = 'id'                              # id 参数名称（父部门）
    __PARAM_DEPARTMENT_ID = 'department_id'        # department_id 参数名称（当前部门）
    __PARAM_SUB_DEPT_ID_LIST = 'sub_dept_id_list'

    # 变量
    __CORP_ID = ''        # CORP_ID 是公司识别码
    __CORP_SECRET = ''    # CORP_SECRET 钉钉应用的识别码
    __AccessToken = ''    # 访问口令

    '私有 - 拼接api地址的方法'
    def _getfinalAPI(self, api):
        return self.__API_URL + api

    '公有 - 刷新accessToken的方法'
    def refreshAccessToken(self):
        payload = {self.__PARAM_CORPID : self.__CORP_ID, self.__PARAM_CORPSECRET : self.__CORP_SECRET}
        response = requests.get(self._getfinalAPI(self.__API_GETTOKEN), params = payload)
        self.__AccessToken = response.json()[self.__PARAM_ACCESS_TOKEN]
        return

    '公有 - 读取accessToken的方法'
    def getAccessToken(self):
        return self.__AccessToken

    '公有 - 获取所有部门id的方法'
    def getDepartmentIds(self, fatherDepartment = 1):
        payload = {self.__PARAM_ACCESS_TOKEN : self.__AccessToken, self.__PARAM_ID : fatherDepartment}
        response = requests.get(self._getfinalAPI(self.__API_DEPARTMENT_LIST_IDS), params = payload)
        return response.json()[self.__PARAM_SUB_DEPT_ID_LIST]

    '公有 - 获取当前部门的所有用户的简单信息的方法'
    def getCurDepartmentUserSimpleInfo(self, department_id):
        payload = {self.__PARAM_ACCESS_TOKEN : self.__AccessToken, self.__PARAM_DEPARTMENT_ID : department_id}
        requests.get(self._getfinalAPI())

    '构造方法'
    def __init__(self, CORP_ID, CORP_SECRET):
        # 初始化两个识别码
        self.__CORP_ID = CORP_ID
        self.__CORP_SECRET = CORP_SECRET
        # 获取AccessToken
        self.refreshAccessToken()
        return




