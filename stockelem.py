# coding=utf-8

DATE=0
STARTPRICE=1
ENDPRICE=2
DIFF_PRICE=3
DIFF_RATIO=4
LOW_PRICE=5
HIGH_PRICE=6
VOLUME=7
VOLUME_MONEY=8
CHANGE_RATIO=9

class StockElem():
    def __init__(self, data):
        self.date = data[DATE]
        self.start_val = float(data[STARTPRICE])
        self.end_val = float(data[ENDPRICE])
        self.diff_val = float(data[DIFF_PRICE])
        pos = data[DIFF_RATIO].find('%')
        self.diff_ratio = float(data[DIFF_RATIO][:pos])/100
        self.high_val = float(data[HIGH_PRICE])
        self.low_val = float(data[LOW_PRICE])
        self.volume = int(data[VOLUME])  # 单位 手
        self.volume_money = float(data[VOLUME_MONEY]) # 单位 万
        pos = data[CHANGE_RATIO].find('%')
        self.change_ratio = float(data[CHANGE_RATIO][:pos])/100

    def dump(self):
        print u"日期: " + self.date
        print u"开盘: %.2f"%(self.start_val)
        print u"收盘: %.2f"%(self.end_val)
        print u"最高: %.2f"%(self.high_val)
        print u"最低: %.2f"%(self.low_val)
        print u"涨跌额: %.2f"%(self.diff_val)
        print u"涨跌幅: %.4f"%(self.diff_ratio)
        print u"成交量: %f"%(self.volume)
        print u"成交额: %f"%(self.volume_money)
        print u"换手率: %.4f"%(self.change_ratio)
