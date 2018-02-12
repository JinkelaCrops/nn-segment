import re


def read_data(data_path):
    with open(data_path, "r", encoding="utf8") as f:
        data = f.readlines()
    data = [d[:-1].strip() for d in data]
    return data


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

    @staticmethod
    def rep_dull(line):
        tmp_find = re.finditer("(?<= ).*?(?= )|^.*?(?= )|(?<= ).*?$", line)
        for tmp in tmp_find:
            s, e = tmp.start(), tmp.end()
            if e - s == 1:
                tmp_sub = "S"
            else:
                tmp_sub = "B" + "M" * (e - s - 2) + "E"
            line = line[:s] + tmp_sub + line[e:]
        return line


class CleanRulePool(object):
    def __init__(self):
        pass

    @staticmethod
    def clean_all_word(line):
        line = re.sub("BM*E|(?<!-)\\bS\\b(?!-)", "#", line)
        line = re.sub("[ #]*#[ #]*", "#", line)
        line_group = line.strip("# ").split("#")
        return line_group


class Pack(object):
    def __init__(self, line_break="\n\n"):
        self.line_break = line_break
        self.pack_data = []

    def pack(self, data, cleaned_data):
        self.pack_data = [f"{d}{self.line_break[0]}{cd}" for d, cd in zip(data, cleaned_data)]
        self.pack_data = [f"{p}{self.line_break}" for p in self.pack_data]
        return self.pack_data


if __name__ == "__main__":
    data_dir = "../data/medicine_en"
    data_name = "en.medicine.sample.txt"
    data_path = f"{data_dir}/{data_name}"
    output_path = f"{data_dir}/{data_name}.label"
    data = read_data(data_path)
    tmp_data = data
    # tmp_data = [LabelRulePool.rep_multi(d) for d in tmp_data]
    # tmp_data = [LabelRulePool.rep_single(d) for d in tmp_data]
    tmp_data = [LabelRulePool.rep_dull(d) for d in tmp_data]
    pack = Pack()
    pack_data = pack.pack(data, tmp_data)
    with open(output_path, "w", encoding="utf8") as f:
        f.writelines(pack_data)
