#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
实体识别
"""

import jieba.posseg


def find_entity(q_id: str, answer: str) -> str:
    """

    :param q_id: question ID
    :param answer: ASR answer
    :return:
    """
    out = [t for t, p in jieba.posseg.cut(answer) if p == 'n']

    # Add
    for a_s in ("运输", "进货", "工资", "运费"):
        if a_s in answer:
            out.append(a_s)

    # 去重
    new_out = []
    for o in out:
        if o not in new_out:
            new_out.append(o)

    # Remove
    for d_s in ("成本", "部分", "店里", "人", "啥意思", "基本上", "桃花", "小伙", "开销", "店面"):
        if d_s in new_out:
            new_out.remove(d_s)

    # Sort
    new_index = []
    for o in new_out:
        new_index.append(answer.index(o))

    new_entity = zip(new_out, new_index)
    new_entity = sorted(new_entity, key=lambda x: x[1])

    if new_entity:
        new_entity = new_entity[:2]
        return ','.join([e[0] for e in new_entity])
    else:
        if q_id.startswith('C'):
            return "人工,房租"
        else:
            return "undefined"


if __name__ == '__main__':
    print(find_entity("A0901", "两三开销主要就是租金和运费"))
