# @File  : binary_classification.py
# @Author: Yimin Jing
# @Date  : 2019/8/20
# @Desc  : 将所有二分类函数分开写，形成可插拔式函数模块

import re
from Number.number_recognize import extract_integer_number_from_text


def q_0103(question_id: str, answer: str) -> str:
    """
    您是要全款付还是分期付？
    """

    if re.findall(r"全款|一次|一回|一下|一笔|一单|一批|一口气|一锤子|全额|全部付清|直接付完", answer):
        # 全款
        return '1'
    elif re.findall(r"分期|半|两|二|三|四|五|六|七|八|九|十|一年|多期|分摊|平摊", answer):
        # 分期
        return '2'
    else:
        if question_id.startswith('C'):
            return '2'
        else:
            return "undefined"


# 2019/8/21新增
def q_0110(question_id: str, answer: str) -> str:
    """
    当时向别借钱是用于什么？
    """

    if re.findall(r"买|进|开|想|要|做|用|拿|准备|计划|打算|着手|正在", answer):
        # 打算购买或投资什么等合理理由
        return '1'
    elif re.findall(r"嫖|赌|毒|股票|证券|理财|债券|基金|保险|期货|信托|外汇|金属|贵金属|黄金|古董|房产|房地产|借贷", answer):
        # 违规违法或风险投资等不合理理由
        return '2'
    else:
        if question_id.startswith('C'):
            return '1'
        else:
            return "undefined"


def q_0402(question_id: str, answer: str) -> str:
    """
    请问您是打算用在当前的生意上还是您另外其它的生意上呢？
    """
    if re.findall(r"当前|刚才|本|此|这个|现在|目前|正说的|现阶段|只有一个|就一个|就这一个|没有别的|没有其它|没有其他|哪有其它|哪有其他|哪有别的|只有|仅|贷款用的", answer):
        # 当前的生意
        return '1'
    elif re.findall(r"其它|其他|另外|另一个|还有|别的|再开|以前的生意|之前的生意", answer):
        # 其它生意
        return '2'
    else:
        if question_id.startswith('C'):
            return '1'
        else:
            return "undefined"


def q_0403(question_id: str, answer: str) -> str:
    """
    您是指会用于理财、股市等投资方面吗？
    """

    if re.findall(r"不是|不会|不.*能|不存在|没有", answer):
        # 否
        return '0'
    elif re.findall(r"[是会对]", answer):
        # 是
        return '1'
    else:
        if question_id.startswith('C'):
            return '1'
        else:
            return "undefined"


def q_0405(question_id: str, answer: str) -> str:
    """
    其他生意的经营规模是否大于您这次申请贷款的生意呢？
    """

    if re.findall(r"不是|没有|差不多|一样|反正|还那样|但是|少一|好一|小|不大|不大于|现在.*大|就这一个", answer):
        # 否
        return '0'
    elif re.findall(r"是|对|当然|另外|另一|要开一|要新开一|比现在大|比现在这个.*大|比这个大|大于|大一.*", answer):
        # 是
        return '1'
    else:
        if question_id.startswith('C'):
            return '1'
        else:
            return "undefined"


def q_0406(question_id: str, answer: str) -> str:
    """
    您其他的生意是工程相关的行业吗？
    """

    if re.findall(r"不是|没有|当然不|肯定不|必须不|怎么.*能|哪能", answer):
        # 否
        return '0'
    elif re.findall(r"是|对|当然|肯定|必须|一定|废话", answer):
        # 是
        return '1'
    else:
        if question_id.startswith('C'):
            return '1'
        else:
            return "undefined"


def q_0407(question_id: str, answer: str) -> str:
    """
    您贷款成功后，是否还会继续经营用于申请贷款的生意？
    """

    # 处理这类回答：我经营啊，不经营我吃什么
    if "不经营" in answer:
        answer = answer.replace("不经营", "")
        if "经营" in answer:
            return "1"
        else:
            return "0"

    if re.findall(r"不是|不会|不.*经营|不一定|不确定|不好说|说不准|再看|再议", answer):
        # 否
        return '0'
    elif re.findall(r"是|会|对|肯定|当然|继续|经营|只有.{,2}一个", answer):
        # 是
        return '1'
    else:
        if question_id.startswith('C'):
            return '1'
        else:
            return "undefined"


