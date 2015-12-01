# coding = utf-8

import os
import csv
class csvdata:
    def __init__(self, file):
        self.file = file
        self.data = {}
    def read(self):
        csvfile = file(self.file, 'r')
        reader = csv.reader(csvfile)
        for line in reader:
            self.data[line[0]] = line
        csvfile.close()

    def readdate(self, date):
        if self.data == {}:
            self.read()
        try:
            return self.data[date]
        except KeyError:
            return None


    def write(self, list, overwrite = False):
        if not os.path.exists(self.file):
            csvfile = file(self.file, 'a')
            writer = csv.writer(csvfile)
            #writer.writerow(['日期', '开盘', '收盘', '最高', '最低', '涨跌额', '涨跌幅', '成交量', '成交额', '换手率'])
            writer.writerows(list)
            csvfile.close()
        else:
            if self.data == {}:
                self.read()
            for line in list:
                if overwrite == False and line[0] in self.data.keys():
                    continue
                self.data[line[0]] = line

            csvfile = file(self.file, 'wb')
            writer = csv.writer(csvfile)
            for date, val in self.data.items():
                writer.writerow(val)
            csvfile.close()

    def add(self, list, overwrite = False):
        if self.data != {}:
            for line in list:
                if overwrite == False and line[0] in self.data.keys():
                    continue;
                self.data[line[0]] = line

    def range(self):
        pass

    def dump(self):
        pass


if __name__ == "__main__":
    test = csvdata('/tmp/stock.csv')
    #test.read()
    print test.readdate("2015-11-26")
    tt = []
    aa = ["2015-02-07","14.09","14.09","-0.09","-0.63%","13.95","14.32","1865475","263714.41","1.25%"]
    #tt.append(aa)
    #test.write(tt)
