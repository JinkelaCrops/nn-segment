"""
规则
1. 连续多个单词首字母大写 -> 人名，药品名 等 专有名词 1
2. 出一句话里有多个大写首字母：标题                   1
3. 拼写错误：rion连在一起 5
4. 药品名: 数字',数字'-英文, 有空格,数字-英文类似的之间不能有空格 4
5.

"""

from label.analyzer import *


def read_data(data_path):
    with open(data_path, "r", encoding="utf8") as f:
        data = f.readlines()
    data = [d[:-1].strip() for d in data]
    return data


data_dir = "data/medicine_en"
data_name = "en.medicine.sample.txt"
data_path = f"{data_dir}/{data_name}"
data = read_data(data_path)
all_pattern = list(re_findall("\([^\(\)]*?\)", data).keys())
all_pattern = [p[1:-1].strip() for p in all_pattern]

# 10
pt = "[0-9]+"

# 10.2
pt = "[0-9]+\.[0-9]+"

# abc123，专有名词(CH2)
pt = "[A-Za-z]+[0-9]+"

# abc 123，举例(group 1)
pt = "[A-Za-z]+ +[0-9]+"

# 123abc
pt = "[0-9]+[A-Za-z]+"

# 1,1'-something
pt = "([0-9,]+[ ']*\-[ ']*)+[A-Za-z \-']+"

len(re_search(f"^{pt}$", all_pattern)) / len(all_pattern)


