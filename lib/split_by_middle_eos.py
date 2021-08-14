import sys
sys.path.append('../')
from lib.my_regex import *

def has_eos_in_btwn(eos_match, str):
    if (eos_match == None):
        return False
    if (eos_match.end() == len(str)):
        return False
    else:
        return True


# 中間に文末文字がある限り、再帰的に自身を呼び、dataに追加し続ける
def split_as_long_as_middle_eos_exist(text, data, elem_to_push):
    eos_match = eos_pattern.search(text)
    elem = elem_to_push.copy()
    if (has_eos_in_btwn(eos_match, text)):
        former = text[:eos_match.end()]
        latter = text[eos_match.end():]
        elem["text"] = former
        data.append(elem)
        split_as_long_as_middle_eos_exist(latter, data, elem_to_push)
    else:
        elem["text"] = text
        data.append(elem)

def split_by_middle_eos(raw_data):
    data = []
    for element in raw_data:
        split_as_long_as_middle_eos_exist(element["text"], data, element)
    return data
