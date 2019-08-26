#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
多分类函数
"""

import re


def q_0101(q_id: str, answer: str) -> str:
    """
    为什么您手头这么多现金呢？
    """
    if re.findall(r'要存|在存|再存|准备存|打算存|计划存|要攒|在攒|再攒|准备攒|打算攒|计划攒|要留|在留|再留|准备留|打算留|计划留|筹集|孩子|上学|出国|留学|买房|买车|结婚', answer):
        # 因某些原因正在存钱中
        return '2'
    elif re.findall(r'习惯|存|攒|留', answer):
        # 有储蓄习惯
        return '3'
    elif re.findall(r'借的|借了|借款|贷款|人借|人的|要还|朋友借|朋友的|兄弟借|兄弟的|伙伴借|伙伴的|亲戚借|亲戚的|家里|同学借|同学的|同事借|同事的', answer):
        # 这是向别人借的
        return '4'
    elif re.findall(r'填错|乱填|瞎填|不对|有错|搞错|有误|是有问题|有原因', answer):
        # 表内信息填写错误
        return '5'
    elif re.findall(r'回款|欠款|货款|应收款|收回|回清|结算|结账|结款|结清|清算|周转|打理|赚的|生意好|租|刚收|赚|挣|刚收到|我.*钱|欠我的|卖', answer):
        # 其它原因（应收账款回款，欠款回款）
        return '6'
    elif re.findall(r'管|怎么花|厉害|有钱|就是有|没有为什么|什么为什么|没.*多少|不.*多|其他|其它|别的|不.*便', answer):
        # 拒绝式回复
        return '7'
    elif re.findall(r'购买|买进|买入|买一|买几|买个|买间|买辆|买张|开一|开个|开家|开间|再买|在买|进货|订货|订购|定货|定购|扩张|扩大|投资|投入|投放|最近|马上|立刻', answer):
        # 打算购买或投资什么
        return '1'
    else:
        if q_id.startswith('C'):
            return '6'
        else:
            return "undefined"


def q_0104(q_id: str, answer: str) -> str:
    """
    剩下的钱从哪里来？
    """
    if re.findall(r'[借贷]', answer):
        # 向别人借或向其它机构贷
        return '1'
    elif re.findall(r'攒|赚|存|挣|生意|生一|营业', answer):
        # 在生意里攒
        return '2'
    elif re.findall(r'其它|其他|回款|欠款|应收款|收回|回清|结算|结账|结清|清算|办法|方式|方法|渠道', answer):
        # 其它（例如应收账款回款、保证金返回等）
        return '3'
    else:
        if q_id.startswith('C'):
            return '3'
        else:
            return "undefined"


# 2019/8/21新增
def q_0109(q_id: str, answer: str) -> str:
    """
    请问您这些钱具体的借款渠道是什么？
    """
    if re.findall(r'亲戚|家人|哥|姐|弟|妹|爸|妈|爹|娘|父|母|伯|叔|婶|姑|姨|舅|爷|奶|姥|公|婆|丈|妻|子|女|媳妇|外甥|侄|朋友|兄弟|哥们|老表|校友|学|师|徒|同事|邻居|隔壁|对门|对面|对个|对过', answer):
        # 亲戚/朋友/同学/同事等
        return '1'
    elif re.findall(r'正规|正式|官方|权威|合法|合规|银行|工商|工行|农业|农行|中国|中行|建设|建行|交通|交行|邮政|储蓄|开发|进出口|发展|广发|浦东|浦发|招商|招行|中信|华夏|光大|民生|恒丰|浙商|渤海', answer):
        # 银行/其它金融机构等
        return '2'
    elif re.findall(r'P2P|无抵押|小额|微贷|贷款|抵押|典当|寄卖|回收|互联网金融|互金|网络贷款|网上贷款|网贷', answer):
        # P2P等网贷平台
        return '3'
    elif re.findall(r'一部分|其中|还有|先从|先看|再从|不够|再就是|要不然|或者|另外|同时', answer):
        # 多渠道借
        return '4'
    else:
        if q_id.startswith('C'):
            return '4'
        else:
            return "undefined"


def q_0301(q_id: str, answer: str) -> str:
    """
    我们注意到您的人行征信上有逾期记录，请问是哪些逾期呢？
    """
    if re.findall(r'信用卡', answer):
        # 信用卡
        return '1'
    elif re.findall(r'P2P|无抵押|小额|微贷|贷款|抵押|典当|寄卖|回收|互联网金融|互金|网络贷款|网上贷款|网贷', answer):
        # 网贷
        return '2'
    elif re.findall(r'其它|其他|抵押', answer):
        # 其它贷款
        return '3'
    elif re.findall(r'经营', answer):
        # 经营性贷款
        return '4'
    elif re.findall(r'房贷|公积金', answer):
        # 房贷
        return '5'
    elif re.findall(r'车贷|汽车|消费', answer):
        # 车贷或其它消费贷款
        return '6'
    else:
        if q_id.startswith('C'):
            return '3'
        else:
            return "undefined"


def q_0302(q_id: str, answer: str) -> str:
    """
    为什么会出现逾期呢？
    """
    if re.findall(r'晚|忘|忙|没|穷|不知道', answer):
        # 客户责任
        return '1'
    elif re.findall(r'银行|工作人员|操作员|客服|经理', answer):
        # 银行人为因素
        return '2'
    elif re.findall(r'延|故障|坏|挂|反应|反映|消息|信息|讯息', answer):
        # 银行转账延迟等问题
        return '3'
    else:
        if q_id.startswith('C'):
            return '3'
        else:
            return "undefined"


def q_0303(q_id: str, answer: str) -> str:
    """
    什么时候出现的逾期您还记得吗？
    """
    if re.findall(r'年|好久|很久|挺久|非常久|好长|很长|挺长|非常长|不|忘|六个|七个|八个|九个|十个|十一个', answer):
        # 6个月以前
        return '1'
    elif re.findall(r'礼拜|周|天|阵|最近|不久|刚刚|没多长|没多久|一个|两个|三个|四个|五个', answer):
        # 最近6个月
        return '2'
    elif re.findall(r'还在|还是|目前|依然|逾期中', answer):
        # 逾期中
        return '3'
    else:
        if q_id.startswith('C'):
            return '1'
        else:
            return "undefined"


def q_0401(q_id: str, answer: str) -> str:
    """
    请问您贷款用途是准备用于生意上，还是家庭消费？
    """
    if re.findall(
            r'一|医|生意|贸易|买卖|商业|经营|店铺|商铺|门市房|门面|成本|资金|维护|维修|大修|设备|电机|机器|房租|账单|账款|周转|采购|进货|订货|材料|原料|成品|进|买一批|买一些|工资|薪水|扩大|开店|开新店|开家|开一家',
            answer):
        # 生意上
        return '1'
    elif re.findall(r'二|家|买.*房|看房|购房|换房|置换|装修|精装|家具|家电|电器|买车|买辆车|买一辆车|看车|养车|保养|换车|留学|培训|学习|考|婚|消费', answer):
        # 家庭消费
        return '2'
    elif re.findall(r'三|其它|其他|都', answer):
        # 其它
        return '3'
    else:
        if q_id.startswith('C'):
            return '3'
        else:
            return "undefined"


def q_0404(q_id: str, answer: str) -> str:
    """
    您的贷款具体是用于什么？
    """
    if re.findall(r'买货|送货|进|订|购|原料|材料|成品|店铺|商铺|门市房|门面|扩大|代理', answer):
        # 进货
        return '1'
    elif re.findall(r'成本|工资|薪水|资金|房租|账单|账款|周转', answer):
        # 流动资金周转
        return '2'
    elif re.findall(r'改善|保养|维护|维修|修车|大修|设备|电器|大型|电机|机器|车辆|装修|店里|店内|开家|开新|开店|开一|开两|开三|开几|买.*台|买.*车|买.*房', answer):
        # 购进资产
        return '3'
    else:
        if q_id.startswith('C'):
            return '2'
        else:
            return "undefined"


# 2019/8/21注销
#def q_0501(q_id: str, answer: str) -> str:
#    """
#    您是经营什么行业的？
#    """
#    if re.findall(
#            r'服务|咨询|资讯|售后|保养|维护|维修|修理|培修|商店|饭店|酒店|餐饮|宾馆|盒饭|便当|小吃|快餐|外卖|烤肉|烧烤|火锅|门诊|诊所|餐厅|餐馆|美容|美发|理发|健康|保健|调理|足疗|按摩|桑拿|刮痧|拔罐|火罐|针灸|公益|医疗|媒体|传媒|广告|出版|教育|培训|学术|大学|研究|科研|化学|生物|地理|地质|农业|旅游|法律|司法|警察|消防|军队|财务|会计|网络|互联网|万维网|因特网|计算机|微机|电脑|软件|开发|码农|代码|设计|艺术|运输|邮政|快递|司机|开车|出租|计程|货车|卡车|吊车|叉车|体校|健身|健美|瑜伽|游泳|球|攀岩|蹦极|银行|金融|音乐|娱乐|网吧|桌游|棋牌|密室|轰趴|舞蹈|跳舞|伴舞|伴奏|乐器|演唱|唱歌|演戏|演员',
#            answer):
#        # 服务类
#        return '03'
#    elif re.findall(
#            r'贸易|生意|卖|销售|机械|制造|房地产|房产|别墅|二手房|租赁|小店|门市房|建筑|汽车|汽配|跑车|二手车|房车|电瓶|电动|自行|用品|电子|数码|零售|批发|服装|衣服|母婴|文具|纸张|木材|木头|农产品|畜牧|养|杀|宰|农民|种地|务农|乳制|豆制|菌类|肉|蛋|茶|水果|咖啡|酒|药',
#            answer):
#        # 贸易类
#        return '02'
#    else:
#        if q_id.startswith('C'):
#            return '03'
#        else:
#            return "undefined"


