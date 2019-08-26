# @File  : demo_number.py
# @Author: Yimin Jing
# @Date  : 2019/8/6
# @Desc  : 本地测试程序

import code
import sys

sys.path.append("/root/FCIE")

from Number.number_recognize import extract_integer_number_from_text, \
    extract_float_number_from_text


def process(sentence: str, mode="integer"):
    if mode == "integer":
        print(extract_integer_number_from_text(sentence))
    else:
        print(extract_float_number_from_text(sentence))


banner = """
Interactive Number Recognize
>> process(sentence, mode="integer")
"""


def usage():
    print(banner)


code.interact(banner=banner, local=locals())
