import re

def replace_pos_comma_into_semi_colon(line):
    count = 0
    line_len = len(line)
    for i in range(line_len):
        if (line[i] == ','):
            count += 1
        if (count == 10):
            str = list(line)
            str[i] = ""
            return ("".join(str))


def split_by_comma(line):
    block_count = 9

    line = line.rstrip()
    line = line.replace('\\N', '')
    data = line.split(',', block_count)# 左端からblock_count回だけ分割する
    return data


file_name = "./2020_01_05_Sun_0900_0930_ch8_A_.ass"
# file_name = "./result.txt"

with open(file_name,"r",encoding="utf-8_sig") as f:
    for line in f.readlines():
        #先頭がDialogueでなければskip
        if (re.match(r'^Dialogue:', line) == None):
            continue

        data = split_by_comma(line)

        #layer, start, end, textなど要素を分解して辞書にいれて返す
        #((label 1)) #textに文末文字が含まれているか判定する
            #文末文字がなければ
                #文末文字が出てくるまでtextを連結する(次の行を解析する)
            #文末文字が末尾で見つかったら
                #前の文にすべての文を連結して終了する
            #文末文字が途中で見つかったら
                #最初の文末文字まで前の文に連結
                #前の文のtext以外のデータを複製し、(label1に戻って)文末文字以降の文字列を解析する


        print(f'{line}')