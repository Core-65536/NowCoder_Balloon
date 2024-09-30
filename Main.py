import _thread
import queue
import time

import _tkinter

import Crawler
import GUI
import Utils

BalloonColor = {    # 题号对应的气球颜色，可以修改
    'A': 'red',
    'B': 'blue',
    'C': 'yellow',
    'D': 'green',
    'E': 'purple',
    'F': 'orange',
    'G': 'pink',
    'H': 'brown',
    'I': 'black',
    'J': 'white',
    'K': 'gray',
    'L': 'cyan',
    'M': 'magenta',
    'N': 'lime'
}
ContestID = 91947   # 比赛ID，可以修改
ProgramLiveTime = 3600 * 5  # 比赛持续时间，单位秒，可以修改
DDosTime = 30    # 防止对服务器造成过大负担的时间，建议最小值为30s


def main():
    ProgramStartTime = time.time()
    TeamHashMap = {}
    SeatsDict = Utils.LoadSeatsDict()

    while time.time() - ProgramStartTime <= ProgramLiveTime:    # 比赛持续时间内运行
        # 初始化获取提交列表、题目字典、用户字典、状态字典
        SubmitList = Crawler.GetSubmitList(ContestID)
        ProblemDict = Crawler.GetProblemDict(SubmitList)
        UserIdDict = Crawler.GetUserIdDict(SubmitList)
        StatusDict = Crawler.GetStatusDict(SubmitList, UserIdDict, ProblemDict)
        StartTime = time.time()
        # 初始化气球队列
        balloon_queue = queue.Queue()
        for i in StatusDict:
            if i not in TeamHashMap:
                # 如果队伍某题AC，则将其加入气球队列
                # type(i): tuple, i[0]: 队伍名, i[1]: 题号
                TeamHashMap[i] = 1  # 标记为已加入气球队列，采用Dict防止重复加入
                if i[0] in SeatsDict:
                    CurrentSeat = SeatsDict[i[0]]
                else:
                    CurrentSeat = '301-Default'
                balloon_queue.put({
                    "team": i[0],                   # 队伍名
                    "Seat": CurrentSeat,               # 座位号
                    "color": BalloonColor[i[1]]     # 气球颜色
                })
        if balloon_queue.empty():   # 如果没有队伍AC，则不启动GUI
            while time.time() - StartTime <= DDosTime:  # 防止对服务器造成过大负担, 最小值建议为30s
                time.sleep(1)
            continue
        # 初始化GUI
        root = GUI.tk.Tk()
        GUI.BalloonApp(root, balloon_queue)     # 传入气球队列
        root.mainloop()     # 运行GUI
        try:
            root.destroy()  # 关闭GUI
        except _tkinter.TclError:  # 在志愿者直接关闭窗口时, destroy()会报错
            pass    # 无需处理错误
        while time.time() - StartTime <= DDosTime:  # 防止对服务器造成过大负担, 最小值建议为30s
            time.sleep(1)


if __name__ == '__main__':
    main()
