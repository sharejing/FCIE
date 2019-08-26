#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re
from Utils.arabic_transform import covert_chinese_to_arabic, arabic2chinese_in_text


def month_convert(month: str) -> int:
    num_dict = {'一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10}
    r = 0
    month = month.replace('月', '')

    if '个多' in month:
        r += 0.5
        month = month.replace('个多', '')
    elif '多个' in month:
        r += 0.5
        month = month.replace('多个', '')
    else:
        month = month.replace('多', '')

    if '个半' in month:
        r += 0.5
        month = month.replace('个半', '')
    elif '半个' in month:
        r += 0.5
        month = month.replace('半个', '')
    else:
        month = month.replace('个', '')

    if not month:
        return r
    if month == "半":
        return r

    _s = re.findall(re.compile('[一二两三四五六七八九]*十[一二两三四五六七八九]*'), month)
    if _s:
        _s = _s[-1].split('十')
        if _s[0]:
            r += num_dict[_s[0][-1]] * 10
        else:
            r += 10
        if _s[1]:
            r += num_dict[_s[1][-1]]
    else:
        r += num_dict[month[-1]]

    return r


def month_convert_from_year(year: str):
    month_num = 0
    if year.endswith('半'):
        year = year[:-1]
        month_num += 6
    year = year.replace('年', '')

    if year == '半':
        month_num = 6
    else:
        year.replace('半', '')
        _month = str(covert_chinese_to_arabic(year))
        if not _month.startswith("Unsupported"):
            month_num += int(_month) * 12

    return month_num


def find_month(m_string):
    try:
        m_string = arabic2chinese_in_text(m_string)
        m = re.findall(re.compile('[半一二两三四五六七八九十0-9]+[多]*个[多|半]*月'), m_string)
        n = re.findall(re.compile('[半一二两三四五六七八九十0-9]+年[半]*'), m_string)

        if m:
            return str(month_convert(m[-1]))
        elif n:
            return str(month_convert_from_year(n[-1]))
        else:
            return "undefined"
    except BaseException:
        return "undefined"


if __name__ == '__main__':
    print(find_month('差不多半个多月吧'))
