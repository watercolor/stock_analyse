# coding=utf-8

from parse_yaml import *
from sohu_data import *
from stock_cfg import *
from util_date import *


class update_data:
    basedir = os.getcwd() + os.sep + "stockdata"
    namedict = {
        "d": "day",
        "w": "week",
        "m": "month"
    }

    def __init__(self, startdate=None, enddate=None, period="d"):
        if startdate == None:
            self.startdate = todaystr()
        else:
            self.startdate = startdate

        if enddate == None:
            self.enddate = todaystr()
        else:
            self.enddate = enddate
        self.period = period

    def update(self, code):
        name = stockarray.getname(code)
        csv_dir = basedir + os.sep + code + '_' + name
        if os.path.exists(csv_dir) == False:
            os.mkdir(csv_dir)
        csv_file = csv_dir + os.sep + self.namedict[self.period] + ".csv"
        print "Fetch %-6s(%s)" % (name, code)
        sohudata = SohuData(code, self.startdate, self.enddate, self.period)
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

day_handle = update_data(startdate=enddate, enddate=todaystr(), period='d')
week_handle = update_data(startdate=enddate, enddate=todaystr(), period='w')
month_handle = update_data(startdate=enddate, enddate=todaystr(), period='m')
for code in stockarray:
    day_handle.update(code)
    week_handle.update(code)
    month_handle.update(code)
