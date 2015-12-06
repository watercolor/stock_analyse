# coding=utf-8

from stock_cfg import *
from csvdata import *
class macd:
    '''
    EMA（12）= 前一日EMA（12）×11/13＋今日收盘价×2/13
    EMA（26）= 前一日EMA（26）×25/27＋今日收盘价×2/27
    DIFF    = 今日EMA（12）- 今日EMA（26）
    DEA     = 前一日DEA×8/10＋今日DIF×2/10
    MACD    = 2×(DIFF－DEA)

    '''
    def __init__(self, short_day = 12, long_day = 26, m_day= 9):
        self.cfg = stock_cfg()
        cfg_macd = self.cfg.get_macd()
        if cfg_macd != None:
            self.short = cfg_macd[0]
            self.long = cfg_macd[1]
            self.m = cfg_macd[2]
        else:
            self.short = short_day + 1
            self.long = long_day + 1
            self.m = m_day + 1
        self.result_list = []

    def calc(self, data_list):
        ema_short = 0.0
        ema_long = 0.0
        dea = 0.0
        #result_list = []
        for i, data in enumerate(data_list):
            data_date = data[0]
            end_val = float(data[1])
            if i == 0:
                ema_short = end_val
                ema_long = end_val
                dea = 0.0
            else:
                ema_short = ema_short * (self.short - 2)/self.short + end_val * 2/self.short
                ema_long = ema_long * (self.long - 2)/self.long + end_val * 2/self.long
                ema_short = round(ema_short, 4)
                ema_long = round(ema_long, 4)

                diff = ema_short - ema_long
                dea = dea * (self.m - 2)/self.m + diff * 2/self.m
                dea = round(dea, 4)

                macd = 2*(diff - dea)
                result = [data_date, round(diff, 3), round(dea, 3), round(macd, 3)]
                self.result_list.append(result)

    def store(self, output_file):
        if self.result_list:
            store = csvdata(output_file)
            store.write(self.result_list)
            self.result_list = []


if __name__ == '__main__':
    src = csvdata('/tmp/stock.csv')
    ma = macd()
    ma.calc(src.get_elem_list('end_val'))
    ma.store('/tmp/macd.csv')