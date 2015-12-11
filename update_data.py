# coding=utf-8

from parse_yaml import *
from sohu_data import *
from stock_cfg import *
from util_date import *
from macd import *

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
        self.stockarray = StockCode()
        self.basedir = os.getcwd() + os.sep + "stockdata"

    def update(self, code, savefile=None):
        name = self.stockarray.getname(code)
        csv_dir = self.basedir + os.sep + code + '_' + name
        if os.path.exists(csv_dir) == False:
            os.mkdir(csv_dir)
        if savefile != None:
            csv_file = savefile
        else:
            csv_file = csv_dir + os.sep + self.namedict[self.period] + ".csv"
        print "Fetch %-6s(%s)" % (name, code)
        sohudata = SohuData(code, self.startdate, self.enddate, self.period)
        sohudata.fetchdata()
        print "Store data to " + csv_file
        sohudata.store_csv(csv_file)

def update_today(flush = False):
    stockarray = StockCode()
    cfg = stock_cfg()
    basedir = os.getcwd() + os.sep + "stockdata"
    lastdate_file = os.getcwd() + os.sep + "last_record_date"
    with open(lastdate_file) as fd:
        lastdate = fd.read()
        startdate = next_n_day(lastdate, 1)

    if flush:
        startdate = "19910101"

    if not os.path.exists(basedir):
        os.mkdir(basedir)

    day_handle = update_data(startdate=startdate, enddate=todaystr(), period='d')
    week_handle = update_data(startdate=startdate, enddate=todaystr(), period='w')
    month_handle = update_data(startdate=startdate, enddate=todaystr(), period='m')
    for code in stockarray:
        #if int(code) < 600279:
        #    continue
        day_handle.update(code)
        week_handle.update(code)
        month_handle.update(code)

    with open(lastdate_file, 'w') as fd:
        fd.write(todaystr())

def macd_calc():
    basedir = os.getcwd() + os.sep + "stockdata"
    ma = macd()
    for parent,dirnames,filenames in os.walk(basedir):
        for dirname in  dirnames:
            fullpath = os.path.join(parent,dirname)
            print "Enter " + fullpath
            filelist = os.listdir(fullpath)
            #print filelist
            for filename in filelist:
                filename_full = fullpath + os.sep + filename
                tmp = filename.split('.')
                macd_name = fullpath + os.sep + tmp[0] + '_macd.csv'
                #print filename_full
                data = csvdata(filename_full)
                ma.calc(data.get_elem_list('end_val'))
                ma.store(macd_name)
                print "Cacl " + macd_name + ' done'
            #    print "parent is:" + parent
            #    print "filename is:" + filename
            #    print "the full name of the file is:" + os.path.join(parent,filename) #输出文件路径信息

update_today()