# 2019/8/21新增
def q_0501(question_id: str, answer: str) -> str:
    """
    请问您经营的生意是偏贸易类还是偏服务类呢？
    """

    if re.findall(
            re.compile(
                ("服务|咨询|资讯|售后|保养|维护|维修|修理|培修|商店|饭店|酒店|餐饮|宾馆|盒饭|便当|小吃|快餐|外卖|烤肉|"
                 "烧烤|火锅|门诊|诊所|餐厅|餐馆|美容|美发|理发|健康|保健|调理|足疗|按摩|桑拿|刮痧|拔罐|火罐|针灸|公益|医疗|"
                 "媒体|传媒|广告|出版|教育|培训|学术|大学|研究|科研|化学|生物|地理|地质|农业|旅游|法律|司法|警察|消防|军队|"
                 "财务|会计|网络|互联网|万维网|因特网|计算机|微机|电脑|软件|开发|码农|代码|设计|艺术|运输|邮政|快递|司机|开车|"
                 "出租|计程|货车|卡车|吊车|叉车|体校|健身|健美|瑜伽|游泳|球|攀岩|蹦极|银行|金融|音乐|娱乐|网吧|桌游|棋牌|密室|"
                 "轰趴|舞蹈|跳舞|伴舞|伴奏|乐器|演唱|唱歌|演戏|演员|汽修|汽配|洗碗|洗衣|洗车")
            ), answer):
        # 服务类
        return '03'
    elif re.findall(
            re.compile(
                ("贸易|生意|卖|销售|机械|制造|房地产|房产|别墅|二手房|租赁|小店|门市房|建筑|汽车|跑车|二手车|房车|电瓶|"
                 "电动|自行|用品|电子|数码|零售|批发|服装|衣服|母婴|文具|纸张|木材|木头|农产品|畜牧|养|杀|宰|农民|种地|务农|"
                 "乳制|豆制|菌类|肉|蛋|茶|水果|咖啡|酒|药|超市|开店|进货|销货")
            ), answer):
        # 贸易类
        return '02'
    else:
        if question_id.startswith('C'):
            return '03'
        else:
            return "undefined"


def q_0505(question_id: str, answer: str) -> str:
    """
    您是否会给客户办理会员卡这种类似储值卡的服务吗？
    """

    if re.findall(r'不会|不办|不给|没有|不提供', answer):
        # 否
        return '0'
    elif re.findall(r'会|办|当然|有|嗯', answer):
        # 是
        return '1'
    else:
        if question_id.startswith('C'):
            return '1'
        else:
            return "undefined"


def q_0602(question_id: str, answer: str) -> str:
    """
    您的利润是否够您还每个月的贷款？
    """

    # 处理这类回答：本来是有些不够的，但借了钱之后就够了
    if "不够" in answer:
        answer = answer.replace("不够", "")
        if "够" in answer:
            return "1"
        else:
            return "0"

    if re.findall(r"不够|不行|有点|有些|够呛", answer):
        # 否
        return '0'
    elif re.findall(r"够|当然|没.*问题|差不多|肯定|一点问题也没有|对啊|可以", answer):
        # 是
        return '1'
    else:
        if question_id.startswith('C'):
            return '1'
        else:
            return "undefined"


def q_0702(question_id: str, answer: str) -> str:
    """
    昨天生意比平时差吗？
    """
    if re.findall(
            re.compile(
                "不是|不差|没有|一般|好一|否|还那样|差不多|比平时.*好|不比平时差|都还行|都还可以|还行|就那样|没开门|没营业"
            ), answer):
        # 否
        return '0'
    elif re.findall(re.compile("是|嗯|不好|差一些|差一点|比平时.*差|比平常.{,2}差|不比平时好|少一"), answer):
        # 是
        return '1'
    else:
        if question_id.startswith('C'):
            return '0'
        else:
            return "undefined"


