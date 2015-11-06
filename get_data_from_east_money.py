#!/usr/bin/python
from urllib2 import urlopen
from lxml import etree
import pandas as pd

BASE_URL='http://data.eastmoney.com/zjlx/'
list_to_tuple_list = lambda l, n: map(lambda x:tuple(l[slice(x*n,(x+1)*n)]), range(n))

def save_profit(c):
    html = urlopen(BASE_URL+'%s.html' % c).read()
    page = etree.HTML(html)
    data = page.xpath(u'//div[@id="content_zjlxtable"]/table/tbody/tr/td/text()|//div[@id="content_zjlxtable"]/table/tbody/tr/td/span/text()')
    data = filter(lambda x: x.strip(),data)
    data = map(lambda x: x.strip().strip(u'\u4e07'),data)
    data = list_to_tuple_list(data,13)
    df = pd.DataFrame(data, columns = ['date','close_price','raise_rate','ma_v','ma_r','ex_v','ex_r','big_v','big_r','mid_v','mid_r', 'sm_v','sm_r'])
    df.to_csv('trend_%s.csv' % c)
    print df

save_profit('000883')
