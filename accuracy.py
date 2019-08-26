"""
计算accuracy脚本
需要在本地运行
"""

import xlrd
import requests

from Utils import question_ids

show_true = False


def process(q_id: str, sentence: str):
    data = {"outPutASR": sentence, "questionId": q_id.upper()}

    if len(sentence.strip()) == 0:
        return "This sentence is a null string!"
    else:
        try:
            return requests.post("http://10.24.248.90:5001/register", data=data).text
        except BaseException:
            return "undefined"


if __name__ == '__main__':
    wb = xlrd.open_workbook(filename="/Users/shark/Desktop/AI问题汇总_v3_0823.xlsx")  # 打开xlsx文件

    sheet1 = wb.sheet_by_index(9)  # 通过索引或表明来获取表格

    question_id = sheet1.col_values(2)[1:]  # 获取列内容
    ASR_answer = sheet1.col_values(5)[1:]
    real_answer = sheet1.col_values(7)[1:]

    count_all = 0  # 有效记录计数
    count_true = 0  # 正确记录计数
    count_undefined = 0  # undefined计数

    for idx, asr, real in zip(question_id, ASR_answer, real_answer):
        if not asr:  # ASR解析为空的为无效记录
            continue
        if str(idx) not in question_ids.BC_list:
            continue

        prediction = process(str(idx), str(asr))

        if prediction == "Undefined question_id":  # 不再使用的问题
            continue

        if isinstance(real, float):
            real = int(real)

        count_all += 1

        if prediction == str(real):
            count_true += 1
            if prediction == "undefined":
                count_undefined += 1
            if show_true:
                print("True ", idx, asr, prediction, real)
        else:
            print("False", idx, asr, prediction, real)

    print("Accuracy: ", count_true, '/', count_all, '(', (count_true / count_all) * 100, '%)')
    print((count_true - count_undefined) / count_all)
