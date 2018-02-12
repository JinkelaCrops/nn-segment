import re

data_dir = "/media/yanpan/7D4CF1590195F939/Projects/nn-segment/data/medicine_en"
data_name = "en.medicine.sample.txt"
data_path = f"{data_dir}/{data_name}"


def read_data(data_path):
    with open(data_path, "r", encoding="utf8") as f:
        data = f.readlines()
    data = [d[:-1].strip() for d in data]
    return data


data = read_data(data_path)


class LabelRulePool(object):
    def __init__(self):
        pass

    @staticmethod
    def rep_single(line):
        return re.sub("(?<!-)\\b[A-Za-z]\\b(?!-)", "S", line)

    @staticmethod
    def rep_multi(line):
        tmp_find = re.finditer("[A-Za-z\-]{2,}", line)
        for tmp in tmp_find:
            line = line[:tmp.start()] + "B" + "M" * (tmp.end() - tmp.start() - 2) + "E" + line[tmp.end():]
        return line

rep_single(rep_multi(data[0]))