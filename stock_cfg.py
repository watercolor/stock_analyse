
import yaml
import os
class stock_cfg:
    cfgfile = os.getcwd() + os.sep + "stock_cfg.yaml"

    def __init__(self):
        with open(self.cfgfile) as fd:
            self.cfg = yaml.load(fd)

    def get_startdate(self):
        return self.cfg['begin_date']

    def get_enddate(self):
        return self.cfg['end_date']


