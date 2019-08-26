#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
方付通公司信息抽取v1.0 (FCIEv1)
函数入口
"""
import re

from Utils.preprocess import error_correction, no_listen

from Date import day_recognize
from Number import number_recognize
from Classification import binary_classification, multiple_classification
from Entity import entity_recognize
from Utils.question_ids import NR_list, DR_list, ER_list


def get_result(question_id: str, content: str) -> str:
    # 数据前处理 (去除一些停用词和ASR纠错)
    content = error_correction(question_id, content)

    # 处理 没听清 的问题
    ans = no_listen(content)
    if ans == "undefined" and question_id.startswith(('A', 'B')):
        return ans

    # Number recognize
    if question_id in NR_list:
        answer = number_recognize.extract_integer_number_from_text(content)
        if answer == "undefined" and question_id.endswith("0712"):
            for s in ("每天", "天天", "每一天"):
                if s in content:
                    answer = "30"
        if answer == "undefined" and question_id.startswith('C'):
            answer = '0'

    # Day recognize
    elif question_id in DR_list:
        answer = day_recognize.find_day(content)
        if answer == "undefined" and question_id.startswith('C'):
            answer = '0'

    # Entity recognize
    elif question_id in ER_list:
        answer = entity_recognize.find_entity(question_id, content)

    # Classification
    else:
        # Binary Classification
        # Q_0103
        if question_id.endswith("0103"):
            answer = binary_classification.q_0103(question_id, content)
        # Q_0110
        elif question_id.endswith("0110"):
            answer = binary_classification.q_0110(question_id, content)
        # Q_0402
        elif question_id.endswith("0402"):
            answer = binary_classification.q_0402(question_id, content)
        # Q_0403
        elif question_id.endswith("0403"):
            answer = binary_classification.q_0403(question_id, content)
        # Q_0405
        elif question_id.endswith("0405"):
            answer = binary_classification.q_0405(question_id, content)
        # Q_0406
        elif question_id.endswith("0406"):
            answer = binary_classification.q_0406(question_id, content)
        # Q_0407
        elif question_id.endswith("0407"):
            answer = binary_classification.q_0407(question_id, content)
        # Q_0501
        elif question_id.endswith("0501"):
            answer = binary_classification.q_0501(question_id, content)
        # Q_0505
        elif question_id.endswith("0505"):
            answer = binary_classification.q_0505(question_id, content)
        # Q_0602
        elif question_id.endswith("0602"):
            answer = binary_classification.q_0602(question_id, content)
        # Q_0702
        elif question_id.endswith("0702"):
            answer = binary_classification.q_0702(question_id, content)
        # Q_0703
        elif question_id.endswith("0703"):
            answer = binary_classification.q_0703(question_id, content)
        # Q_0704
        elif question_id.endswith("0704"):
            answer = binary_classification.q_0704(question_id, content)
        # Q_0708
        elif question_id.endswith("0708"):
            answer = binary_classification.q_0708(question_id, content)
        # Q_0709
        elif question_id.endswith("0709"):
            answer = binary_classification.q_0709(question_id, content)
        # Q_0713
        elif question_id.endswith("0713"):
            answer = binary_classification.q_0713(question_id, content)
        # Q_0801
        elif question_id.endswith("0801"):
            answer = binary_classification.q_0801(question_id, content)
        # Q_0806
        elif question_id.endswith("0806"):
            answer = binary_classification.q_0806(question_id, content)

        # Multiple Classification
        # Q_0101
        elif question_id.endswith("0101"):
            answer = multiple_classification.q_0101(question_id, content)
        # Q_0104
        elif question_id.endswith("0104"):
            answer = multiple_classification.q_0104(question_id, content)
        # Q_0109
        elif question_id.endswith("0109"):
            answer = multiple_classification.q_0109(question_id, content)
        # Q_0301
        elif question_id.endswith("0301"):
            answer = multiple_classification.q_0301(question_id, content)
        # Q_0302
        elif question_id.endswith("0302"):
            answer = multiple_classification.q_0302(question_id, content)
        # Q_0303
        elif question_id.endswith("0303"):
            answer = multiple_classification.q_0303(question_id, content)
        # Q_0401
        elif question_id.endswith("0401"):
            answer = multiple_classification.q_0401(question_id, content)
        # Q_0404
        elif question_id.endswith("0404"):
            answer = multiple_classification.q_0404(question_id, content)
        # Q_0514
        elif question_id.endswith("0514"):
            answer = multiple_classification.q_0514(question_id, content)
        # Q_0515
        elif question_id.endswith("0515"):
            answer = multiple_classification.q_0515(question_id, content)
        # Q_0516
        elif question_id.endswith("0516"):
            answer = multiple_classification.q_0516(question_id, content)
        # Q_0804
        elif question_id.endswith("0804"):
            answer = multiple_classification.q_0804(question_id, content)
        else:
            answer = "Undefined question_id"

    """
    2019-08-08
    这个部分是用于对类似于 "记不清" 这样对回答进行处理
    """
    if answer == "undefined" and question_id.startswith('B'):
        if re.findall("不记|不清|记不|忘|想不|查不出来|没法查|怎么知道|哪.*知道|那.*知道|没.*印象|不.*清楚|不.*了解|不.*记得", content) and \
                question_id.endswith(("0101", "0108", "0109", "0110", "0111", "0301", "0302", "0303", "0405", "0406",
                                      "0501", "0502", "0503", "0504", "0505", "0506", "0507", "0513", "0514", "0515",
                                      "0516", "0517", "0518", "0701", "0702", "0703", "0704", "0705", "0708", "0709",
                                      "0710", "0711", "0712", "0713", "0801", "0802", "0804", "0805", "0806", "0807",
                                      "0901", "0902")):
            answer = get_result("C" + question_id[1:], content)
        if re.findall("还没|还不|不知|没想|没规划|没计划|没打算|没安排|要等|要看|谁知道|怎么知道|说不准", content) and \
                question_id.endswith(("0102", "0103", "0104", "0105", "0106", "0107", "0401", "0402", "0403", "0404",
                                      "0407", "0601", "0602", "0803")):
            answer = get_result("C" + question_id[1:], content)

    """
    2019-08-20
    解决ASR两遍不识别的问题
    """
    if content == '' and question_id.startswith('B'):
        answer = get_result("C" + question_id[1:], content)

    return answer


if __name__ == '__main__':
    print(get_result("A0801", "十万元以上大开支"))
