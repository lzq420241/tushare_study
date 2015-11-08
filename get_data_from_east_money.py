#!/usr/bin/python
from urllib2 import urlopen
from lxml import etree
import pandas as pd
import os
import time
from datetime import datetime, date
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

COL_NUM=13
BASE_URL='http://data.eastmoney.com/zjlx/'
list_to_tuple_list = lambda l, n: map(lambda x:tuple(l[slice(x*COL_NUM,(x+1)*COL_NUM)]), range(n))

def save_profit(c):
    f_n = './data/trend_%s.csv' % c
    if os.path.exists(f_n) and time.localtime(os.path.getmtime(f_n)).tm_mday == date.timetuple(datetime.today()).tm_mday:
        print 'File exists'
        # return
    html = urlopen(BASE_URL+'%s.html' % c).read()
    page = etree.HTML(html)
    data = page.xpath(u'//div[@id="content_zjlxtable"]/table/tbody/tr/td/text()|//div[@id="content_zjlxtable"]/table/tbody/tr/td/span/text()')
    data = filter(lambda x: x.strip(),data)
    data = map(lambda x: x.strip().strip('%'),data)
    data = map(lambda x: x!='-' and x or '0',data)
    def try_normalize(x):
        try:
            return unicode('%.2f' % (float(x)/10000)) if abs(float(x)) > 100 else x
        except:
            return x
    data = map(lambda x: try_normalize(x), data)
    data = map(lambda x: x.endswith(u'\u4ebf') and unicode(float(x.strip(u'\u4ebf'))*10000) or x,data)
    data = map(lambda x: x.endswith(u'\u4e07') and x.strip(u'\u4e07') or x, data)
    data = list_to_tuple_list(data,len(data)/COL_NUM)
    df = pd.DataFrame(data, columns = ['date','close_price','raise_rate','ma_v','ma_r','ex_v','ex_r','big_v','big_r','mid_v','mid_r', 'sm_v','sm_r'])
    df.to_csv(f_n, encoding='utf-8')

for i in ['002489','600985','000979', '600252', '601288','601988','601006','600018']:
    save_profit(i)
    df = pd.read_csv('./data/trend_%s.csv' % i)
    print df


