import sys
sys.path.append('../')
from lib.my_regex import *

def has_eos(text):
    if (eos_pattern.search(text)):
        return True
    eos_match = brackets_eos.search(text)
    if (eos_match != None and eos_match.end() == len(text)): #文末に閉じ括弧があったら
        return True
    return False

def join_continuous_sentences(data):
    joined_data = []
    data_len = len(data)
    idx = 0
    while (idx < data_len):
        elem_to_push = data[idx].copy()
        appended_content = ""
        while (True):
            appended_content += data[idx]["text"]
            if (has_eos(data[idx]["text"])):
                break
            idx += 1
            if (idx >= data_len):
                break
        elem_to_push["text"] = appended_content
        joined_data.append(elem_to_push)
        idx += 1
    return joined_data