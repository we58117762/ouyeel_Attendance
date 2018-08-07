'自动生成考勤日报并发布到微信群中'

import time
from AttendanceUtil import AttendanceUtil
import requests


'********************************常量配置***************************************'
'CORP_ID 是公司识别码'
CORP_ID = "dingc7fb31db15999b4435c2f4657eb6378f"

'CORP_SECRET 钉钉中考勤日报这个应用的识别码'
CORP_SECRET = "FWGnzL06BnOh8S7vOctAYgvSumOuxQpE7Bc6wqdwCc4qdyP2uSRO0w7C9ggstocO"

#BEGIN_TIME = time.strftime("%Y-%m-%d 00:00:00", time.localtime())
#END_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

BEGIN_TIME = "2018-08-06 00:00:00"
END_TIME = "2018-08-06 23:59:59"

'*******************************************************************************'
print(BEGIN_TIME)
print(END_TIME)

def getUniquList(unUniqueList):
    uniqueList = []
    for element in unUniqueList:
        if element not in uniqueList:
            uniqueList.append(element)
    return uniqueList


ouyeelAttendance = AttendanceUtil(CORP_ID, CORP_SECRET)
print('\n①获取ACCSESS_TOKEN:')
print(ouyeelAttendance.getAccessToken())

'获取公司所有部门'
departmentIdList = ouyeelAttendance.getDepartmentIds()
print('\n②获取所有部门ID: ')
print(departmentIdList)

'获取每个部门下的员工合集'
userSimpleInfoList = []
for departmentId in departmentIdList:
    userSimpleInfoList.extend(ouyeelAttendance.getCurDepartmentUserSimpleInfo(departmentId))
'去重'
userSimpleInfoList = getUniquList(userSimpleInfoList)
print('\n④获取所有部门下公司人员信息：')
print('信息条数为(去重后):' + str(len(userSimpleInfoList)))
'获取所有姓名及id对合集'
userIdList = []
userSimpleInfoDicList = userSimpleInfoList
for userSimpleInfoDic in userSimpleInfoList:
    userIdList.append(userSimpleInfoDic['userid'])
print(userSimpleInfoDicList)

'获取考勤信息'
attendanceInfoDicList = ouyeelAttendance.getUserAttendanceInfo(
    userIdList,
    BEGIN_TIME,
    END_TIME)
print('\n获取考勤信息：')
print('考勤信息条数：' + str(len(attendanceInfoDicList)))
#print(attendanceInfoDicList)

'将考勤信息和人员对应起来'
formatAttendanceInfoDicList = []
for attendanceInfoDic in attendanceInfoDicList:
    for userSimpleInfoDic in userSimpleInfoDicList:
        if userSimpleInfoDic['userid'] == attendanceInfoDic['userId']:
            tempAttendanceInfoDic = attendanceInfoDic
            tempAttendanceInfoDic['name'] = userSimpleInfoDic['name']
            formatAttendanceInfoDicList.append(tempAttendanceInfoDic)
print('\n获取格式化考勤信息：')
print('共有' + str(len(formatAttendanceInfoDicList)))
print(formatAttendanceInfoDicList)

'生成考勤报表'
resultString = []
for formatAttendanceInfoDic in formatAttendanceInfoDicList:
    resultString.append(
        formatAttendanceInfoDic['name'] + ' '
    )
print(resultString)
