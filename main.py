'自动生成考勤日报并发布到微信群中'

from AttendanceUtil import AttendanceUtil
import requests


'********************************常量配置***************************************'
'CORP_ID 是公司识别码'
CORP_ID = "dingc7fb31db15999b4435c2f4657eb6378f"

'CORP_SECRET 钉钉中考勤日报这个应用的识别码'
CORP_SECRET = "FWGnzL06BnOh8S7vOctAYgvSumOuxQpE7Bc6wqdwCc4qdyP2uSRO0w7C9ggstocO"

'*******************************************************************************'


def getUniquList(unUniqueList):
    uniqueList = []
    for element in unUniqueList:
        if element not in uniqueList:
            uniqueList.append(element)
    return uniqueList


ouyeelAttendance = AttendanceUtil(CORP_ID, CORP_SECRET)
print('ACCSESS_TOKEN: ' + ''.join(ouyeelAttendance.getAccessToken()))

'获取公司所有部门'
departmentIdList = ouyeelAttendance.getDepartmentIds()
print('部门ID: ' + ' '.join(list(map(str, departmentIdList))))

'获取每个部门下的员工合集'
userSimpleInfoList = []
for departmentId in departmentIdList:
    userSimpleInfoList.extend(ouyeelAttendance.getCurDepartmentUserSimpleInfo(departmentId))
'去重'
userSimpleInfoList = getUniquList(userSimpleInfoList)
print('公司人员信息条数：' + str(len(userSimpleInfoList)))

'获取所有id合集'
userIdList = []
for userIdDic in userSimpleInfoList:
    userIdList.append(userIdDic['userid'])
print('所有人员id条数：' + str(len(userIdList)))

