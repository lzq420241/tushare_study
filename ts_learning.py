import tushare as ts


df = ts.get_profit_data(2015,3)

print df
df2 = df[df.gross_profit_rate > 30]

print df2.sort_values(by='gross_profit_rate')