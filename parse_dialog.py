# open_file = "./2020_01_05_Sun_0900_0930_ch8_A_.ass"
open_file = "./result.txt"

with open(open_file,"r",encoding="utf-8_sig") as f:
    for line in f.readlines():
        line = line.rstrip()
        print(f'1:{line}')

        #まず,で区切った配列を用意する
        #タイムスタンプなどの情報を保持
        #
