import json
import numpy as np
import os

# 读取json文件并写入为字典格式
current_path = os.getcwd()
root_path = ""
for i in range(0, len(current_path)):
    root_path += current_path[i]
    if current_path[i + 1:i + 4] == 'src':
        break
data_path = root_path + "/test_data.json"
with open(data_path, 'r', encoding='utf-8') as fp:
    json_data = json.load(fp)

# 读取所有user_id
user_ids = []
for key in json_data.keys():
    user_ids.append(key)

# 读取所有case_id
case_ids = []
case_score = {}  # 统计每题均分的字典，按照{case_id: [累计总分，累计作答人数]}存储数据
case_info = {}  # 统计每题信息的字典，按照{case_id: {'题目类型': '', '作答人数': '', '平均得分': ''}}存储数据
for user_id in user_ids:
    cases = json_data[user_id]['cases']
    for case in cases:
        if case['case_id'] not in case_ids:  # 发现新的题目
            case_ids.append(case['case_id'])
            case_info.setdefault(case['case_id'], {'题目类型': case['case_type'], '题目地址': case['case_zip']})  # 初始化case_info
            case_score.setdefault(case['case_id'], [case['final_score'], 1])
        else:  # 已有题目
            case_score[case['case_id']][0] += case['final_score']
            case_score[case['case_id']][1] += 1

average_scores = []

for key in case_score:
    case_info[key]['作答人数'] = case_score[key][1]
    average_score = case_score[key][0] / case_score[key][1]
    case_info[key]['平均得分'] = average_score
    average_scores.append(100 - average_score)

max_average_score = np.max(average_scores)
min_average_score = np.min(average_scores)

for key in case_score:
    case_info.get(key)['index'] = (100 - case_info.get(key)['平均得分'] - min_average_score) / (
                max_average_score - min_average_score) * 100

# 将题目信息写入case_info.json文件
json_str = json.dumps(case_info, ensure_ascii=False, indent=4)
storage_path = root_path + "/src/difficultyAnalysis/avgScoreCount/case_info.json"
with open(storage_path, 'w', encoding='utf-8') as fp:
    fp.write(json_str)
