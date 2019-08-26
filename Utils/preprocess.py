"""
对ASR识别的错误进行纠正
对一些影响解析结果的的错误进行纠正
"""

import re
from Utils.question_ids import NR_list


def number_recognize_ec(q_id: str, sent: str) -> str:
    """
    Number recognize error correction
    :param q_id: Question id
    :param sent: Sentence
    :return:
    """
    # 去除停用词
    for s in ("一下", "一点", "想一想", "一共", "一直", "不一等", "不一定", "一定", "一些"):
        sent = sent.replace(s, '')

    # 去除干扰
    if q_id.endswith(("0601", "0705", "0711", "0712")):
        sent = sent.replace("一个月", ' ')
    if q_id.endswith("0502"):
        sent = sent.replace("一天", ' ')

    for s in ("一个都没有", "一个也没有", "一个都没", "一个也没", "一个人都没有", "一个人也没有", "没啥人"):
        sent = sent.replace(s, "没有")

    # 二十多万 -> 二十万
    # 2019-08-13
    if "多万" in sent:
        index = sent.index("多万") - 1
        if sent[index] in ('十', '百', '千'):
            sent = sent.replace("多万", "万")
    sent = sent.replace("来万", "万")

    # ASR结果纠错
    # Special examples
    for s in ("梨园", "李元", "李艳", "李毅", "林源", "林园", "林燕"):
        sent = sent.replace(s, "零元")
    sent = sent.replace("医院", "一元")
    sent = sent.replace("武清", "五千")
    sent = sent.replace("死亡", "四万")
    sent = sent.replace("齐家", "七家")
    sent = sent.replace("有加", "六家")

    return sent


def error_correction(q_id: str, sent: str) -> str:
    """
    Error correction before process
    :param q_id: Question id
    :param sent: Sentence
    :return:
    """
    # 这儿加一个NR的
    if q_id in NR_list:
        sent = number_recognize_ec(q_id, sent)

    # Classification
    if q_id.endswith("0101"):
        # 为什么您手头这么多现金呢？
        for s in ("告知资产", "公司资产"):
            sent = sent.replace(s, "购置资产")
        for s in ("点错",):
            sent = sent.replace(s, "填错")

    if q_id.endswith("0104"):
        # 剩下的钱从哪里出？
        for s in ("重生一", "重申一", "从声音"):
            sent = sent.replace(s, "从生意")
        for s in ("里面转", "里面找", "里面赚", "里面砸", "里砸", "里展"):
            sent = sent.replace(s, "里面攒")
        sent = sent.replace("李娜", "里拿")
    if q_id.endswith("0401"):
        # 请问您贷款用途是准备用于生意上，还是家庭消费？
        for s in ("由于", "英语", "有一", "用一"):
            sent = sent.replace(s, "用于")
        for s in ("本身一", "本身已", "本身硬", "本身以", "本升一", "本身印"):
            sent = sent.replace(s, "本生意")
        for s in ("声音", "生一", "十一", "三七"):
            sent = sent.replace(s, "生意")
        sent = sent.replace("开心的", "开新的")
        sent = sent.replace("正确", "证券")
        sent = sent.replace("抓紧消费", "家庭消费")
    if q_id.endswith("0402"):
        for s in ("声音", "生一"):
            sent = sent.replace(s, "生意")
    if q_id.endswith("0404"):
        # 您的贷款具体是用于什么？
        sent = sent.replace("近", "进")
        sent = sent.replace("没车", "买车")
        sent = sent.replace("支付公司", "支付工资")
    if q_id.endswith("0405"):
        # 其他生意的经营规模是否大于您这次申请贷款的生意呢？
        sent = sent.replace("大爷", "大于")
        sent = sent.replace("不搭理", "不大于")
    if q_id.endswith("0407"):
        sent = sent.replace("晶莹", "经营")
    if q_id.endswith("0501"):
        # 您是经营什么行业的？是服务业还是贸易类，或者其他生意呢？
        sent = sent.replace("问题用品", "文体用品")
        sent = sent.replace("仿制品", "纺织品")
        sent = sent.replace("灵寿", "零售")
        sent = sent.replace("金银", "经营")
        for s in ("销户", "消户", "消火", "小伙", "小火"):
            sent = sent.replace(s, "销货")
        for s in ("报一", "猫也", "猫一"):
            sent = sent.replace(s, "贸易")
        sent = sent.replace("屏幕一类", "偏贸易类")
        sent = sent.replace("天猫也累了", "偏贸易类")
        sent = sent.replace("孟磊", "贸易类")
    if q_id.endswith("0503"):
        sent = sent.replace("一个人", " ")
        sent = sent.replace("以前", "一千")
    if q_id.endswith("0505"):
        # 您是否会给客户办理会员卡这种类似储值卡的服务吗？
        sent = sent.replace("补办", "不办")
        sent = sent.replace("有伴", "有办")
        sent = sent.replace("半了", "办了")
    if q_id.endswith("0507"):
        # 目前有几家公司或者个人在给您供货？
        sent = sent.replace("李佳", "五家")
        sent = sent.replace("顾家", "五家")
        sent = sent.replace("酒家", "九家")
    if q_id.endswith("0602"):
        for s in ('勾', '攻', '购'):
            sent = sent.replace(s, "够")
    if q_id.endswith(("0702", "0708")):
        # 昨天生意比平时差吗？
        # 昨天的生意比平时要好吗？
        for s in ("一半", "一班"):
            sent = sent.replace(s, "一般")
    if q_id.endswith("0703"):
        # 您生意现在处于淡季吗？
        sent = sent.replace("单机", "淡季")
        sent = sent.replace("忘记", "旺季")
        sent = sent.replace("不但不旺", "不淡不旺")
    if q_id.endswith(("0704", "0801")):
        sent = sent.replace('邮', '有')
        sent = sent.replace('幼', '有')
        sent = sent.replace("友友", "有有")
    if q_id.endswith("0709"):
        # 昨天有其他非常规收入？
        sent = sent.replace("非常贵", "非常规")
        sent = sent.replace('邮', '有')
        sent = sent.replace('幼', '有')
        sent = sent.replace("友友", "有有")
    if q_id.endswith("0801"):
        # 您在过去半年有3万元以上的大额支出吗？
        sent = sent.replace("ｅ", "呃")
        sent = sent.replace("ｕ", "有")
    if q_id.endswith("0804"):
        # 生意上赚到的钱您一般怎么花？
        for s in ("声音", "生一", "十一"):
            sent = sent.replace(s, "生意")
        sent = sent.replace("陈银行", "存银行")
        sent = sent.replace("流程", "留存")
        sent = sent.replace("刘在生意", "留在生意")
        sent = sent.replace("没有引力", "没有盈利")
    if q_id.endswith("0901"):
        sent = sent.replace("公司", "工资")
    if q_id.endswith("0902"):
        sent = sent.replace("一个月", ' ')

    return sent


def no_listen(sent: str):
    """
    处理 没听清 这类问题
    """
    if re.findall(re.compile("没听清|没听到|你说什么|你说啥|再说一遍|再说一次|是什么|指什么|是啥|不好意思"), sent):
        return "undefined"
    else:
        return "continue"
