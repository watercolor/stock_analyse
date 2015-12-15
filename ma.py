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

    def update(self, ma_file, datalist, period='d'):
        pass
    #     eachresult = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    #     pop_price = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    #     queue = [[], [], [], [], [], []]
    #     madata = csvdata(ma_file)
    #     for ma_num in self.macfg:
    #         idx = self.ma_idx[ma_num]
    #         data_queue = queue[idx]
    #
    #         data_queue.append(end_price)
    #         length = len(data_queue)

    def store(self, output_file):
        if self.result_list:
            store = csvdata(output_file)
            store.write(self.result_list)
            self.result_list = []

if __name__ == '__main__':
    path = os.path.join(os.getcwd(), 'stockdata', '000002_万科A')
    ma_obj = ma()
    data = csvdata(os.path.join(path, 'day.csv'))
    ma_obj.calc(data.get_elem_list('end_val'))
    ma_obj.store(os.path.join(path, 'day_ma.csv'))