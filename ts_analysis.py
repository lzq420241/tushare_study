#!/usr/bin/python
import pandas as pd
import tushare as ts
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
df = pd.read_csv('profit_201503.csv',encoding='utf-8')
#df2 = df[df.gross_profit_rate > 40]
df2 = df[df.net_profit_ratio > 20]
df2 = df2.iloc[:,1:]

df3 = df2.sort_values(by='net_profit_ratio',ascending=False)


codes_with_high_profit = map(lambda x:str(x).zfill(6), df3.code.tolist())
for c in codes_with_high_profit:
    df4 = ts.get_hist_data(c,start='2015-11-03',end='2015-11-03')
    if not df4.empty and df4.ma20.tolist()[0] > df4.high.tolist()[0] < 10:
        print c
        print df4
