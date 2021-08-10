'''
    Coded by Cho_bo
    
    util.py
        - main에 집어넣기 잡다한 것들만 모아놓은 거
    
    2021-08-09 ~
'''
from pytz import timezone, utc
from typing import List

import datetime
import sys

# String concatenation without '+' for the performance issue
def concat_all(*strings: List[str]) -> str:
    str_list: list = []
    for st in strings:
        str_list.append(st)

    return ''.join(str_list)

# Get Time - KST(GMT+9)
def get_time() -> str:
    now = datetime.datetime.utcnow()
    kst = timezone('Asia/Seoul')
    return utc.localize(now).astimezone(kst).strftime('%Y%m%d_%H%M%S')

def exit_func() -> None:
    sys.exit("Program Terminated Successfully")

class NotDefinedNumberError(Exception):
    def __init__(self):
        super().__init__('Typing non-defined Number.')