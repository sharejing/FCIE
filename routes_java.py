#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from datetime import date, datetime
from flask import Flask, request

from FCIE_v1 import get_result

app = Flask(__name__)


@app.route('/register', methods=['POST'])
def register():
    # Java calls
    sent = request.json['outPutASR']
    q_id = request.json["questionId"]

    answer = get_result(q_id, sent)

    log_path = os.path.join("/root/log_FCIE", "log_" + str(date.today()).replace("-", "_") + ".txt")

    with open(log_path, "a") as f:
        f.write(str(datetime.now()) + "\t" + q_id + "\t" + sent + "\t" + str(answer) + "\n")

    return str(answer)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
