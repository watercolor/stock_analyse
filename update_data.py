# coding=utf-8

from parse_yaml import *
from sohu_data import *
from stock_cfg import *
from util_date import *
from macd import *
from ma import *
from util_path import *
from datacheck import *

class update_data:
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
        if not os.path.exists(self.basedir):
            os.mkdir(self.basedir)

    def set_save_dir(self, dirpath):
        self.basedir = dirpath
        if not os.path.exists(self.basedir):
            os.mkdir(self.basedir)

    def update(self, code, savefile=None):
        name = self.stockarray.getname(code)
        csv_dir = self.basedir + os.sep + code + '_' + name
        if os.path.exists(csv_dir) == False:
            oldpath = find_similar_path(code)
            if oldpath:
                os.rename(oldpath, csv_dir)
                #print "rename " + oldpath + " to " + csv_dir
            else:
                os.mkdir(csv_dir)

        if savefile != None:
            csv_file = savefile
        else:
            csv_file = csv_dir + os.sep + self.namedict[self.period] + ".csv"
        print "Fetch %-6s(%s)" % (name, code)
        if os.path.exists(csv_file) == False:
            startdate = "19900101"
        else:
            #startdate = self.startdate
            data = csvdata(csv_file)
            lastdate = data.read_last_date()
            startdate = date_conv_sub_line(lastdate)
        sohudata = SohuData(code, startdate, self.enddate, self.period)
        sohudata.fetchdata()
        print "Store data to " + csv_file
        sohudata.store_csv(csv_file)

def update_today(flush = False):
    stockarray = StockCode()
    cfg = stock_cfg()
    datefile = date_file()
    startdate = datefile.getnext()

    day_handle = update_data(startdate=startdate, enddate=todaystr(), period='d')
    week_handle = update_data(startdate=startdate, enddate=todaystr(), period='w')
    month_handle = update_data(startdate=startdate, enddate=todaystr(), period='m')
    for code in stockarray:
        day_handle.update(code)
        week_handle.update(code)
        month_handle.update(code)


def get_period(filename):
    period_dict = {
          'day.csv': 'd',
         'week.csv': 'w',
        'month.csv': 'm'
    }
    try:
        return period_dict[filename]
    except KeyError:
        return 'd'

def algo_update():
    walk_all_file_do(macd_update)
    walk_all_file_do(ma_update)


def macd_update(datafile, base_path):
    macd_obj = macd()
    datafile_path = os.path.join(base_path, datafile)
    if os.path.exists(datafile_path):
        macdfile_name = datafile.split('.')[0] + '_macd.csv'
        macdfile_path = os.path.join(base_path, macdfile_name)
        data = csvdata(datafile_path)
        if os.path.exists(macdfile_path):
            macdcsvdata = csvdata(macdfile_path)
            macd_last_record_date = macdcsvdata.read_last_date()
            start_date = next_n_day(macd_last_record_date, 1)
            end_date = date_conv_with_line(todaystr())
            #price_data = data.get_elem_list_last_n('end_val', 1)
            price_data = data.get_elem_list_date_range('end_val', start_date, end_date)
            #print price_data
            macd_obj.update(macdfile_path, price_data, period=get_period(datafile))
            print "Update " + macdfile_path + ' done'
        else:
            end_price_all = data.get_elem_list('end_val')
            macd_obj.calc(end_price_all)
            macd_obj.store(macdfile_path)
            print "Create " + macdfile_path + ' done'

def ma_update(datafile, base_path):
    ma_obj = ma()
    datafile_path = os.path.join(base_path, datafile)
    if os.path.exists(datafile_path):
        mafile_name = datafile.split('.')[0] + '_ma.csv'
        mafile_path = os.path.join(base_path, mafile_name)
        data = csvdata(datafile_path)
        if os.path.exists(mafile_path):
            macsvdata = csvdata(mafile_path)
            ma_last_record_date = macsvdata.read_last_date()
            start_date = next_n_day(ma_last_record_date, 1)
            end_date = date_conv_with_line(todaystr())
            #price_data = data.get_elem_list_last_n('end_val', 1)
            price_data = data.get_elem_list_date_range('end_val', start_date, end_date)
            #print price_data
            ma_obj.update(mafile_path, datafile_path, price_data, period=get_period(datafile))
            print "Update " + mafile_path + ' done'
        else:
            end_price_all = data.get_elem_list('end_val')
            ma_obj.calc(end_price_all)
            ma_obj.store(mafile_path)
            print "Create " + mafile_path + ' done'

def walk_all_file_do(func):
    basefiles = ['day.csv', 'week.csv', 'month.csv']
    basedir = os.path.join(os.getcwd() ,"stockdata")
    for parent,dirnames,filenames in os.walk(basedir):
        for dirname in  dirnames:
            fullpath = os.path.join(parent,dirname)
            print "Enter " + fullpath
            for datafile in basefiles:
                func(datafile, fullpath)

datefile=date_file()
update_today()
algo_update()
#walk_all_file_do(algodata_check)
datefile.update()