def q_0703(question_id: str, answer: str) -> str:
    """
    您生意现在处于淡季吗？
    """
    # 去除调侃疑问句 "是不是淡季" 无意义
    answer = answer.replace("是不是淡季", " ")

    # 处理双重否定表肯定的答案
    for s in ("不是旺季", "不算旺季", "不处于旺季"):
        if s in answer:
            answer = answer.replace(s, "淡季")
    for s in ("不是淡季", "不算淡季", "不处于淡季"):
        if s in answer:
            answer = answer.replace(s, "旺季")

    if re.findall(re.compile("不是|不算|不淡|差不多|没有|旺季|不处于|处于旺季|一般|比平时.{,2}好"), answer):
        # 否
        return '0'
    elif re.findall(re.compile("是|淡季|处于|处于淡季|比平时.{,2}差|有一点"), answer):
        # 是
        return '1'
    else:
        if question_id.startswith('C'):
            return '1'
        else:
            return "undefined"


def q_0704(question_id: str, answer: str) -> str:
    """
    除了现在我们聊的这个生意外，您还有其他收入来源吗？
    """

    if re.findall(r"没有|没", answer):
        # 否
        return '0'
    elif re.findall(r"有", answer):
        # 是
        return '1'
    else:
        if question_id.startswith('C'):
            return '1'
        else:
            if 'ｕ' in answer:
                return '1'
            else:
                return "undefined"


def q_0708(question_id: str, answer: str) -> str:
    """
    昨天的生意比平时要好吗？
    """

    if re.findall(r"不是|没有|不对|不好|还那样|还好|还行|差不多|一样|正常|一般", answer):
        # 否
        return '0'
    elif re.findall(r"是|对|好|当然|比平时.*好", answer):
        # 是
        return '1'
    else:
        if question_id.startswith('C'):
            return '1'
        else:
            return "undefined"


def q_0709(question_id: str, answer: str) -> str:
    """
    昨天有其他非常规收入吗？
    """

    if re.findall(r"没有|没", answer):
        # 否
        return '0'
    elif re.findall(r"有", answer):
        # 是
        return '1'
    else:
        if question_id.startswith('C'):
            return '1'
        else:
            return "undefined"


# 2019/8/21新增
def q_0713(q_id: str, answer: str) -> str:
    """
    您最近什么原因店里没有收入？
    """
    if re.findall(r'只有|过节|放假|旅游|陪|玩|疼|痛|送|医院|看|病|家|乡|婚|孩|有事|事情|丢|找不着|补办|去世|过世', answer):
        # 客户进货去了，只有昨天没有营业额，或其他合理原因
        return '1'
    elif re.findall(r'工商|消防|税务|装修|风|雨|冰雹|雪|天气|地震|火|窃|偷|盗', answer):
        # 其它会极大影响客户生意的原因（店铺被工商局等要求关闭、店铺周边装修、主要店员生病、客户或家人生病）
        return '2'
    else:
        if q_id.startswith('C'):
            return '2'
        else:
            return "undefined"


def q_0801(question_id: str, answer: str) -> str:
    """
    您在过去半年有3万元以上的大额支出吗？
    """

    answer = answer.replace("有没有", " ")

    if re.findall(r"没有|没", answer):
        # 否
        return '0'
    elif re.findall(r"有|嗯|买了", answer):
        # 是
        return '1'
    else:
        if question_id.startswith('C'):
            return '1'
        else:
            extracted_int = extract_integer_number_from_text(answer)

            if extracted_int != "undefined":
                if int(extracted_int) > 30000:
                    return "1"
                else:
                    return "undefined"
            else:
                return "undefined"


def q_0806(question_id: str, answer: str) -> str:
    """
    除了偿还债务之外您还有其他的大额开支吗？
    """

    if re.findall(r"没有|没", answer):
        # 否
        return '0'
    elif re.findall(r"有", answer):
        # 是
        return '1'
    else:
        if question_id.startswith('C'):
            return '1'
        else:
            return "undefined"
