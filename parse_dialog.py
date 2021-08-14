import re

def print_data(data):
    for row in data:
        print(f'start: {row["start"]}, end: {row["end"]} content: {row["text"]}')


def split_by_comma(line):
    block_count = 9
    formats = ["layer", "start", "end", "style", "name", "marginl", "marginr", "marginv", "effect", "text"]

    line = line.rstrip()
    line = line.replace('\\N', '')
    line = line.replace('➡', '')

    # 左端からblock_count回だけ分割する
    splitted_list = line.split(',', block_count)

    #リストのままだとアクセスしづらいので、formats順に辞書にする
    data = dict(zip(formats, splitted_list))

    #textをposとcontentに分離し、辞書でまとめて保存
    pos_text = data['text'].split('}')
    pos = pos_text[0].strip('{')
    text = pos_text[1]
    data['pos'] = pos
    data['text'] = text
    return data


def has_eos(txt0):
    txt = list(txt0)
    if "｡" in txt or "?" in txt or "!" in txt or "！" in txt or "？" in txt or "》" in txt:
        return True 
    else:
        return False

# ファイルから読み込んで連想配列を返却する関数
# 戻り値のデータ構造
# data[idx]['key']
# key == text のとき, textのvalueは辞書{'pos', 'content'}
###### example
# data = [
#     {
#         'layer': 'Dialogue: 0',
#         'start': '0:25:05.36',
#         'end': '0:25:08.36',
#         'style': 'Default',
#         'name': '', 
#         'marginl': '0000',
#         'marginr': '0000',
#         'marginv': '0000',
#         'effect': '',
#         'pos': '\\pos(500,1020)\\c&H00ffff&',
#         'text': '見えない世界の扉が開く｡'
#         },
# ]
def parse_data_from_file(file_name):
    data = []
    with open(file_name,"r",encoding="utf-8_sig") as f:
        for line in f.readlines():
            #先頭がDialogueでなければskip
            if (re.match(r'^Dialogue:', line) == None):
                continue
            row = split_by_comma(line)
            if (row['style'] == 'Default'):
                data.append(row)
    return data

eos_pattern = re.compile(r".*?[。｡?!！？》]+")
brackets_eos = re.compile(r"[)）]$")
def get_eos_in_btwn_sentence(str):
    pattern = eos_pattern.search(str)
    return pattern

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

def join_continuous_sentence(data):
    joined_data = []
    data_len = len(data)
    idx = 0
    while (idx < data_len):
        elem_to_push = data[idx].copy()
        appended_content = ""
        while (True):
            appended_content += data[idx]["text"]
            if (has_eos(data[idx]["text"][-1:])):
                break
            idx += 1
            if (idx >= data_len):
                break
        elem_to_push["text"] = appended_content
        joined_data.append(elem_to_push.copy())
        idx += 1
    return joined_data

file_name = "./another.ass"
# file_name = "./2020_01_05_Sun_0900_0930_ch8_A_.ass"
data = parse_data_from_file(file_name)
data = split_by_middle_eos(data)
data = join_continuous_sentence(data)

print_data(data)
