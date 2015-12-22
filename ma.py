# coding=utf-8

from csvdata import *

class ma:
    ma_idx = {
        5: 0,
        10: 1,
        20: 2,
        30: 3,
        60: 4,
        120: 5,
    }
    def __init__(self):
        self.macfg = [5, 10, 20, 30, 60, 120]
        self.ma_number = len(self.macfg)
        self.result_list = []


    def calc(self, datalist):
        first_calc = [False, False, False, False, False, False]
        eachresult = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        pop_price = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        queue = [[], [], [], [], [], []]
        for i, data in enumerate(datalist):
            datadate = data[0]
            end_price = float(data[1])
            for ma_num in self.macfg:
                idx = self.ma_idx[ma_num]
                data_queue = queue[idx]
                data_queue.append(end_price)
                length = len(data_queue)

                #add a queue to calc ma price
                if length == ma_num:
                    if first_calc[idx] == False:
                        average_price = sum(data_queue)/length
                        first_calc[idx] = True
                    else:
                        # an accelerate method to calc average, keep precision in calc
                        average_price = eachresult[idx] + (end_price - pop_price[idx]) / ma_num
                    eachresult[idx] = average_price
                    pop_price[idx] = data_queue.pop(0)

            result = [datadate]
            for i in range(self.ma_number):
                round_price = round(eachresult[i], 3)
                result.append(round_price)
            self.result_list.append(result)

    def update(self, ma_file, datafile, datalist, period='d'):
        first_calc = [False, False, False, False, False, False]
        ma_result = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]          #this data calc each ma result
        prev_manum_price = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]   # prev manum data
        queue = [[], [], [], [], [], []]   # each hold queue for hold prev n data
        madata = csvdata(ma_file)
        data = csvdata(datafile)
        end_price_array = data.get_elem_list_last_n('end_val', self.macfg[-1] + len(datalist))
        end_price_array = end_price_array[:-len(datalist)]

        end_price_number = len(end_price_array)
        ma_last_data = madata.read_last()
        new_ma_result_list = []
        # build ma need result, includes last ma_number endprice and last ma_result
        for ma_num in self.macfg:
            idx = self.ma_idx[ma_num]
            data_queue = queue[idx]
            ma_result[idx] = float(ma_last_data[idx + 1]) # +1 for first is date

            if end_price_number < ma_num:
                last_n_data = map(lambda  x: float(x[1]), end_price_array[-end_price_number:])
                prev_manum_price[idx] = None
            else:
                last_n_data = map(lambda  x: float(x[1]), end_price_array[1-ma_num:])
                prev_manum_price[idx] = float(end_price_array[-ma_num][1])
            data_queue.extend(last_n_data)

        for i, data in enumerate(datalist):
            datadate = data[0]
            end_price = float(data[1])
            for ma_num in self.macfg:
                idx = self.ma_idx[ma_num]
                data_queue = queue[idx]
                data_queue.append(end_price)
                length = len(data_queue)

                #add a queue to calc ma price
                if length == ma_num:
                    if first_calc[idx] == False:
                        average_price = sum(data_queue)/length
                        first_calc[idx] = True
                    else:
                        # an accelerate method to calc average, keep precision in calc
                        average_price = ma_result[idx] + (end_price - prev_manum_price[idx]) / ma_num
                    ma_result[idx] = average_price
                    prev_manum_price[idx] = data_queue.pop(0)
            result = [datadate]
            for i in range(self.ma_number):
                try:
                    round_price = ma_result[i]
                    print "i: %s, price: %s, type:%s"%(i, round_price, type(round_price))
                    round_price = round(round_price, 3)
                    result.append(round_price)
                except:
                    print ma_result[i]
                    print i
            new_ma_result_list.append(result)
        # finally add all calc result to db
        madata.append_data(new_ma_result_list, period)

    def store(self, output_file):
        if self.result_list:
            store = csvdata(output_file)
            store.write(self.result_list)
            self.result_list = []

if __name__ == '__main__':
    path = os.path.join(os.getcwd(), 'stockdata', '603999_读者传媒')
    ma_obj = ma()
    data = csvdata(os.path.join(path, 'day.csv'))
    ma_obj.update(os.path.join(path, 'day_ma.csv'), os.path.join(path, 'day.csv'), data.get_elem_list_last_n('end_val', 5))
    #ma_obj.calc(data.get_elem_list('end_val'))
    #ma_obj.store(os.path.join(path, 'day_ma.csv'))