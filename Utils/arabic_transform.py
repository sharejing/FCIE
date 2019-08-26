# @File  : utils.py
# @Author: Yimin Jing
# @Date  : 2019/8/5
# @Desc  : 一些核心转化函数
import re

# 单位字典bit_to_unit，例如 (2: "十")表示给定的字符是两位数，那么返回的结果一定包含"十"。3/4/5/9以此类推
bit_to_unit = {2: "十", 3: "百", 4: "千", 5: "万", 9: "亿"}
unit_to_digit = {"十": 10, "百": 100, "千": 1000, "万": 10000, "亿": 100000000}
digit_to_chinese = {"0": "零", "1": "一", "2": "二", "3": "三", "4": "四",
                    "5": "五", "6": "六", "7": "七", "8": "八", "9": "九"}
chinese_to_digit = {"零": 0, "一": 1, "二": 2, "两": 2, "三": 3, "四": 4,
                    "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}


def convert_arabic_to_chinese(digits):
    """
    将纯阿拉伯数字转化为中文汉字数字
    如：18 -> 一十八
    """

    def wrapper(u):
        """
        针对多位连续 "零"的简单去重函数
        如："一百零零" -> "一百"  "一千零零一" -> "一千零一"
        """
        if "零零" in u:
            return wrapper(u.replace("零零", "零"))

        return u[:-1] if u[-1] == "零" else u

    def transform(digits, bit):
        """
        转化函数
        digits: 纯阿拉伯数字字符串
        bit: 该数字的位数，即字符串的长度
        """
        # 如果是一位数，则直接按照digit_to_chinese返回对应汉字
        if bit == 1:
            return digit_to_chinese[digits]

        # 否则，如果第一个字符是"0"，则省略"单位"字符，返回零和剩余字符的递归字符串
        if digits[0] == "0":
            return wrapper("%s%s" % ("零", transform(digits[1:], bit - 1)))

        # 否则，如果是2/3/4/5/9位数，那么返回最高位数的字符串"数值" + "单位" + "剩余字符的递归字符串"
        if bit < 6 or bit == 9:
            return wrapper("%s%s%s" % (digit_to_chinese[digits[0]], bit_to_unit[bit], transform(digits[1:], bit - 1)))

        # 否则，如果是6/7/8位数，那么用"万"字将字符串从万位数划分位两部分，再对这两个部分进行递归
        # 如：137890，则为 13 + "万" + "7890"，再对划开的两个部分递归
        if bit < 9:
            return "%s%s%s" % (transform(digits[:-4], bit - 4), "万", transform(digits[-4:], 4))

        # 否则，如果是10位数及以上，用"亿"仿照上面进行划分
        if bit > 9:
            return "%s%s%s" % (transform(digits[:-8], bit - 8), "亿", transform(digits[-8:], 8))

    return transform(digits, len(digits))


def covert_chinese_to_arabic(chinese):
    """
    将中文汉字数字转化为纯阿拉伯数字
    如：六百二十四 -> 624
    """
    units = list(unit_to_digit.keys())
    chine = list(chinese_to_digit.keys())

    def wrapper(v):
        """
        处理中文汉字数字中一些特殊省略、约数等现象
        如：一百二 -> 一百二十  七八百 -> 八百
        """

        # 一百七八 -> 一百七   一万七八 -> 一万七
        if len(v) > 2 and v[-1] in chine[1:] and v[-2] in chine[1:] and v[-3] in units[1:]:
            v = v[:-1]

        # 一百五 -> 一百五十
        if len(v) > 2 and v[-1] in chine and v[-2] in units[1:]:
            v += units[units.index(v[-2]) - 1]

        # 一百十五 -> 一百一十五
        if "十" in v:
            index = v.index("十")
            if index == 0 or v[index - 1] in units:
                v = v[:index] + "一" + v[index:]

        # 解决三类问题：(百八十 -> 八十) (百 -> 一百) (十三 -> 一十三)
        flag = -1
        for digit in v:
            if digit in chine and flag == -1:
                flag = v.index(digit)
        if flag == -1 and v != "":
            v = "一" + v
        else:
            v = v[flag:]

        return v

    def to_digit(v):
        """完备的中文汉字数字转阿拉伯数字"""
        omit_flag = 0
        results = 0
        r = 1  # 进率
        base = 0  # 基础进率

        for i in range(len(v) - 1, -1, -1):
            val = dict(unit_to_digit, **chinese_to_digit).get(v[i])
            if val >= 10 and i == 0:
                omit_flag = 0
                if val > r:
                    r = val
                    results += val
                else:
                    r *= val
            elif val >= 10:
                omit_flag = 0
                if val > r:
                    r = val
                    base = r
                else:
                    r = base * val
            else:
                if omit_flag == 0:
                    omit_flag = 1
                    results += r * val
        return results

    def transform(chinese):

        chinese = wrapper(chinese)

        if len(chinese) == 0:
            return 0

        if len(chinese) == 1:
            return chinese_to_digit[chinese]

        if "万" not in chinese and "亿" not in chinese:
            return to_digit(chinese)

        if "亿" in chinese:
            parts = chinese.split("亿")
            return transform(parts[0]) * 100000000 + transform(parts[1])

        if "万" in chinese:
            parts = chinese.split("万")
            return transform(parts[0]) * 10000 + transform(parts[1])

    return transform(chinese)


def arabic2chinese_in_text(text):
    """将文本中的阿拉伯数字转化为中文汉字数字"""
    for digits in re.findall(re.compile("[0-9]+"), text):
        text = text.replace(digits, convert_arabic_to_chinese(digits))
    return text

# print(covert_chinese_to_arabic("十五六"))
