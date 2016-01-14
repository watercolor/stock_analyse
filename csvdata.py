# coding=utf-8

import os
import csv
from stockelem import *
from util_date import *
class csvdata:
    name_hash = {
        'date':0,
        'start_val':1,
        'end_val':2,
        'high_val':6,
        'low_val':5,
    }
    def __init__(self, file):
        self.file = file
        self.data = []
        self.datadict = {}

    def read(self, reverse = False):
        if {} == self.datadict and os.path.exists(self.file):
            csvfile = file(self.file, 'r')
            reader = csv.reader(csvfile)
            for line in reader:
                self.datadict[line[0]] = line
            csvfile.close()
            self.data = sorted(self.datadict.iteritems(), key = lambda d:d[0], reverse = reverse)
            #data 为列表结构,每一项数据为(date, data)

    def readdate(self, date):
        self.read()
        try:
            return self.datadict[date]
        except KeyError:
            return None


    def write(self, list, overwrite = False, reverse = False):
        list.sort()
        if reverse:
            list.reverse()
        if not os.path.exists(self.file):
            csvfile = file(self.file, 'w')
            writer = csv.writer(csvfile)
            #writer.writerow(['日期', '开盘', '收盘', '最高', '最低', '涨跌额', '涨跌幅', '成交量', '成交额', '换手率'])
            writer.writerows(list)
            csvfile.close()
        else:
            if overwrite:
                self.read()
                # updata data if set overwrite
                for line in list:
                    self.datadict[line[0]] = line

                # sort data
                self.data = sorted(self.datadict.iteritems(), key = lambda d:d[0], reverse = reverse)

                # store data
                csvfile = file(self.file, 'w')
                writer = csv.writer(csvfile)
                for val in self.data:
                    writer.writerow(val[1])
                csvfile.close()
            else:
                csvfile = file(self.file, 'a')
                writer = csv.writer(csvfile)
                #writer.writerow(['日期', '开盘', '收盘', '最高', '最低', '涨跌额', '涨跌幅', '成交量', '成交额', '换手率'])
                writer.writerows(list)
                csvfile.close()

    def add(self, list):
        self.read()
        # updata data if set overwrite
        for line in list:
            self.datadict[line[0]] = line

        # sort data
        self.data = sorted(self.datadict.iteritems(), key = lambda d:d[0])

    def read_last(self):
        self.read()
        try:
            return self.data[-1][1]
        except IndexError:
            return None

    def read_last_n(self, num):
        self.read()
        try:
            return map(lambda x: x[1], self.data[-num:])
        except IndexError:
            return None

    def read_last_date(self):
        self.read()
        try:
            return  self.data[-1][0]
        except:
            return None

    def del_date(self, date):
        self.read()
        try:
            del self.datadict[date]
            for i, line in enumerate(self.data):
                if line[0] == date:
                    del self.data[i]
        except KeyError:
            return

    def len(self):
        self.read()
        return len(self.data)

    def del_last(self):
        self.read()
        try:
            lastdate = self.data[-1][0]
            del self.data[-1]
            del self.datadict[lastdate]
        except KeyError:
            return

    # 获得一个特定数据的日期+ 数据 列表
    def get_elem_list(self, elemstr):
        if elemstr not in self.name_hash.keys():
            return None
        index = self.name_hash[elemstr]
        result = []
        self.read()
        for elem in self.data:
            result.append([elem[0], elem[1][index]])
        return  result

    def get_elem_list_last_n(self,elemstr, lastnum):
        try:
            index = self.name_hash[elemstr]
            self.read()
            return map(lambda x: [x[0],x[1][index]], self.data[-lastnum:])
        except KeyError:
            return None

    def get_elem_list_date_n(self, elemstr, finddate, count):
        try:
            self.read()
            index = self.name_hash[elemstr]
            date_list = map(lambda x:x[0], self.data)
            date_index = date_list.index(finddate)
            if count > 0:
                if date_index + count > self.len():
                    ret_data = map(lambda x: [x[0],x[1][index]], self.data[date_index:])
                else:
                    ret_data = map(lambda x: [x[0],x[1][index]], self.data[date_index:date_index + count])
            else:
                if date_index - count < 0:
                    ret_data = map(lambda x: [x[0],x[1][index]], self.data[:date_index + 1])
                else:
                    ret_data = map(lambda x: [x[0],x[1][index]], self.data[date_index - count:date_index + 1])
            return ret_data
        except KeyError, IndexError:
            return None

    def get_elem_list_date_range(self, elemstr, startdate, enddate):
        try:
            self.read()
            index = self.name_hash[elemstr]
            date_list = map(lambda x:x[0], self.data)
            start_index = date_index(date_list, startdate)
            end_index = date_index(date_list, enddate, True)
            ret_data = map(lambda x: [x[0],x[1][index]], self.data[start_index : end_index + 1])
            return ret_data
        except (KeyError, IndexError):
            return None

    def range(self):
        pass

    def dump(self):
        self.read()
        for elem in self.data:
            print elem

    def append_data(self, datalist, period='d'):
        if self.len() > 0 and period != 'd':
            last_date = self.read_last_date()
            recv_first_date = datalist[0][0]
            #print "recvdate: " + recv_first_date + " last_date: " + last_date
            deletelast = False
            if period == 'w' and issameweek(last_date, recv_first_date):
                deletelast = True
            elif period == 'm' and issamemonth(last_date, recv_first_date):
                deletelast = True
            if deletelast:
                self.del_last()
                self.write(datalist, overwrite= True)
            else:
                self.write(datalist)
        else:
            self.write(datalist)

if __name__ == "__main__":
    testdata = csvdata('/Users/nzm/code/stock_analyse/stockdata/600000_浦发银行/day.csv')
    print testdata.get_elem_list_date_range('end_val', "2015-12-01", "2015-12-22")
