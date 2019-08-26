#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re
from Utils.arabic_transform import covert_chinese_to_arabic, arabic2chinese_in_text


def day_convert(day: str) -> str:
    day_int = 0
    if '年' in day:
        if day.count('半') > 1:
            return "undefined"
        if day.endswith('半') or day.startswith('半'):
            day_int += 180
            day = day.replace('半', '')
        day = day.replace('年', '')
        if day:
            day_int += covert_chinese_to_arabic(day) * 365
        return str(day_int)

    if "季度" in day:
        day = day.replace("个季度", '')
        day_int = covert_chinese_to_arabic(day) * 90
        return str(day_int)

    if '月' in day:
        if day.count('半') > 1:
            return "undefined"
        if "个半月" in day:
            day_int += 15
            day = day.replace("个半月", '')
            day_int += covert_chinese_to_arabic(day) * 30
            return str(day_int)
        day = day.replace("个月", '')
        # day = day.replace("月", "")
        if '半' in day:
            day_int += 15
            day = day.replace("半", '')
        if day:
            day_int += covert_chinese_to_arabic(day) * 30
        return str(day_int)

    if '周' in day or "个礼拜" in day or "个星期" in day:
        day = day.replace('周', '')
        day = day.replace("个礼拜", '')
        day = day.replace("个星期", '')
        day_int = covert_chinese_to_arabic(day) * 7
        return str(day_int)

    if '天' in day:
        day = day.replace('天', '')
        day_int = covert_chinese_to_arabic(day)
        return str(day_int)


def find_day(d_string: str) -> str:
    d_string = d_string.replace('多', '')
    try:
        # 1、数字全部转为数字
        d_string = arabic2chinese_in_text(d_string)

        d_string = d_string.replace("俩", "两")

        # 2、正则匹配出所有可能的字符串
        d1 = re.findall(re.compile("[半一二两三四五六七八九十]+年[半]*"), d_string)
        d2 = re.findall(re.compile("[半一二两三四五六七八九十]+个[半]*月"), d_string)
        d3 = re.findall(re.compile("[一二两三四五六七八九十]+周"), d_string)
        d4 = re.findall(re.compile("[一二两三四五六七八九十]+个礼拜"), d_string)
        d5 = re.findall(re.compile("[一二两三四五六七八九十]+个星期"), d_string)
        d6 = re.findall(re.compile("[一二两三四五六七八九十]+天"), d_string)
        d7 = re.findall(re.compile("[一二两三四五六七八九十]+个季度"), d_string)
        # d8 = re.findall(re.compile("[半一二两三四五六七八九十]月"), d_string)
        d = d1 + d2 + d3 + d4 + d5 + d6 + d7
        flag_index = 0
        flag_d = None

        # 3、排序取出最后一个
        for dd in d:
            if d_string.index(dd) >= flag_index:
                flag_index = d_string.index(dd)
                flag_d = dd

        if flag_d is not None:
            # 4、转换为数字
            result = day_convert(flag_d)
            return result
        else:
            # 判断 明天、后天
            if "现在" in d_string:
                return "0"
            if "今天" in d_string:
                return "0"
            if "明天" in d_string:
                return "1"
            if "大后天" in d_string:
                return "3"
            if "后天" in d_string:
                return "2"
            if "下下周" in d_string:
                return "14"
            if "下周" in d_string:
                return "7"
            if "下下个月" in d_string:
                return "60"
            if "下个月" in d_string:
                return "30"
            if "明年" in d_string:
                return "365"
            if "后年" in d_string:
                return "730"
            return "undefined"

    except BaseException:
        return "undefined"


if __name__ == '__main__':
    print(find_day("嗯一个半月"))
    # print(find_day("嗯不是我没有打算吗还没有计划要用这笔钱这是我自己就是攒的养老钱"))
