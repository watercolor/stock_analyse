
import urllib
import os
import yaml

stockcode_file = "/Users/nzm/code/stock_analyse/stockcode.yaml"
stockcfg = None
with open(stockcode_file) as fd:
    stockcfg = yaml.load(fd)

print stockcfg[601318]



