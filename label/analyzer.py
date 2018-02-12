import re
from collections import Counter
# import pandas as pd
# from fuzzywuzzy import fuzz
# import json


# 返回匹配的所有片段
def re_findall(reg, ref, counter=True):
    """
    reFindall("^【.*?】",ref)
    """
    tmp = list(map(lambda x: re.finditer(reg, x), ref))
    if counter:
        return Counter([y.group() for x in tmp for y in x])
    else:
        return list(set([y.group() for x in tmp for y in x]))


# 返回匹配的所有原句
def re_search(reg, ref):
    """
    reSearch("^【.*?】",ref)
    """
    tmp = list(filter(lambda x: re.search(reg, x) is not None, ref))
    return tmp


def re_bi_search(reg, refs):
    """
    reSearch("^【.*?】",ref)
    """
    tmps = []
    for ref in refs:
        tmps.append(list(map(lambda x: re.search(reg, x) is not None, ref)))
    tmp = list(map(any, zip(*tmps)))
    res = list(filter(lambda x: tmp[x[0]], enumerate(zip(*refs))))
    res = [(r[0], r[1][0], r[1][1]) for r in res]
    return res


# 返回删除匹配之后的所有原句
def re_findall_delete(reg, ref):
    """
    reSearch("^【.*?】",ref)
    """
    tmp = list(map(lambda x: re.sub(reg, "", x), ref))
    return tmp


# 根据某个片段匹配整句中的部分
# def candidate_similar_(src_sentence, tgt_sentence, level=-1, report=True):
#     sep = "\u0000"
#     src_sentence = re.sub("(?<=[A-Za-z ])([,\.:;!\?\(\)\[\]/])(?=[A-Za-z ])", " \\1 ", src_sentence)
#     tgt_sentence = re.sub("(?<=[A-Za-z ])([,\.:;!\?\(\)\[\]/])(?=[A-Za-z ])", " \\1 ", tgt_sentence)
#
#     src_sentence = re.sub("(?<= )[A-Za-z]+[-']?[A-Za-z]*(?= )", sep, src_sentence)
#     src_sentence = re.sub(f"(?<={sep}) *[,\.:;!\?\(\)\[\]/]+ *(?={sep}|$)", sep, src_sentence)
#     src_sentence = re.sub(f"(?<=^) *[,\.:;!\?\(\)\[\]/]+ *(?={sep}|$)", sep, src_sentence)
#     src_sentence = re.sub(f"[ {sep}]*{sep} *", sep, src_sentence)
#     candidate = list(filter(len, src_sentence.split(sep)))
#
#     # for can in candidate:
#     #     print(can, "###", fuzz.partial_ratio(can, tgt_sentence))
#     scores = {can: fuzz.partial_ratio(can, tgt_sentence) for can in candidate}
#     scores_filter = {can: s for can, s in scores.items() if s > level}
#     if report:
#         return str(scores_filter)
#     else:
#         return len(scores_filter) == len(scores)
