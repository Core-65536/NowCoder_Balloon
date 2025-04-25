import json
import csv
import os

def parse_json_to_cssv(json_file, output_csv):
    # 读取JSON文件
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 提取关键数据
    submit_data = data['data']['submitDataList'][0]
    submissions = submit_data['submissions']
    users = {user['uid']: user['name'] for user in submit_data['signUpUsers']}
    
    # 创建题目ID到题号的映射
    problem_map = {problem['problemId']: problem['index'] for problem in data['data']['problemData']}
    
    # 准备CSV数据
    csv_data = []
    for submission in submissions:
        uid = submission['uid']
        problem_id = submission['problemId']
        
        csv_data.append({
            '用户名': users.get(uid, f"Unknown-{uid}"),
            '题号': problem_map.get(problem_id, "Unknown"),
            '题目ID': problem_id,
            '状态': "AC" if submission['status'] == 5 else "未AC",
            '提交时间': submission['submitTime'],
            '耗时(ms)': submission['timeConsumption'],
            '提交ID': submission['submissionId']
        })
    
    # 写入CSV文件
    with open(output_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=csv_data[0].keys())
        writer.writeheader()
        writer.writerows(csv_data)
    
    print(f"已将数据导出至 {output_csv}")

# 执行转换
parse_json_to_csv('Sample.json', 'contest_submissions.csv')