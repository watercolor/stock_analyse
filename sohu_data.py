# coding=utf-8
import urllib2
import json, csv, os
from stockdata import *
from datetime import date
from csvdata import *
class SohuData:
    """ fetch sohu stock data
    """
    baseurl = "http://q.stock.sohu.com/hisHq?"
    basecallback = "historySearchHandler"
    def __init__(self, code, startdate=None, enddate=None, period = "d"):
        self.code = code
        today = date.today()
        if startdate == None:
            self.startdate = str(today.year) + str(today.month) + str(today.day - 1)
        else:
            self.startdate = startdate

        if enddate == None:
            self.enddate = str(today.year) + str(today.month) + str(today.day)
        else:
            self.enddate = enddate
        self.period = period
        self.fetchurl = None
        self.data_fetched = None
        self.data_json = None

    def fetchdata(self):
        if self.fetchurl == None:
            self.genurl()
        #print self.fetchurl
        data = urllib2.urlopen(self.fetchurl)
        for line in data:
            line = line.decode('gbk')
            self.data_fetched = line
            break
        #print self.data_fetched[22:-3]
        self.format_data(self.data_fetched[22:-3])

    def genurl(self):
        "http://q.stock.sohu.com/hisHq?code=cn_300228&start=20150130&end=20151231&stat=1&order=D&period=m&callback=historySearchHandler&rt=xml"
        geturl = SohuData.baseurl \
                 + "code=cn_" + self.code \
                 + "&start=" + self.startdate \
                 + "&end=" + self.enddate \
                 + "&stat=1&order=D" \
                 + "&period=" + self.period \
                 + "&callback=" + self.basecallback \
                 + "&rt=jsonp"
        self.fetchurl = geturl
        return self.fetchurl

    def format_data(self, data):
        try:
            self.data_json = json.loads(data)
            if 'hq' not in self.data_json.keys():
                self.data_json = None
        except ValueError:
            self.data_json = None
            print "fetch %s data error"%(self.code)
        #print jsonobj
        #print jsonobj['hq'][1]
        #tt = StockData(jsonobj['hq'][1])

    def store_csv(self, inputfile='/tmp/stock.csv'):
        if self.data_json != None:
            csv_data = csvdata(inputfile)
            csv_data.write(self.data_json['hq']
        else:
            print "Store to " + inputfile + " failed. Data not fetched, maybe code error."


if __name__  == "__main__":
    test = SohuData("600000")#, "20151101", "20151127")
    test.fetchdata()
    test.store_csv()