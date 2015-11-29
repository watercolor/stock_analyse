# coding=utf-8

import os
from parse_yaml import *
from sohu_data import *
from stockdata import *

stockarray = StockCode()

basedir = os.getcwd() + "/stockdata"
startdate = "20150101"
enddate   = "20151127"
if os.path.exists(basedir) == False:
    os.mkdir(basedir)
for code in stockarray:
    name = stockarray.getname(code)
    csv_dir = basedir + '/' + code + '_' + name
    if os.path.exists(csv_dir) == False:
        os.mkdir(csv_dir)
    csv_file = csv_dir + '/' + enddate + ".csv"
    print "Fetch %-6s(%s)"%(name, code)
    sohudata = SohuData(code, startdate, enddate)
    sohudata.fetchdata()
    print "Store data to " + csv_file
    sohudata.store_csv(csv_file)
