import re

def print_data(data):
    for row in data:
        print(f'start: {row["start"]}, end: {row["end"]} content: {row["text"]}')


def split_by_comma(line):
    block_count = 9
    formats = ["layer", "start", "end", "style", "name", "marginl", "marginr", "marginv", "effect", "text"]

    line = line.rstrip()
    line = line.replace('\\N', '')

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
    if "｡" in txt or "?" in txt or "!" in txt or "！" in txt or "？" in txt or "《" in txt or "》" in txt:
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


def join_continuous_sentence(data):
    joined_data = []
    data_len = len(data)
    idx = 0
    while (idx < data_len):
        elem_to_push = data[idx]
        appended_content = ""
        while (True):
            appended_content += data[idx]["text"]
            if (has_eos(data[idx]["text"])):
                break
            idx += 1
        elem_to_push["text"] = appended_content
        joined_data.append(elem_to_push)
        idx += 1
    return joined_data


#((label 1)) #textに文末文字が含まれているか判定する
    #文末文字がなければ
        #文末文字が出てくるまでtextを連結する(次の行を解析する)
    #文末文字が末尾で見つかったら
        #前の文にすべての文を連結して終了する
    #文末文字が途中で見つかったら
        #最初の文末文字まで前の文に連結
        #前の文のtext以外のデータを複製し、(label1に戻って)文末文字以降の文字列を解析する

file_name = "./2020_01_05_Sun_0900_0930_ch8_A_.ass"
# file_name = "./result.txt"
data = parse_data_from_file(file_name)
joined_data = join_continuous_sentence(data)
print_data(joined_data)
