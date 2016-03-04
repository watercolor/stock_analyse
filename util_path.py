# encoding=utf-8
import time
import os
import glob
from parse_yaml import *

def find_similar_path(code):
    pattern = os.getcwd() + os.sep + "stockdata" + os.sep + code + "_*"
    result = glob.glob(pattern)
    if len(result):
        return result[0]
    else:
        return None