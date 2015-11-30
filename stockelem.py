# coding=utf-8

class StockData():
    def __init__(self, data):
        self.date       = data[0]
        self.start_val  = data[1]
        self.end_val    = data[2]
        self.diff_val   = data[3]
        self.diff_ratio = data[4]
        self.high_val   = data[6]
        self.low_val    = data[5]
        self.volume     = data[7]       #单位 手
        self.volume_money = data[8]     #单位 万
        self.change_ratio = data[9]

    def dump(self):
        print u"日期: " + self.date
        print u"开盘: " + self.start_val
        print u"收盘: " + self.end_val
        print u"最高: " + self.high_val
        print u"最低: " + self.low_val
        print u"涨跌额: " + self.diff_val
        print u"涨跌幅: " + self.diff_ratio
        print u"成交量: " + self.volume
        print u"成交额: " + self.volume_money
        print u"换手率: " + self.change_ratio

