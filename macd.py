# coding=utf-8

from stock_cfg import *
from csvdata import *
from stockelem import *
from util_date import *
class macd:
    '''
    EMA（12）= 前一日EMA（12）×11/13＋今日收盘价×2/13
    EMA（26）= 前一日EMA（26）×25/27＋今日收盘价×2/27
    DIFF    = 今日EMA（12）- 今日EMA（26）
    DEA     = 前一日DEA×8/10＋今日DIF×2/10
    MACD    = 2×(DIFF－DEA)

    '''
    IDX_DATE = 0
    IDX_DIFF = 1
    IDX_DEA_IDX = 2
    IDX_MACD_IDX = 3
    IDX_EMA_SHORT = 4
    IDX_EMA_LONG = 5
    IDX_DEA_IDX2 = 6
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
        self.store_file = None

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
                result = [data_date, round(0.0, 3), round(dea, 3), round(0.0, 3), ema_short, ema_long, dea]
                self.result_list.append(result)
            else:
                ema_short = ema_short * (self.short - 2)/self.short + end_val * 2/self.short
                ema_long = ema_long * (self.long - 2)/self.long + end_val * 2/self.long
                ema_short = round(ema_short, 4)
                ema_long = round(ema_long, 4)

                diff = ema_short - ema_long
                dea = dea * (self.m - 2)/self.m + diff * 2/self.m
                dea = round(dea, 4)

                macd = 2*(diff - dea)
                result = [data_date, round(diff, 3), round(dea, 3), round(macd, 3), ema_short, ema_long, dea]
                self.result_list.append(result)

    def set_store_file(self, file):
        self.store_file = file

    def update(self, macd_file, today_data, period='d'):
        macddata = csvdata(macd_file)
        lastdata = macddata.read_last()
        if lastdata == None:
            self.calc(today_data)
            self.store(macd_file)
            return

        ema_short = float(lastdata[self.IDX_EMA_SHORT])
        ema_long = float(lastdata[self.IDX_EMA_LONG])
        dea = float(lastdata[self.IDX_DEA_IDX2])
        result = []
        for data in today_data:
            end_price = float(data[1])

            ema_short = ema_short * (self.short - 2)/self.short + end_price * 2/self.short
            ema_long = ema_long * (self.long - 2)/self.long + end_price * 2/self.long
            ema_short = round(ema_short, 4)
            ema_long = round(ema_long, 4)

            diff = ema_short - ema_long
            dea = dea * (self.m - 2)/self.m + diff * 2/self.m
            dea = round(dea, 4)
            macd = 2*(diff - dea)
            result.append([data[0], round(diff, 3), round(dea, 3), round(macd, 3), ema_short, ema_long, dea])
        macddata.append_data(result, period)

    def store(self, output_file):
        if self.result_list:
            store = csvdata(output_file)
            store.write(self.result_list)
            self.result_list = []


if __name__ == '__main__':
    path = os.getcwd() + os.sep + 'stockdata' + os.sep + "000002_万科A" + os.sep
    ma = macd()
    data = csvdata(path + 'day.csv')
    ma.update(path + 'day_macd.csv', data.read_last())
    #src = csvdata('/tmp/stock.csv')
    #ma = macd()
    #ma.calc(src.get_elem_list('end_val'))
    #ma.store('/tmp/macd.csv')