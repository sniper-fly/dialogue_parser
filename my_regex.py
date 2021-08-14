import re

eos_pattern = re.compile(r".*?[。｡?!！？》]+")
brackets_eos = re.compile(r"[)）]$")
