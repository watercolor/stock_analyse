# coding=utf-8

class StockElem():
    def __init__(self, data):
        self.date = data[0]
        self.start_val = float(data[1])
        self.end_val = float(data[2])
        self.diff_val = float(data[3])
        pos = data[4].find('%')
        self.diff_ratio = float(data[4][:pos])/100
        self.high_val = float(data[6])
        self.low_val = float(data[5])
        self.volume = int(data[7])  # 单位 手
        self.volume_money = float(data[8]) # 单位 万
        pos = data[9].find('%')
        self.change_ratio = float(data[9][:pos])/100

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
