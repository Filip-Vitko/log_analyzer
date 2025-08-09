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
    time_taken1 = timeit.timeit(lambda: version_1(path, my_list_2), number=100)
    time_taken2 = timeit.timeit(lambda: version_2(path), number=100)

    print(f"Time for test_function1: {time_taken1:.5f} seconds")
    print(f"Time for test_function2: {time_taken2:.5f} seconds")

    if time_taken1 < time_taken2:
        print("test_function1 is faster", end="\n\n")
    else:
        print("test_function2 is faster", end="\n\n")
