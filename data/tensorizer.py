from collections import Counter
import pickle
import re
import os


class BaseFunction(object):

    @staticmethod
    def iter_sum(lst):
        tmp = lst[0]
        for l in lst[1:]:
            tmp += l
        return tmp


class IO(object):
    def __init__(self):
        pass

    @staticmethod
    def read(read_path, read_type="csv"):
        if read_type == "csv":
            with open(read_path, "r", encoding="utf8") as f:
                return f.readlines()
        elif save_type == "pickle":
            return pickle.load(open(save_path, "rb"))
        else:
            raise NotImplementedError("other read_type is not supported yet.")

    @staticmethod
    def save(save_data, save_path, save_type="csv"):
        if save_type == "csv":
            with open(save_path, "w", encoding="utf8") as f:
                f.writelines(save_data)
        elif save_type == "pickle":
            pickle.dump(save_data, open(save_path, "wb"))
        else:
            raise NotImplementedError("other save_type is not supported yet.")

    def read_proj(self, proj_name, clean_func=lambda x: x):
        proj_path = "/".join(proj_name.split("/")[:-1])
        proj_prefix = proj_name.split("/")[-1]
        proj_files = list(filter(lambda x: x.startswith(proj_prefix), os.listdir(proj_path)))
        data_dict = {pf: clean_func(self.read(f"{proj_path}/{pf}")) for pf in proj_files}
        return data_dict


class TextClean(object):
    def __init__(self):
        pass

    @staticmethod
    def strip_lines(lines, strip_char=None):
        if strip_char:
            lines = [line.strip(strip_char) for line in lines]
        else:
            lines = [line.strip() for line in lines]
        return lines


class DataField(object):
    def __init__(self, x, y, x_dict=None, y_dict=None):
        self.x = x
        self.y = y
        assert len(self.x) == len(self.y)
        self.length = len(self.x)
        self.x_dict = self.make_dict(self.x) if x_dict is None else x_dict
        self.y_dict = self.make_dict(self.y) if y_dict is None else y_dict

    @staticmethod
    def make_dict(lines):
        sum_counter = BaseFunction.iter_sum([Counter(line) for line in lines])
        words = sorted(sum_counter.keys())
        words = ["█"] + words
        return dict(zip(words, range(len(words))))

    def make_field(self):
        def make_line_tensor(char_lst, char_to_index):
            char_lst_tmp = []
            for char in char_lst:
                try:
                    char_lst_tmp.append(char_to_index[char])
                except KeyError as e:
                    char_lst_tmp.append("<unk>")
            return char_lst_tmp

        self.x = {k: make_line_tensor(x_line, self.x_dict) for k, x_line in enumerate(self.x)}
        self.y = {k: make_line_tensor(y_line, self.y_dict) for k, y_line in enumerate(self.y)}
        return 0


if __name__ == '__main__':
    proj_name = "../data/medicine_en/medicine"
    io = IO()
    train_dict = io.read_proj(f"{proj_name}_train", clean_func=lambda x: x)
    valid_dict = io.read_proj(f"{proj_name}_valid", clean_func=lambda x: x)
    test_dict = io.read_proj(f"{proj_name}_test", clean_func=lambda x: x)

    s, t = f'medicine_train.src', f'medicine_train.tgt'
    train_field = DataField(train_dict[s], train_dict[t])
    train_src_dict = train_field.x_dict
    train_tgt_dict = train_field.y_dict
    train_field.make_field()

    s, t = f'medicine_valid.src', f'medicine_valid.tgt'
    valid_field = DataField(valid_dict[s], valid_dict[t], train_src_dict, train_tgt_dict)
    valid_field.make_field()

    s, t = f'medicine_test.src', f'medicine_test.tgt'
    test_field = DataField(test_dict[s], test_dict[t], train_src_dict, train_tgt_dict)
    test_field.make_field()

    # save dictionary, train and valid
    t.save(train_field, open(proj_name + ".train.pt", "wb"))
    t.save(valid_field, open(proj_name + ".valid.pt", "wb"))
    t.save(test_field, open(proj_name + ".test.pt", "wb"))
