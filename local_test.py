#!/usr/bin/env python
# -*- coding:utf-8 -*-

import code
import requests


def process(question_id: str, sentence: str):
    data = {
        "outPutASR": sentence,
        "questionId": question_id.upper()
    }

    if len(sentence.strip()) == 0:
        print("This sentence is a null string!")
    else:
        try:
            return requests.post("http://10.24.248.90:5001/register", data=data).text
        except BaseException:
            return "undefined"


banner = """
Interactive Froad Company IE v1.0
>> process(question_id, sentence)
"""


def usage():
    print(banner)


code.interact(banner=banner, local=locals())
