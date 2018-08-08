"""
用于获取各项考勤数据的类
BY LEO 2018-8-3
"""

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


class AttendanceUtil:

    # 常量
    __API_URL = 'https://oapi.dingtalk.com/'             # 接口域名
    __API_GETTOKEN = 'gettoken'                          # API - 获取access token的api
    __API_DEPARTMENT_LIST_IDS = 'department/list_ids'    # API - 获取部门id列表的api
    __API_USER_SIMPLELIST = 'user/simplelist'            # API - 获取部门人员简单信息的api
    __API_ATTENDANCE_LIST = 'attendance/list'            # API - 获取考勤信息

    __PARAM_CORPID = 'corpid'                            # PARAM - CORPID 参数名称
    __PARAM_CORPSECRET = 'corpsecret'                    # PARAM - CORPSECRET 参数名称
    __PARAM_ACCESS_TOKEN = 'access_token'                # PARAM - access token 参数名称
    __PARAM_ID = 'id'                                    # PARAM - id 参数名称（父部门）
    __PARAM_DEPARTMENT_ID = 'department_id'              # PARAM - department_id 参数名称（当前部门）

    __JSON_PARAM_SUB_DEPT_ID_LIST = 'sub_dept_id_list'   # JSON_PARAM - 参数名称（部门列表）
    __JSON_USERLIST = 'userlist'                         # JSON_PARAM - 参数名称（用户简单列表）
    __JSON_USERIDS = 'userIds'                           # JSON_PARAM - 用户ID列表
    __JSON_WORK_DATE_FROM = 'workDateFrom'               # JSON_PARAM - 考勤开始时间
    __JSON_WORK_DATE_TO = 'workDateTo'                   # JSON_PARAM - 考勤结束时间
    __JSON_RECORD_RESULT = 'recordresult'                # JSON_PARAM - 考勤结果
    __JSON_HAS_MORE = 'hasMore'                          # JSON_PARAM - 表明是否还有更多考勤数据
    __JSON_OFFSET = 'offset'                             # JSON_PARAM - 考勤结果读取偏移量
    __JSON_LIMIT = 'limit'                               # JSON_PARAM - 一次读取的结果条数


    # 变量
    __CORP_ID = ''        # CORP_ID 是公司识别码
    __CORP_SECRET = ''    # CORP_SECRET 钉钉应用的识别码
    __AccessToken = ''    # 访问口令

    # HTTP请求常量
    __HTTP_CONTENT_TYPE = 'Content-Type'
    __HTTP_CONTENT_TYPE_JSON = 'application/json'

    __HTTP_CONTENT_ENCODING = 'Content-encoding'
    __HTTP_CONTENT_ENCODING_UTF8 = 'UTF8'

    '私有 - 拼接api地址的方法'
    def _getfinalAPI(self, api):
        return self.__API_URL + api

    '私有 - 拼接api地址的方法POST'
    def _getfinalAPI_post(self, api):
        return self.__API_URL + api + '?access_token=' + self.__AccessToken

    '公有 - 刷新accessToken的方法'
    def refreshAccessToken(self):
        payload = {self.__PARAM_CORPID: self.__CORP_ID, self.__PARAM_CORPSECRET: self.__CORP_SECRET}
        response = requests.get(self._getfinalAPI(self.__API_GETTOKEN), params=payload)
        self.__AccessToken = response.json()[self.__PARAM_ACCESS_TOKEN]
        return

    '公有 - 读取accessToken的方法'
    def getAccessToken(self):
        return self.__AccessToken

    '公有 - 获取所有部门id的方法'
    def getDepartmentIds(self, fatherDepartment = 1):
        payload = {self.__PARAM_ACCESS_TOKEN: self.__AccessToken, self.__PARAM_ID: fatherDepartment}
        response = requests.get(self._getfinalAPI(self.__API_DEPARTMENT_LIST_IDS), params=payload)
        return response.json()[self.__JSON_PARAM_SUB_DEPT_ID_LIST]

    '公有 - 获取当前部门的所有用户的简单信息的方法'
    def getCurDepartmentUserSimpleInfo(self, department_id):
        payload = {self.__PARAM_ACCESS_TOKEN: self.__AccessToken, self.__PARAM_DEPARTMENT_ID: department_id}
        response = requests.get(self._getfinalAPI(self.__API_USER_SIMPLELIST), params=payload)
        return response.json()[self.__JSON_USERLIST]

    '公有 - 获取用户考勤信息的方法'
    def getUserAttendanceInfo(self, userIdList, beginTime, endTime):
        """userList不得超过50个"""
        """开始时间和结束时间间隔最大为7天"""
        headers = {self.__HTTP_CONTENT_TYPE: self.__HTTP_CONTENT_TYPE_JSON,
                   self.__HTTP_CONTENT_ENCODING: self.__HTTP_CONTENT_ENCODING_UTF8}
        """循环读取考勤结果"""
        offset = 0
        limit = 50
        response = []
        while True:
            data = {self.__JSON_WORK_DATE_FROM: beginTime,
                    self.__JSON_WORK_DATE_TO: endTime,
                    self.__JSON_USERIDS: userIdList,
                    self.__JSON_OFFSET: offset,
                    self.__JSON_LIMIT: limit}
            r = requests.post(self._getfinalAPI_post(self.__API_ATTENDANCE_LIST),
                                     headers=headers,
                                     json=data)
            response.extend(r.json()[self.__JSON_RECORD_RESULT])
            offset += limit
            if r.json()[self.__JSON_HAS_MORE] is False:
                break
        return response

    '构造方法'
    def __init__(self, corp_id, corp_secret):
        # 初始化两个识别码
        self.__CORP_ID = corp_id
        self.__CORP_SECRET = corp_secret
        # 获取AccessToken
        self.refreshAccessToken()
        return




