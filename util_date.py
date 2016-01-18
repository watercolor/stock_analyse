import time
from datetime import date, datetime, timedelta
def gen_datestr(today_val):
    y = str(today_val.year)
    m = str(today_val.month)
    d = str(today_val.day)
    if len(m) < 2:
        m = '0' + m
    if len(d) < 2:
        d = '0' + d
    return y + m + d

def todaystr():
    today_val = date.today()
    return gen_datestr(today_val)

def date_sub(day1, day2):
    d1_y, d1_m, d1_d = int(day1[:4]), int(day1[5:7]), int(day1[8:])
    d2_y, d2_m, d2_d = int(day2[:4]), int(day2[5:7]), int(day2[8:])
    d1 = datetime(d1_y, d1_m, d1_d)
    d2 = datetime(d2_y, d2_m, d2_d)
    return (d1-d2).days

def isleapyear(year):
    if year % 4 ==0 and (year % 100 != 0 or year % 400 == 0):
        return True
    else:
        return False

def month_days(datestr):
    d1_y, d1_m, d1_d = int(datestr[:4]), int(datestr[5:7]), int(datestr[8:])
    days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    day_calc = days[d1_m]

    if isleapyear(d1_y) and d1_m == 2 and d1_d == 29:
        day_calc += 1

    return day_calc

def issameweek(day1, day2):
    cal1 =  format_date(day1)
    cal2 =  format_date(day2)
    return cal1.isocalendar()[1] == cal2.isocalendar()[1]

def issamemonth(day1, day2):
    d1_m = int(day1[5:7])
    d2_m = int(day2[5:7])
    if d1_m == d2_m:
        return True
    else:
        return False

def next_n_day(datestr, number):
    olddate = format_date(datestr)
    newdate = olddate + timedelta(number)
    if '-' in datestr:
        newstr = str(newdate.year) + "-%02d"%(newdate.month) + "-%02d"%(newdate.day)
    else:
        newstr = str(newdate.year) + "%02d"%(newdate.month) + "%02d"%(newdate.day)
    return newstr

def format_date(datestr):
    if '-' in datestr:
        return datetime.strptime(datestr, "%Y-%m-%d")
    else:
        return datetime.strptime(datestr, "%Y%m%d")

def date_index(date_list, finddate,left_find=False):
    outrange = False
    if finddate in date_list:
        return date_list.index(finddate)

    if left_find:
        enddate = format_date(date_list[0])
    else:
        enddate = format_date(date_list[-1])
    while finddate not in date_list:
        if left_find:
            finddate = next_n_day(finddate, -1)
            if format_date(finddate) < enddate:
                outrange = True
                break
        else:
            finddate = next_n_day(finddate, 1)
            if format_date(finddate) > enddate:
                outrange = True
                break;

    if outrange == False:
        return date_list.index(finddate)
    else:
        return None

class date_file:
    def __init__(self, datefile = None):
        self.lastdate = None
        if datefile ==  None:
            self.lastdate_file = os.path.join(os.getcwd(), "stockdata", "last_record_date")
        else
            self.lastdate_file = datefile
        with open(self.lastdate_file) as fd:
            self.lastdate = fd.read()

    def getnext(self, flush = False, next_n = 1):
        if flush:
            return "19910101"
        else:
            return next_n_day(self.lastdate, next_n)

    def getdate(self):
        return self.lastdate

    def update(self, datestr = todaystr()):
        with open(self.lastdate_file, 'w') as fd:
            fd.write(datestr)

#ddd=["1990-01-01", "1990-01-02", "1990-01-04", "1990-01-06"]
#print date_index(ddd, "1989-12-31", False)

