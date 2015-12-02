
from datetime import date
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
