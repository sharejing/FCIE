# @File  : demo_month.py
# @Author: Yimin Jing
# @Date  : 2019/8/6
# @Desc  : 本地测试程序-抽取月份

import code
import sys

from Date.month_recognize import find_month

sys.path.append("/root/FCIE")


def process(sentence: str):
    print(find_month(sentence))


banner = """
Interactive month Recognize
>> process(sentence)
"""


def usage():
    print(banner)


code.interact(banner=banner, local=locals())
