from lib.parse_data_from_file import parse_data_from_file
from lib.split_by_middle_eos import split_by_middle_eos
from lib.join_continuous_sentences import join_continuous_sentences

def print_data(data):
    idx = 0
    for row in data:
        print(f'{idx}    {row["start"]}    {row["end"]}    {row["style"]}    {row["pos"]}    {row["text"]}')
        idx += 1

# file_name = "./data/another.ass"
file_name = "./data/2020_01_05_Sun_0900_0930_ch8_A_.ass"


data = parse_data_from_file(file_name)
data = split_by_middle_eos(data)
data = join_continuous_sentences(data)

print_data(data)
