'自动生成考勤日报并发布到微信群中'

from ouyeel_Attendance.ouyeel_Attendance.AttendanceUtil import AttendanceUtil

'********************************常量配置***************************************'
'CORP_ID 是公司识别码'
CORP_ID = "ding0yr83dhxnera2lon"

'CORP_SECRET 钉钉中考勤日报这个应用的识别码'
CORP_SECRET = "YMwxF_izQLWT3SwnyIAvm1XDIioD4sCHXH2gwbEPvI1fPEOCCb_2U7jZOwB9pkds"

#BEGIN_TIME = time.strftime("%Y-%m-%d 00:00:00", time.localtime())
#END_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

BEGIN_TIME = "2019-09-11 19:00:00"
END_TIME = "2019-09-11 23:59:59"


'**************************************函数声明*************************************'
'辅助 - 列表排重'
def getUniquList(unUniqueList):
    uniqueList = []
    for element in unUniqueList:
        if element not in uniqueList:
            uniqueList.append(element)
    return uniqueList


'辅助 - 翻译考勤结果字符串'
def formatAttendanceResult(attendanceResult):
    """时间结果翻译"""
    resultDic = {
        'Normal': '正常',
        'Early': '早退',
        'Late': '迟到',
        'SeriousLate': '严重迟到',
        'Absenteeism': '旷工迟到',
        'NotSigned': '未打卡'
    }

    if attendanceResult in resultDic:
        result = resultDic[attendanceResult]
    else:
        result = '未定义'

    return result





    return


'主要 - 获取考勤结果信息（不含有市外出差、市内外出及请假信息 - 只能获取到打过卡的人的记录）'
def getAttendanceResult_OnlyChecked(userIdList, userSimpleInfoDicList, beginTime, endTime):
    '根据id获取考勤结果(此考勤)'
    attendanceInfoDicList = ouyeelAttendance.getUserAttendanceInfo(
        userIdList,
        beginTime,
        endTime)
    print('\n获取考勤信息：')
    print('考勤信息条数：' + str(len(attendanceInfoDicList)))

    '将考勤结果和人员对应起来（仅保留上班考勤）'
    formatAttendanceInfoDicList = []
    for attendanceInfoDic in attendanceInfoDicList:
        '仅保留上班考勤记录'
        if attendanceInfoDic[ouyeelAttendance.JSON_CHECK_TYPE] == ouyeelAttendance.JSON_CHECK_TYPE_OFF_DUTY:
            continue
        for userSimpleInfoDic in userSimpleInfoDicList:
            if userSimpleInfoDic[ouyeelAttendance.JSON_USER_ID] == attendanceInfoDic[ouyeelAttendance.JSON_USERID]:
                tempAttendanceInfoDic = attendanceInfoDic
                tempAttendanceInfoDic[ouyeelAttendance.JSON_NAME] = userSimpleInfoDic[ouyeelAttendance.JSON_NAME]
                formatAttendanceInfoDicList.append(tempAttendanceInfoDic)
    print('\n获取格式化考勤信息：')
    print('共有' + str(len(formatAttendanceInfoDicList)))
    return formatAttendanceInfoDicList


'**************************************主要业务流程*************************************'
ouyeelAttendance = AttendanceUtil(CORP_ID, CORP_SECRET)
print('\n①获取ACCSESS_TOKEN:')
print(ouyeelAttendance.getAccessToken())

'获取公司所有部门'
departmentIdList = ouyeelAttendance.getDepartmentIds()
print('\n②获取所有部门ID: ')
print(departmentIdList)

'获取每个部门下的员工姓名及id合集'
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
for userSimpleInfoDic in userSimpleInfoDicList:
    userIdList.append(userSimpleInfoDic[ouyeelAttendance.JSON_USER_ID])

attendanceInfo_onlyChecked_DicList = getAttendanceResult_OnlyChecked(userIdList, userSimpleInfoDicList, BEGIN_TIME, END_TIME)
#print(attendanceInfo_onlyChecked_DicList)


'仅保留'




