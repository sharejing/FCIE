#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re
import collections


def load_pattern(pattern_file=r'/root/NER/Date/date_pattern.txt'):
    """
    在文件中读取匹配模式
    :param pattern_file: 存储 pattern 的文件
    :return: pattern 列表
    """
    _patterns = []
    with open(pattern_file, 'r', encoding='utf-8') as f:
        for line in f:
            p_l = line.strip()
            if p_l:
                _patterns.append(p_l)
    # print("Loaded pattern from %s" % pattern_file)
    return _patterns


def find_date(s, patterns=None):
    """
    根据 pattern 在 s 中匹配出相应的子串
    :param s: 待匹配字符串
    :param patterns: 匹配模式
    :return: 匹配到的子串列表
    """

    if not patterns:
        patterns = load_pattern()

    assert isinstance(patterns, (list, tuple))

    _s = s
    result = []

    for pattern in patterns:
        r_p = re.findall(re.compile(pattern), _s)
        if r_p:
            for q in r_p:
                _s = _s.replace(q, ' ')
                if q == '':
                    r_p.remove(q)
        result.extend(r_p)

    result_c = collections.Counter(result).most_common()

    result_and_index = []

    for r_c in result_c:
        if r_c[1] > 1:
            index = []
            r_c_index = s.find(r_c[0])
            while r_c_index != -1:
                index.append(r_c_index)
                r_c_index = s.find(r_c[0], r_c_index + 1)
            assert len(index) == r_c[1]
            for i in index:
                result_and_index.append(tuple([r_c[0], i]))

        else:
            result_and_index.append(tuple([r_c[0], s.find(r_c[0])]))

    results = []
    for r, i in sorted(result_and_index, key=lambda x: x[1]):
        results.append(r)

    if not results:
        return 'undefined'
    else:
        return results[-1]


if __name__ == '__main__':
    patterns = load_pattern(pattern_file="date_pattern.txt")
    result = find_date('今天是星期一，2019年，7月', patterns)
    print(result)