# def q_0508(q_id: str, answer: str) -> str:
#     if re.findall(r'佣金|回扣|报酬', answer):
#         return '1'
#     elif re.findall(r'统一|一致|一样', answer):
#         return '2'
#     elif re.findall(r'自由|没有|随意|随性|任意|弹性|没规定', answer):
#         return '3'
#     else:
#         if q_id.startswith('C'):
#             return '3'
#         else:
#             return "undefined"


def q_0514(q_id: str, answer: str) -> str:
    """
    您的客户一般多久跟您结一次货款？
    """
    if re.findall(r'月|季|年|两周|两个礼拜|两个多礼拜|三周|三个礼拜|三个多礼拜|十五天|二十天|二十五天|三十天|三十五天|四十天|四十五天|五十天', answer):
        # 大于等于1个月
        return '1'
    elif re.findall(r'周|礼拜|四天|五天|六天|七天|八天|九天|十天|十一天|十二天|十三天|十四天|十一二天|十二三天|十三四天', answer):
        # 每周
        return '2'
    elif re.findall(r'每天|一天|天天|每一天|两天|三天|不赊|不欠|不拖|现|一手|当时|当场', answer):
        # 每天
        return '3'
    else:
        if q_id.startswith('C'):
            return '1'
        else:
            return "undefined"


