import pandas as pd
import numpy as np


zeroTime = pd.Timedelta('2 days 1:2:10')
x = zeroTime.seconds
print(x)
filename = 'test.xlsx'
data = pd.read_excel(filename)
customerid = data['会员卡号']
first_purch_time = data['首次购买时间']
sign_up_time = data['注册/绑定时间']
follow_time = data['关注时间']

delta = follow_time[10] - first_purch_time[10]
print(delta)
print(delta.seconds)

delta_days = int((delta.days*24*3600 + delta.seconds) / (24*3600))
print(delta_days)



if delta > zeroTime:
    print('yes')
else:
    print('no')










