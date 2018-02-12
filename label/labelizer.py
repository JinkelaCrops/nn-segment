import re
import random


class Labelizer(object):
    def __init__(self, label_file_path, line_break="\n\n"):
        self.f = open(label_file_path, "r", encoding="utf8")
        self.line_break = line_break
        self.data = []
        self.data_reshape = []

    def process(self):
        with self.f:
            self.data = [d.split(self.line_break[0]) for d in self.f.read().split(self.line_break) if not d == ""]
        self.data_reshape = list(zip(*self.data))
        return self.data_reshape


class TrainValidTestSplit(object):
    def __init__(self):
        pass

    @staticmethod
    def split_and_write(bi_data, data_name="data", test_size=1000, valid_size=1000):
        random.seed(0)
        src_data = random.sample(bi_data[0], len(bi_data[0]))
        random.seed(0)
        tgt_data = random.sample(bi_data[1], len(bi_data[1]))
        if not src_data[0][-1] == "\n":
            src_data = ["%s\n" % d for d in src_data]
            tgt_data = ["%s\n" % d for d in tgt_data]

        train_name = f"{data_name}_train"
        test_name = f"{data_name}_test"
        valid_name = f"{data_name}_valid"

        with open(f"{train_name}.src", "w", encoding="utf8") as f:
            f.writelines(src_data[:-(test_size + valid_size)])
        with open(f"{train_name}.tgt", "w", encoding="utf8") as f:
            f.writelines(tgt_data[:-(test_size + valid_size)])
        with open(f"{test_name}.src", "w", encoding="utf8") as f:
            f.writelines(src_data[-test_size:])
        with open(f"{test_name}.tgt", "w", encoding="utf8") as f:
            f.writelines(tgt_data[-test_size:])
        with open(f"{valid_name}.src", "w", encoding="utf8") as f:
            f.writelines(src_data[-(test_size + valid_size):-test_size])
        with open(f"{valid_name}.tgt", "w", encoding="utf8") as f:
            f.writelines(tgt_data[-(test_size + valid_size):-test_size])
        return 0


if __name__ == '__main__':
    label_file_path = "../data/medicine_en/en.medicine.sample.txt.label"

    lb = Labelizer(label_file_path)
    TrainValidTestSplit.split_and_write(lb.process(), "../data/medicine_en/medicine")
