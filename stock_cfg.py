
import yaml
import os
class stock_cfg:
    cfgfile = os.getcwd() + os.sep + "config.yaml"
    cfg = None
    def __init__(self):
        if self.cfg == None:
            with open(self.cfgfile) as fd:
                self.cfg = yaml.load(fd)
        else:
            pass

    def get_startdate(self):
        return self.cfg['begin_date']

    def get_enddate(self):
        return self.cfg['end_date']

    def get_macd(self):
        try:
            return [self.cfg['macd']['short'], self.cfg['macd']['long'], self.cfg['macd']['m']]
        except KeyError:
            return None

