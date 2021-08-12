import os
import glob
import re

    #a[0] = Format: Layer
    #a[1] = Start
    #a[2] = End
    #a[3] = Style (Default|Rubi)
    #a[4] = Name (空白) 
    #a[5][6][7] = MarginL, MarginR, MarginV, (大体全部0000)
    #a[8][9] = 空白
    #a[10][11] = Effect 
    #a[12] = Text
    #print(a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8],a[9],a[10],a[11],a[12])

def eos(txt0):

    txt = list(txt0)

    #print(txt)
    #print("".join(txt))

    if "｡" in txt or "?" in txt or "!" in txt or "！" in txt or "？" in txt or "《" in txt or "》" in txt:

        return 1 
    else:
        return 0
        
sw = 0 
t = []
tr = 0

sennum = 1

#print(t[1],t[2],t[3],t[10],t[11],t[12])

with open(r"C:\Users\Ryu\tvjimaku\tvprogMoti\ASS\202001\2020_01_05_Sun_0900_0930_ch8_A_.ass","r",encoding="utf-8_sig") as f:
    
    for line in f.readlines():
        line = line.rstrip()
        line = line.replace("\\N", "")


        a = re.split(',|{|}', line)
        
        if a[0] == "Dialogue: 0" and a[3] == "Default":
            if sw == 0: #一文目の処理
                t = a
                if eos(a[-1]) == 1:
                    print(sennum, t[1],t[2],t[3],t[10],t[11]," ".join(t[12:]))
                else:
                    pass
                sw += 1
                sennum += 1

            else: #二文目以降
            
                if eos(a[-1]) == 0: #文末記号なしのとき
                    t = a
                    #t.append(a[-1])
                    tr = 1
                else: #文末記号ありのとき
                    if tr == 1: #t[12]以降が複数文で構成されているとき
                        t.append(a[-1])
                        print(sennum, t[1],t[2],t[3],t[10],t[11]," ".join(t[12:]))
                        """a.clear()
                        t.clear()"""
                        sennum += 1

                    else: #t[12]が一文だけで完結するとき
                        t = a
                        print(sennum, t[1],t[2],t[3],t[10],t[11],t[12])

                        sennum += 1

                    for k in range (12, len(t)-1):
                        t.pop(k)

                    tr = 0
