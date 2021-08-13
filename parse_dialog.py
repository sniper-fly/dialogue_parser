import re

def split_by_comma(line):
    block_count = 9
    formats = ["layer", "start", "end", "style", "name", "marginl", "marginr", "marginv", "effect", "text"]

    line = line.rstrip()
    line = line.replace('\\N', '')
    data = line.split(',', block_count)# 左端からblock_count回だけ分割する
    data = dict(zip(formats, data))
    data['text'] = data['text'].split('}')
    pos = data['text'][0]
    pos = pos.strip('{')
    content = data['text'][1]
    data['text'] = {"pos": pos, "content": content} #posとcontentを分離して辞書に保存
    return data

def has_eos(txt0):
    txt = list(txt0)

    if "｡" in txt or "?" in txt or "!" in txt or "！" in txt or "？" in txt or "《" in txt or "》" in txt:
        return True 
    else:
        return False

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
#         'text': {
#               'pos': '\\pos(500,1020)\\c&H00ffff&',
#               'content': '見えない世界の扉が開く｡'
#                       }
#         },
# ]
def parse_data_from_file(file_name):
    with open(file_name,"r",encoding="utf-8_sig") as f:
        data = []
        for line in f.readlines():
            #先頭がDialogueでなければskip
            if (re.match(r'^Dialogue:', line) == None):
                continue

            #layer, start, end, textなど要素を分解して辞書にいれて返す
            data.append(split_by_comma(line))
        return data

file_name = "./2020_01_05_Sun_0900_0930_ch8_A_.ass"
# file_name = "./result.txt"

data = parse_data_from_file(file_name)

idx = 0
for row in data:
    

    idx += 1

    #layer, start, end, textなど要素を分解して辞書にいれて返す
    #((label 1)) #textに文末文字が含まれているか判定する
        #文末文字がなければ
            #文末文字が出てくるまでtextを連結する(次の行を解析する)
        #文末文字が末尾で見つかったら
            #前の文にすべての文を連結して終了する
        #文末文字が途中で見つかったら
            #最初の文末文字まで前の文に連結
            #前の文のtext以外のデータを複製し、(label1に戻って)文末文字以降の文字列を解析する
