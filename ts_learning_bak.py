import pandas as pd
import tushare as ts


# pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def remove_percent(s):
    if '.' in s and '%' in s:
        return float(s.strip('%'))
    return s

df = ts.top_list('2015-10-30')
df['pchange'] = df['pchange'].replace('%', '', regex=True).astype('float')
# print dir(df)
# print df.sort_values(by='pchange', ascending=False)[df.pchange>8.0]['code']

up_c_top_list = df[df.pchange>7.0]['code'].tolist()
up_n_top_list = df[df.pchange>7.0]['name'].tolist()

for c, n in zip(up_c_top_list, up_n_top_list):
    # print c
    df1 = ts.get_hist_data(c,start='2015-10-27',end='2015-10-30')
    try:
        if not df1.empty and df1['close'].tolist()[-1] < df1['ma20'].tolist()[-1]:
            print c, n
            print df1
    except:
        pass

# df2 = df[df.gross_profit_rate > 30]

# print df2.sort_values(by='gross_profit_rate')