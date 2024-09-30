# NowCoder_Balloon - 适配牛客竞赛的气球发放脚本

Python环境：Python 3.12

安装程序依赖：
  `pip install requests pandas`

使用指南：\
  首先运行`ExportSeatsDict.py`, 选择座位表导入至json中 \
  然后即可运行`Main.py` \
  脚本会自动爬取`Main.py`中对应比赛ID的榜单, 并将气球队列以GUI形式显示 \
  GUI会在当前气球队列发放完毕后退出, 后台每30s检测是否有新的气球应当发放, 如果有则重新弹出GUI窗口