def q_0515(q_id: str, answer: str) -> str:
    """
    这些客户在您这儿拿货多久了？
    """
    if re.findall(r'不久|没多久|没多长|没多少|天|日|号|周|礼拜|一个|两个|三个|四个|五个', answer):
        # 小于6个月
        return '1'
    elif re.findall(r'半年|六个|七个|八个|九个|十个|十一|一年', answer):
        # 6-18个月
        return '2'
    elif re.findall(r'两年|三年', answer):
        # 18个月以上
        return '3'
    else:
        if q_id.startswith('C'):
            return '3'
        else:
            return "undefined"


def q_0516(q_id: str, answer: str) -> str:
    """
    这些客户从你这拿货是怎么结款的？
    """
    if re.findall(r'先钱|先打|先付|先给钱|先支付', answer):
        # 先打款后发货
        return '1'
    elif re.findall(r'当|现|一次性|每|天|日|周|礼拜|月|季|年|微信|支付宝|现金|卡', answer):
        # 现款现货
        return '2'
    elif re.findall(r'先货|先拿货|先取|先给货', answer):
        # 先拿货后打款
        return '3'
    else:
        if q_id.startswith('C'):
            return '2'
        else:
            return "undefined"


#2019/8/21注销
#def q_0713(q_id: str, answer: str) -> str:
#    """
#    您最近什么原因店里没有收入？
#    """
#    if re.findall(r'只有|就|放假|家|乡', answer):
#        return '1'
#    elif re.findall(r'工商|消防', answer):
#        return '2'
#    elif re.findall(r'周边|周围', answer):
#        return '3'
#    elif re.findall(r'生病|医院|医生', answer):
#        return '4'
#    elif re.findall(r'家里|家人', answer):
#        return '5'
#    else:
#        if q_id.startswith('C'):
#            return '1'
#        else:
#            return "undefined"


def q_0804(q_id: str, answer: str) -> str:
    """
    生意上赚到的钱您一般怎么花？
    """
    if re.findall(r'没赚|没盈利|亏损', answer):
        return '1'
    elif re.findall(r'投资|生意|还是|存在|放在|进|扩大|继续|采购|材料|原料', answer):
        return '2'
    elif re.findall(r'偿还|还钱|还款|还其|还别|还另', answer):
        return '3'
    elif re.findall(r'家|怎么花都|就怎么|花了|买|旅游|旅行|培训|学习|上课|上学|读书|教育|出国|留学|生活|日常|正常|消费|金属|收拾|吃|衣|食|住|房|车|还贷款|还啊|还阿|还呀|想怎么就怎么|给.*花|上交|领导|老婆', answer):
        return '4'
    elif re.findall(r'攒|存|银行', answer):
        return '5'
    elif re.findall(r'一部分|大部分|小部分|少部分|一半|多半|要么|或者|其中|不方便|不合适|不想|其它|其他', answer):
        return '6'
    else:
        if q_id.startswith('C'):
            return '6'
        else:
            return "undefined"
