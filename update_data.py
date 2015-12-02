# coding=utf-8

import os
from datetime import date
from parse_yaml import *
from sohu_data import *
from stockelem import *
from stock_cfg import *

class update_data:
    basedir = os.getcwd() + os.sep + "stockdata"

    def __init__(self, startdate=None, enddate=None):
        today = date.today()
        if startdate == None:
            self.startdate = str(today.year) + str(today.month) + str(today.day - 1)
        else:
            self.startdate = startdate

        if enddate == None:
            self.enddate = str(today.year) + str(today.month) + str(today.day)
        else:
            self.enddate = enddate
        pass

    def update(self, code):
        name = stockarray.getname(code)
        csv_dir = basedir + os.sep + code + '_' + name
        if os.path.exists(csv_dir) == False:
            os.mkdir(csv_dir)
        csv_file = csv_dir + os.sep + "20151127" + ".csv"
        print "Fetch %-6s(%s)" % (name, code)
        sohudata = SohuData(code, self.startdate, self.enddate)
        sohudata.fetchdata()
        print "Store data to " + csv_file
        sohudata.store_csv(csv_file)

stockarray = StockCode()
cfg = stock_cfg()
basedir = os.getcwd() + os.sep + "stockdata"
startdate = cfg.get_startdate()
enddate = cfg.get_enddate()

if os.path.exists(basedir) == False:
    os.mkdir(basedir)

update_handle = update_data(startdate= enddate, enddate=todaystr())
for code in stockarray:
    update_handle.update(code)
