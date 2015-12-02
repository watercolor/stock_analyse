
import shelve
from csvdata import *

class shelve_data:
    def __init__(self, input_file):
        self.file = input_file
        self.data = shelve.open(self.file)
        pass

    def read(self, date):
        try:
            return self.data[date]
        except KeyError:
            return None

    def add(self, date, data):
        self.data[date] = data

    def range(self):
        return self.data['range']

    def newest_date(self):
        return self.data['range'][0]

    def oldest_date(self):
        return self.data['range'][1]

    def newest(self):
        try:
            return self.data[self.newest_date()]
        except KeyError:
            return None

    def __iter__(self):
        return self

    def next(self):
        pass

    def conv_from_csv(self, csvfile):
        csv_data = csvdata(csvfile)
        csv_data.read()
        maxdate = None
        mindate = None
        for data in csv_data.data.values():
            print data
            self.add(data[0], data)
            if data[0] > maxdate or maxdate == None:
                maxdate = data[0]
            if data[0] < mindate or mindate == None:
                mindate = data[0]
        print "MaxDate: " + maxdate + " MinDate: " + mindate
        self.data['range'] = [maxdate, mindate]

        self.data.close()

ttt = shelve_data('/tmp/shelve_data_test')
#ttt.conv_from_csv('/tmp/stock.csv')
print ttt.read('2015-11-27')

