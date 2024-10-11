import json
import queue
import time
import os

import _tkinter
import win32api
import win32con

import Crawler
import GUI
import Utils

BalloonColor = {  # 题号对应的气球颜色，可以修改
    'A': 'purple',
    'B': 'green',
    'C': 'orange',
    'D': 'black',
    'E': 'blue',
    'F': 'lime',
    'G': 'pink',
    'H': 'red',
    'I': 'yellow',
    'J': 'white',
    'K': 'gray',
    'L': 'cyan',
    'M': 'magenta',
    'N': 'azure',
}
ColorBalloon = {  # 气球颜色对应的题号，可以修改
    'purple': 'A',
    'green': 'B',
    'orange': 'C',
    'black': 'D',
    'blue': 'E',
    'lime': 'F',
    'pink': 'G',
    'red': 'H',
    'yellow': 'I',
    'white': 'J',
    'gray': 'K',
    'cyan': 'L',
    'magenta': 'M',
    'azure': 'N',
}
ContestID = 92670  # 比赛ID，可以修改
ProgramLiveTime = 3600 * 5  # 比赛持续时间，单位秒，可以修改
DDosTime = 10  # 防止对服务器造成过大负担的时间，建议最小值为30s
DoNotIgnoreAlreadyDelivered = 1  # 是否忽略已经送达的队伍，1为不忽略，0为忽略
# 是否启用学校筛选功能
SelectSchool = 0
SchoolName = '辽宁大学'


def main():
    if win32api.MessageBox(0, "是否第一次启动程序？", "NowCoder_Balloon",
                           win32con.MB_ICONQUESTION | win32con.MB_YESNO) == win32con.IDYES:
        if os.path.exists("RealDelivered.json"):
            os.remove("RealDelivered.json")
    ProgramStartTime = time.time()
    SeatsDict = Utils.LoadSeatsDict()
    while time.time() - ProgramStartTime <= ProgramLiveTime:  # 比赛持续时间内运行
        TeamHashMap = {}
        FirstBlood = {}
        if DoNotIgnoreAlreadyDelivered:
            try:
                with open('RealDelivered.json', 'r', encoding='utf-8') as f:
                    Delivered = json.load(f)
                    for i in Delivered:
                        TeamHashMap[(i['team'], ColorBalloon[i['color']])] = 1
                        FirstBlood[ColorBalloon[i['color']]] = i['team']
            except FileNotFoundError:
                pass
        # 初始化获取提交列表、题目字典、用户字典、状态字典
        SubmitList = Crawler.GetSubmitList(ContestID)
        ProblemDict = Crawler.GetProblemDict(SubmitList)
        UserIdDict = Crawler.GetUserIdDict(SubmitList)
        StatusDict = Crawler.GetStatusDict(SubmitList, UserIdDict, ProblemDict)
        StartTime = time.time()

        # 初始化气球队列
        balloon_queue = queue.Queue()
        for i in StatusDict:
            NameTuple = (UserIdDict[i[0]], i[1])
            if NameTuple not in TeamHashMap:
                # 如果队伍某题AC，则将其加入气球队列
                # type(i): tuple, i[0]: 队伍uid, i[1]: 题号
                TeamHashMap[i] = 1  # 标记为已加入气球队列，采用Dict防止重复加入
                if str(i[0]) in SeatsDict:
                    CurrentSeat = SeatsDict[str(i[0])]
                else:
                    CurrentSeat = 'No_Seats'
                CurrentTeamInfo = {
                    "team": UserIdDict[i[0]],  # 队伍名
                    "Seat": CurrentSeat,  # 座位号
                    "color": BalloonColor[i[1]]  # 气球颜色
                }
                if i[1] not in FirstBlood:
                    FirstBlood[i[1]] = UserIdDict[i[0]]
                    win32api.MessageBox(0, f"题号{i[1]}由{UserIdDict[i[0]]}队伍，座位号{CurrentSeat}首杀",
                                        "NowCoder_Balloon", win32con.MB_ICONWARNING)
                    RealDelivered = []
                    if os.path.exists("RealDelivered.json"):
                        RealDelivered = json.load(open("RealDelivered.json", "r", encoding='utf-8'))
                        os.remove("RealDelivered.json")
                    RealDelivered.append(CurrentTeamInfo)
                    with open("RealDelivered.json", "w", encoding='utf-8') as f:
                        json.dump(RealDelivered, f, ensure_ascii=False, indent=4)
                    continue
                balloon_queue.put(CurrentTeamInfo)
        if balloon_queue.empty():  # 如果没有队伍AC，则不启动GUI
            while time.time() - StartTime <= DDosTime:  # 防止对服务器造成过大负担, 最小值建议为30s
                time.sleep(1)
            continue
        # 初始化GUI
        root = GUI.tk.Tk()
        GUI.BalloonApp(root, balloon_queue)  # 传入气球队列
        root.mainloop()  # 运行GUI
        try:
            root.destroy()  # 关闭GUI
        except _tkinter.TclError:  # 在志愿者直接关闭窗口时, destroy()会报错
            pass  # 无需处理错误
        while time.time() - StartTime <= DDosTime:  # 防止对服务器造成过大负担, 最小值建议为30s
            time.sleep(1)


if __name__ == '__main__':
    main()
