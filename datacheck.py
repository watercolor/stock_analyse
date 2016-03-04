# coding=utf-8
# This file is used to generate week.csv and month.csv
# because we found that the SOHU data get week and month data lose some first weeks and months data
# and this will cause MACD caculate error

import os
from parse_yaml import *
from stock_cfg import *
from csvdata import *
from util_date import *

class datacheck:
    def __init__(self, filepath):
        self.filepath = filepath
        self.daydata   = csvdata(os.path.join(filepath, 'day.csv'))
        self.weekdata  = csvdata(os.path.join(filepath, 'week.csv'))
        self.monthdata = csvdata(os.path.join(filepath, 'month.csv'))
        self.daydata.read()
        self.weekdata.read()
        self.monthdata.read()

    def check_period(self, daydata, w_m_data, cmp_func, newfile, force = False):
        if daydata.len() == 0:
            return
        first_date = get_elem(daydata.read_index(0), 'date')

        if w_m_data.len() != 0:
            first_date2 = get_elem(w_m_data.read_index(0), 'date')
        if w_m_data.len() != 0 and cmp_func(first_date, first_date2) and force == False:
            return True
        else:
            new_data_list = []
            data_same_period = []
            min_val = 0.0
            max_val = 0.0
            volume = 0.0
            volume_money = 0.0
            diff = 0.0
            diff_ratio = 0.0
            last_date = None
            weekstart = True
            last_end_val = 0.0
            start_val = 0.0
            end_val = 0.0
            for idx, data in enumerate(self.daydata):
                # not same week, record last week data
                if data_same_period != [] and cmp_func(get_elem(data, 'date'), get_elem(data_same_period[-1], 'date')) is False:
                    week_data = [last_date, "%.2f" % start_val, "%.2f" % end_val, diff, diff_ratio,
                                  "%.2f" % min_val, "%.2f" % max_val, volume, "%.2f"%volume_money, 0.0]
                    new_data_list.append(week_data)
                    last_end_val = end_val
                    data_same_period = []
                    weekstart = True
                if weekstart == True:
                    weekstart = False
                    start_val = float(get_elem(data, 'start_val'))
                    min_val = float(get_elem(data, 'low_val'))
                    max_val = float(get_elem(data, 'high_val'))
                    volume = 0.0
                    volume_money = 0.0
                else:
                    min_val = min(min_val, float(get_elem(data, 'low_val')))
                    max_val = max(max_val, float(get_elem(data, 'high_val')))


                data_same_period.append(data)
                volume = volume + float(get_elem(data, 'volume'))
                volume_money = volume_money + float(get_elem(data, 'volume_money'))
                end_val = float(get_elem(data, 'end_val'))
                if last_end_val != 0:
                    diff = '%.2f'%(end_val - last_end_val)
                    diff_ratio = '%.2f%%'%(((end_val-last_end_val)/last_end_val)*100)
                else:
                    diff = "0.00"
                    diff_ratio = "0.00%"
                last_date = get_elem(data, 'date')
            week_data = [last_date, "%.2f" % start_val, "%.2f" % end_val, diff, diff_ratio,
                                  "%.2f" % min_val, "%.2f" % max_val, volume, "%.2f"% volume_money, 0.0]
            new_data_list.append(week_data)
            newdata = csvdata(os.path.join(self.filepath, newfile))
            newdata.write(new_data_list)
            print "Update %s data to %s "%(self.filepath, newfile)

    def check_week(self, newfile = 'week_new.csv'):
        self.check_period(self.daydata, self.weekdata, issameweek, newfile)

    def check_month(self, newfile = 'month_new.csv'):
        self.check_period(self.daydata, self.monthdata, issamemonth, newfile)

def algodata_check(datafile, fullpath):
    algo_prefix = ["_ma.csv", "_macd.csv"]
    algo_src = []
    datapath = os.path.join(fullpath, datafile)
    datasrc = csvdata(datapath)
    for algo in algo_prefix:
        algofile = datafile[0: datafile.index('.')] + algo
        algofilepath = os.path.join(fullpath, algofile)
        algo_src.append(csvdata(algofilepath))

    for data in datasrc:
        finddate = data[0]
        excep = False
        for algo in algo_src:
            if algo.hasdate(finddate):
                continue
            else:
                excep = True
                print "%s dos not have date %s, break"%(algo.filename(), finddate)
        if excep:
            break


if __name__ == "__main__":
    stockcode = StockCode()
    for code in stockcode:
        str = code + '_' + stockcode.getname(code)

        codepath = os.path.join(os.getcwd(), 'stockdata', str)
        check_elem = datacheck(codepath)
        check_elem.check_week()
        check_elem.check_month()
