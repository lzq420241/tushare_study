#!/usr/bin/python
import pandas as pd
import tushare as ts
from urllib2 import urlopen
from lxml import etree
import pandas as pd
import os
import time
from datetime import datetime, date
from multiprocessing import Pool

COL_NUM=13
BASE_URL='http://data.eastmoney.com/zjlx/'
list_to_tuple_list = lambda l, n: map(lambda x:tuple(l[slice(x*COL_NUM,(x+1)*COL_NUM)]), range(n))
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def save_profit(c):
    f_n = './data/trend_%s.csv' % c
    if os.path.exists(f_n) and time.localtime(os.path.getmtime(f_n)).tm_mday == date.timetuple(datetime.today()).tm_mday:
        print 'File exists'
        return
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
    df.drop(['ma_r','ex_r','big_r','mid_r','sm_r'], axis=1, inplace=True)
    df.to_csv(f_n, encoding='utf-8')


def select_the_major_sell_end(c):
    df4 = ts.get_hist_data(c,start='2015-11-06',end='2015-11-06')
    # if not df4.empty and 0<(df4.ma10.tolist()[0] - df4.ma5.tolist()[0])/df4.ma10.tolist()[0] < 0.05 and 0<(df4.ma20.tolist()[0] - df4.ma5.tolist()[0])/df4.ma20.tolist()[0] < 0.05 and df4.high.tolist()[0] < 13:
    if not df4.empty and df4.close.tolist()[0] < 13:
        save_profit(c)
        df = pd.read_csv('./data/trend_%s.csv' % c)
        # df = df[0:5]
        # df = df[df.ma_v<0]
        # if len(df.index) >= 3:
        # df.iat[0,3] is raise_rate, df.iat[0,4] is ma_v
        # print df[0:3]
        # print df.iat[0,3] , df.iat[0,4],df.iat[1,3] , df.iat[1,4]
        print c
        print df
        print
        # if df.iat[0,3] > 0 and df.iat[0,4] < 0 and df.iat[1,3] < 0 and df.iat[1,4] < 0 and df.iat[2,3] < 0 and df.iat[2,4] < 0:
        #     print c
        #     print df[0:5]
        #     print 


df = pd.read_csv('profit_201503.csv',encoding='utf-8')
#df2 = df[df.gross_profit_rate > 40]
df2 = df[df.net_profit_ratio > 10]
df2 = df2.iloc[:,1:]

df3 = df2.sort_values(by='net_profit_ratio',ascending=False)


codes_with_high_profit = map(lambda x:str(x).zfill(6), df3.code.tolist())
p = Pool(5)
p.map(select_the_major_sell_end, codes_with_high_profit)


