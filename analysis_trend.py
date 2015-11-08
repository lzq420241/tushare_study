#!/usr/bin/python
import pandas as pd
import tushare as ts
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def deal_amount(arr):
    return sum(filter(lambda x: x>0, arr))

for c in ['002489']:#, '600252', '601288','601988','601006','600018']:
    df = pd.read_csv('trend_%s.csv' % c)
    df.drop(['ma_v','ma_r','ex_r','big_r','mid_r','sm_r'], axis=1, inplace=True)

    s1 = df.apply(lambda x: deal_amount([x['ex_v'], x['big_v'], x['mid_v'],x['sm_v']]), axis=1)
    df.insert(3, 'deal_amt', s1)
    # df = df[0:3]
    # df = df[df.ma_v<0]
    print df
    print df.groupby(['raise_rate'],sort=True).groups
    # print df.iat[4,3] > 0, df.iat[4,4] > 0
    # print len(df.index)
    # print df[index=0]
    # df = df[df.ma_v<0]
    # # df[df='-']=0
    # # print df
    # # df = df[df.raise_rate < 0]
    # print df.date
    # print 
    # print type(df.date)
    # print c, df.date, df.raise_rate
    # # print 
    # if len(df.index) >5 and df.date[4] >= '2015-10-30':
    #     print c


