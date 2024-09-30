import tkinter as tk


# GUI界面
# Author: ChatGPT-GPT4o
class BalloonApp:
    def __init__(self, root, balloon_queue):
        self.labels = None
        self.Count = 0
        self.queueLen = balloon_queue.qsize()
        if self.queueLen <= 3:
            self.Count = 3 - self.queueLen

        self.root = root
        self.root.title("ACM Balloon Distribution")
        self.root.geometry("800x400")  # 增大窗口大小

        self.balloon_queue = balloon_queue  # 接收队列
        self.balloon_info = []  # 当前界面显示的气球信息
        self.create_widgets()
        self.populate_initial_balloon_info()

    def create_widgets(self):
        # 设置大字体
        large_font = ("Helvetica", 16)

        # 初始化显示区域
        self.labels = []
        for i in range(3):  # 界面上最多显示3个队伍信息
            team_label = tk.Label(self.root, text="队伍名", font=large_font, width=20)
            team_label.grid(row=i, column=0, padx=20, pady=20)
            seat_label = tk.Label(self.root, text="座位号", font=large_font, width=10)
            seat_label.grid(row=i, column=1, padx=20, pady=20)
            color_label = tk.Label(self.root, text="气球颜色", font=large_font, bg="white", width=10)
            color_label.grid(row=i, column=2, padx=20, pady=20)
            button = tk.Button(self.root, text="已送达", font=large_font,
                               command=lambda idx=i: self.balloon_delivered(idx), width=10, height=2)
            button.grid(row=i, column=3, padx=20, pady=20)
            self.labels.append((team_label, seat_label, color_label))

    def populate_initial_balloon_info(self):
        # 从队列中初始获取气球信息并显示
        for _ in range(3):  # 最多显示3个任务
            if not self.balloon_queue.empty():
                task = self.balloon_queue.get_nowait()
                self.balloon_info.append(task)

        # 更新显示
        for idx, info in enumerate(self.balloon_info):
            self.labels[idx][0].config(text=info["team"])  # 队伍名
            self.labels[idx][1].config(text=info["Seat"])  # 座位号
            self.labels[idx][2].config(text=info["color"], bg=info["color"].lower())  # 气球颜色

    def balloon_delivered(self, idx):
        # 当前行的任务标记为已送达，并更新为队列中下一个任务
        if idx < len(self.balloon_info):
            print(f"气球已送达: {self.balloon_info[idx]['team']}")
            if not self.balloon_queue.empty():
                # 从队列中取下一个任务并替换掉当前的
                next_task = self.balloon_queue.get_nowait()
                self.balloon_info[idx] = next_task
                # 更新当前行的信息
                self.labels[idx][0].config(text=next_task["team"])
                self.labels[idx][1].config(text=next_task["Seat"])
                self.labels[idx][2].config(text=next_task["color"], bg=next_task["color"].lower())
            else:
                self.labels[idx][0].config(text='队伍名')
                self.labels[idx][1].config(text='座位号')
                self.labels[idx][2].config(text='气球颜色', bg='white')
                self.Count += 1
                if self.Count >= 3:
                    print("所有气球任务已送达，程序退出。")
                    self.root.after(1000, self.root.quit)
