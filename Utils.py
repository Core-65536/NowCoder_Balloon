import json
import os.path


# 拼接查询url
def JointUrl(ContestID):
    # url例子: https://ac.nowcoder.com/acm/contest/rank/submit-list?currentContestId=91177&contestList=91177
    url = 'https://ac.nowcoder.com/acm/contest/rank/submit-list?'
    url += 'currentContestId=' + str(ContestID) + '&'
    url += 'contestList=' + str(ContestID)
    return url


# 读取座位信息
def LoadSeatsDict():
    if os.path.exists('Seats.json'):
        pass
    else:
        print("Seats.json不存在, 请检查文件是否存在")
        exit(0)
    with open('Seats.json', 'r', encoding='utf-8') as f:
        SeatDicts = json.load(f)
    for i in SeatDicts:
        SeatDicts[i] = str(SeatDicts[i])
    return SeatDicts
