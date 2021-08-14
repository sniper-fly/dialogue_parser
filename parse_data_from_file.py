import re

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
