# @File  : number_recognize_1.py
# @Author: Yimin Jing
# @Date  : 2019/8/5
# @Desc  : 识别中文文本中的数字，并将其转化为阿拉伯数字

import re
import math
from Utils.arabic_transform import covert_chinese_to_arabic, arabic2chinese_in_text, chinese_to_digit, unit_to_digit


def load_pattern(pattern_file_path: str) -> list:
    """读取日期模式匹配文件"""
    with open(pattern_file_path, "r", encoding="utf-8") as f:
        number_patterns = [line.strip() for line in f]
    return number_patterns


def match_number(text, patterns):
    """给定文本及匹配模式，返回匹配到的数字"""
    number = []
    for p in patterns:
        res = re.findall(p, text)
        if len(res) > 0:
            for r in res:
                if r:
                    number.append(r)
                    text = text.replace(r, "", 1)
    return number


def clean_digits(digits: str) -> str:
    """
    清洗中文汉字数字中的重复现象
    如： "一万一万" -> "一万"  "七千八千" -> "八千"
    """
    # 从偶数位切开，处理完全重复的现象，如："一万一万"，"一百万一百万"，"十二十二"
    if len(digits) % 2 == 0:
        index = len(digits) // 2
        if digits[:index] == digits[index:]:
            return digits[:index]

    # 处理不完全重复的现象，如："七万八万"
    units = ["#", "十", "百", "千", "万"]
    r = "#"
    position = 0
    for idx, char in enumerate(digits):
        if char in units:
            if units.index(char) > units.index(r):
                r = char
                position = idx
            elif units.index(char) == units.index(r):
                return digits[position + 1:]

    return digits


def process_range_digits(digits: str, index: int) -> str:
    """
    处理一些是范围的数字
    如 "十二三万" -> 125000  "一百七八" -> 175
    """
    A = digits[:index] + digits[index + 1:]  # 较大的数
    B = digits[:index + 1] + digits[index + 2:]  # 较小的数
    return str(math.floor((covert_chinese_to_arabic(A) + covert_chinese_to_arabic(B)) / 2))


def process_telephone_number(digits: str) -> str:
    """电话号码按照纯数字输出"""
    telephone_number = ""
    for char in digits:
        telephone_number += str(chinese_to_digit[char])

    return telephone_number


def is_range_digits(digits: str):
    """
    判断一个数字是否范围的数字
    如 "十二三万" -> 125000  "一百七八" -> 175
    如果是，则返回这个范围数划分的索引位置
    """
    flag = False
    index = 0  # 划分的索引位置

    units = ["十", "百", "千", "万", "零"]

    for idx, c in enumerate(digits):
        if c not in units:
            if idx < len(digits) - 1 and digits[idx + 1] not in units:
                flag = True
                index = idx
    if flag:
        return flag, index
    else:
        return flag, -1


def is_telephone_number(digits: str):
    """
    判断是否是电话号码数字(>2),若是直接转化为电话号码输出
    """
    if len(digits) > 2:
        return all([False if char in unit_to_digit.keys() else True for char in digits])
    else:
        return False


def extract_integer_number_from_text(sentence: str) -> str:
    """从文本中抽取整数"""
    try:

        # 1 将文本一致性，所有的阿拉伯数字转中文汉字数字
        sentence = arabic2chinese_in_text(sentence)

        # 2 给定模式，从文本中抽取中文汉字数字
        patterns = load_pattern("/root/FCIE/Number/integer_pattern")
        integers = match_number(sentence, patterns)
        
        # 3 按字符本身所在位置排序
        new_index = []
        for integer in integers:
            new_index.append(sentence.index(integer))
        sorted_integers = sorted(zip(integers, new_index), key=lambda x: x[1])
        new_integers = [integer_index[0] for integer_index in sorted_integers]
        
        # 4 判断抽取出来的数字是否为范围数或者普通数字 (确定的数字)
        if len(new_integers) > 0:
            # 判断是否是"几万"、"十几万"、"几百万"这样的数字
            for integer in new_integers:
                if "几" in integer:
                    new_integers.remove(integer)
            if len(new_integers) == 0:
                return "undefined"

            # 是电话号码
            if is_telephone_number(new_integers[-1]):
                return process_telephone_number(new_integers[-1])

            flag, index = is_range_digits(clean_digits(new_integers[-1]))
            if flag:
                # 是范围数
                return process_range_digits(clean_digits(new_integers[-1]), index)
            else:
                # 是普通数
                return str(covert_chinese_to_arabic(clean_digits(new_integers[-1])))
        else:
            if re.findall(r"没有|没做|没算|没.*生意|没卖钱|没卖货", sentence):
                return str(0)

            else:
                return "undefined"
    except BaseException:
        return "undefined"


def extract_float_number_from_text(sentence: str) -> str:
    """从文本中抽取小数"""

    try:
        # 1 将文本一致性，所有的阿拉伯数字转中文汉字数字
        sentence = arabic2chinese_in_text(sentence)

        # 2 给定模式，从文本中抽取中文汉字数字
        patterns = load_pattern("/root/FCIE/Number/float_pattern")
        floats = match_number(sentence, patterns)

        # 3 将抽取出来的中文数字转化为阿拉伯数字
        if len(floats) > 0:
            real = clean_digits(floats[-1])
            if "%" in real:
                return str(covert_chinese_to_arabic(real.replace("%", "")) / 100)
            elif "百分之" in real:
                return str(covert_chinese_to_arabic(real.replace("百分之", "")) / 100)
            elif "个点" in real:
                return str(covert_chinese_to_arabic(real.replace("个点", "")) / 100)
            elif "成" in real:
                return str(covert_chinese_to_arabic(real.replace("成", "")) / 10)
            else:
                return str(covert_chinese_to_arabic(real) / 100)
        else:
            return "undefined"
    except BaseException:
        return "undefined"
