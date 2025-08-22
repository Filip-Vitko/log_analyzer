import re
import os
import pathlib
import datetime
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter
from dataclasses import dataclass
from typing import List, Dict, Tuple
import timeit

SCRIPT_DIR = Path(__file__).parent.resolve()

my_dict = {"INFO" : 0, "WARNING" : 0, "ERROR" : 0, "DEBUG" : 0}
path = SCRIPT_DIR / "example.log"
my_list_2 = []
def version_1(path, my_list_2):
    with path.open(mode='r', encoding='utf-8') as file:
        for log_line in file:
            my_list_2.append(str(re.search(r"INFO|WARNING|ERROR|DEBUG" , log_line).group()))

        info_couter = Counter(my_list_2)
    my_list_2.clear()
    
def version_2(path):
    couter = Counter()
    with path.open(mode='r', encoding='utf-8') as file:
        for log_line in file:
            match = re.search(r"INFO|WARNING|ERROR|DEBUG" , log_line)
            if match:
                couter[match.group()] += 1


os.system('cls' if os.name == 'nt' else 'clear')

for _ in range(5):
    time_taken1 = timeit.timeit(lambda: version_1(path, my_list_2), number=1)
    time_taken2 = timeit.timeit(lambda: version_2(path), number=1)

    print(f"Time for test_function1: {time_taken1:.5f} seconds")
    print(f"Time for test_function2: {time_taken2:.5f} seconds")

    if time_taken1 < time_taken2:
        print("test_function1 is faster", end="\n\n")
    else:
        print("test_function2 is faster", end="\n\n")

#output()
print(Path.cwd())
print(SCRIPT_DIR)
my_list = list(Path(SCRIPT_DIR).iterdir())
if my_list:
    for item in my_list:
        x = str(item)
        y = re.search(r"\.log", x)
        if y:
            print(y.group())
            break

def _my_generator():
    with path.open(mode='r', encoding='utf-8') as file:
        for log_line in file:
            yield log_line

output = _my_generator()

def _iter_lines():
    path = SCRIPT_DIR / "example.log"
    with path.open(mode='r', encoding='utf-8') as file:
        for line in file:
            yield line

output = _iter_lines()
for i in output:
    print(i)
    print(type(i))

my_dict = {'2025-08-07': 4, '2025-08-08': 1}
for key, val in my_dict.items():
    print(key, val)