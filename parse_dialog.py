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


def get_first_eos_idx(str):
    eos_chars = ["｡",    "?",    "!",    "！",    "？",    "》"]
    INFINITY = 1000000000
    min_idx = INFINITY
    for eos in eos_chars:
        idx = str.find(eos)
        if (idx != -1):
            min_idx = min(idx, min_idx)
    if (min_idx == INFINITY):
        return -1
    return min_idx


def split_until_middle_eos_exist(data, elem_to_push, latter):
    while (True):
        eos_idx = get_first_eos_idx(latter[:-1])
        if (eos_idx != -1):
            former = latter[:eos_idx + 1]
            latter = latter[eos_idx + 1:]
            elem_to_push["text"] = former
            data.append(elem_to_push.copy())
        else:
            elem_to_push["text"] = latter
            data.append(elem_to_push.copy())
            break


def split_by_middle_eos(raw_data):
    data = []
    data_len = len(raw_data)
    idx = 0
    while (idx < data_len):
        elem_to_push = raw_data[idx].copy()
        eos_idx = get_first_eos_idx(raw_data[idx]["text"][:-1])
        if (eos_idx != -1):
            former = raw_data[idx]["text"][:eos_idx + 1]
            latter = raw_data[idx]["text"][eos_idx + 1:]
            elem_to_push["text"] = former
            data.append(elem_to_push.copy())
            split_until_middle_eos_exist(data, elem_to_push, latter)
        else:
            data.append(elem_to_push)
        idx += 1
    return data


def join_continuous_sentence(data):
    joined_data = []
    data_len = len(data)
    idx = 0
    while (idx < data_len):
        elem_to_push = data[idx]
        appended_content = ""
        while (True):
            appended_content += data[idx]["text"]
            if (has_eos(data[idx]["text"][-1:])):
                break
            idx += 1
        elem_to_push["text"] = appended_content
        joined_data.append(elem_to_push)
        idx += 1
    return joined_data

                # if (has_eos_at_the_end(data[idx]["text"])):
                #     break
                # else:
                #     #最初の文末文字まで前の文に連結
                #     former = data[idx]["text"][111]
                #     latter = data[idx]["text"][222]
                #     appended_content += former
                #     elem_to_push["text"] = appended_content
                #     joined_data.append(elem_to_push)
                #     continue
                    
                #     #前の文のtext以外のデータを複製し、(label1に戻って)文末文字以降の文字列を解析する

#textに文末文字があったら
    #文末文字が末尾で見つかったら
        #前の文にすべての文を連結して終了する
    #文末文字が途中で見つかったら
        #最初の文末文字まで前の文に連結
        #前の文のtext以外のデータを複製し、(label1に戻って)文末文字以降の文字列を解析する

file_name = "./another.ass"
# file_name = "./result.txt"
# data = parse_data_from_file(file_name)
# data = split_by_middle_eos(data)
# joined_data = join_continuous_sentence(data)

# print_data(data)

examples = [
    "アニキ！!ああ",
    "こ。ん!!にちは!!",
    "!?さようなら",
    "さようなら",
]

for row in examples:
    print(get_eos_in_btwn_sentence(row))

# print(eos_pattern2.search("hello"))
# print(eos_pattern2.search("hello a"))