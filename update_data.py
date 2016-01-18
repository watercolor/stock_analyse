# coding=utf-8

from parse_yaml import *
from sohu_data import *
from stock_cfg import *
from util_date import *
from macd import *
from ma import *
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
    datefile = date_file()
    startdate = datefile.getnext()

    day_handle = update_data(startdate=startdate, enddate=todaystr(), period='d')
    week_handle = update_data(startdate=startdate, enddate=todaystr(), period='w')
    month_handle = update_data(startdate=startdate, enddate=todaystr(), period='m')
    for code in stockarray:
        #if int(code) < 600279:
        #    continue
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
            price_data = data.get_elem_list_last_n('end_val', 1)
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
            price_data = data.get_elem_list_last_n('end_val', 1)
            #price_data = data.get_elem_list_date_range('end_val', "2015-12-16", "2016-01-14")
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
            #if dirname < "000589":
            #    continue
            fullpath = os.path.join(parent,dirname)
            print "Enter " + fullpath
            for datafile in basefiles:
                func(datafile, fullpath)

datefile=date_file()
update_today()
algo_update()
datefile.update()
