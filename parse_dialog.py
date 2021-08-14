from parse_data_from_file import parse_data_from_file
from split_by_middle_eos import split_by_middle_eos
from join_continuous_sentences import join_continuous_sentences

def print_data(data):
    for row in data:
        print(f'start: {row["start"]}, end: {row["end"]} content: {row["text"]}')

# file_name = "./another.ass"
file_name = "./2020_01_05_Sun_0900_0930_ch8_A_.ass"
data = parse_data_from_file(file_name)
data = split_by_middle_eos(data)
data = join_continuous_sentences(data)

print_data(data)
