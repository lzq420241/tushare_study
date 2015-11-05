#!/usr/bin/python
import tushare as ts

def save_profit(y, q):
    df = ts.get_profit_data(y,q)
    # df = ts.get_today_all()
    while df is None:
        df = ts.get_profit_data(y,q)
    print df
    df.to_csv('profit_%s0%s.csv' % (y,q),encoding='utf-8')

save_profit(2012,4)
