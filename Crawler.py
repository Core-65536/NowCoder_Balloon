import json

import Networks
import Utils

# 是否启用学校筛选功能
SelectSchool = 0
SchoolName = '辽宁大学'


# 获取题目字典, 返回字典{题目ID: 题目序号}
def GetProblemDict(SubmitList):
    SubmitList = SubmitList['problemData']
    ProblemDict = {}
    for i in SubmitList:
        ProblemDict[i['problemId']] = i['index']
    return ProblemDict


# 获取用户字典, 返回字典{用户ID: 用户名}
# 如果启用学校筛选功能, 则只返回学校为SchoolName的用户
def GetUserIdDict(SubmitList):
    UserIdDict = {}
    SubmitList = SubmitList['submitDataList'][0]['signUpUsers']
    for i in SubmitList:
        if SelectSchool == 1:
            # 存在没有school字段的用户, 采用try-except处理
            try:
                if i['school'] == SchoolName:
                    UserIdDict[i['uid']] = i['name']
            except KeyError:
                pass    # 无需处理
        else:
            UserIdDict[i['uid']] = i['name']
    return UserIdDict


# 获取提交列表, 返回字典
# 提交列表例子见Sample.json
def GetSubmitList(ContestID):
    url = Utils.JointUrl(ContestID)
    rp = Networks.Net_Get(url)
    SubmitList = json.loads(rp)
    SubmitList = SubmitList['data']
    return SubmitList


# 获取状态字典, 返回字典{(用户名, 题目序号): 1}
def GetStatusDict(SubmitList, UserIdDict, ProblemDict):
    StatusDict = {}
    SubmitList = SubmitList['submitDataList'][0]['submissions']
    for i in SubmitList:
        # status: 5表示AC, uid在UserIdDict中为采用学校筛选时的过滤措施
        if i['status'] == 5 and i['uid'] in UserIdDict:
            pair = (UserIdDict[i['uid']], ProblemDict[i['problemId']])
            StatusDict[pair] = 1
    return StatusDict
