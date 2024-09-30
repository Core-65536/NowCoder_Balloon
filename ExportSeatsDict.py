import pandas as pd
import json
from tkinter import Tk
from tkinter.filedialog import askopenfilename


# 打开文件选择对话框选择Excel文件
def select_excel_file():
    Tk().withdraw()  # 隐藏主窗口
    filename = askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
    return filename


# 读取Excel文件并转换为JSON格式
def excel_to_json(excel_file):
    try:
        # 使用pandas读取Excel文件
        df = pd.read_excel(excel_file, engine='openpyxl')  # 确保使用openpyxl引擎

        # 将Excel内容转换为字典格式，列1为键，列2为值
        seat_dict = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))

        # 将字典写入JSON文件
        with open('Seats.json', 'w', encoding='utf-8') as json_file:
            json.dump(seat_dict, json_file, ensure_ascii=False, indent=4)
        print("成功导出到Seats.json")

    except UnicodeDecodeError as e:
        print(f"文件编码错误: {e}")
    except Exception as e:
        print(f"出现错误: {e}")


if __name__ == "__main__":
    excel_file = select_excel_file()
    if excel_file:
        excel_to_json(excel_file)
    else:
        print("未选择文件")
