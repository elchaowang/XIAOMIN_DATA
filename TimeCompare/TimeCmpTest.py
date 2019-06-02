import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 这个data是所有苏秘正式会员的关注时间A
#                     绑定微信时间B
#                     和首次购买时间C明细.
# 需要分析: 1. A>C的顾客和A<C的顾客比例分布;
#          2. B>C的顾可和B<C的顾客比例分布;
#          3. A-B的间隔天数分布, B-C的间隔天数分布, A-C的间隔天数分布
# （以上分析均需排除A/B/C均为一天的顾客）


# define A>C: 1, A<C: 2
# define B>C: 3, B<C: 4

zeroTime = pd.Timedelta('0 days 0:0:00')
th_days = 90
daily_seconds = 86400
class cust:
    def __init__(self, customerid, follow_time, sign_up_time, first_purchase_time):
        self.customerid = customerid
        self.follow_time = follow_time
        self.sign_up_time = sign_up_time
        self.first_purchase_time = first_purchase_time
        self.customer_categrayAC = None
        self.customer_categrayBC = None
        self.follow_first_purch()
        self.sign_up_first_purch()

    def follow_first_purch(self):
        if (self.follow_time - self.first_purchase_time) > zeroTime:
            self.customer_categrayAC = True
        else:
            self.customer_categrayAC = False

    def sign_up_first_purch(self):
        if (self.sign_up_time - self.first_purchase_time) > zeroTime:
            self.customer_categrayBC = True
        else:
            self.customer_categrayBC = False

    def delat_AB_follow_sign_up(self):
        delta = self.follow_time - self.sign_up_time
        delta_days = (delta.days * daily_seconds + delta.seconds) / daily_seconds
        return delta_days

    def delta_BC_sign_up_first_purchase(self):
        delta = self.sign_up_time - self.first_purchase_time
        delta_days = (delta.days * daily_seconds + delta.seconds) / daily_seconds
        return delta_days

    def delta_AC_follow_first_purchase(self):
        delta = self.follow_time - self.first_purchase_time
        delta_days = (delta.days * daily_seconds + delta.seconds) / daily_seconds
        return delta_days


class cust_group:

    def __init__(self, customerid, follow_time, sign_up_time, first_purchase_time):
        self.customers = list()
        if len(customerid) == len(follow_time) == len(sign_up_time) == len(first_purchase_time):
            for i in range(len(customerid)):
                person = cust(customerid[i], follow_time[i], sign_up_time[i], first_purchase_time[i])
                self.customers.append(person)

    def get_AC_distribution(self):
        num_true, num_false = 0, 0
        for person in self.customers:
            if person.customer_categrayAC is True:
                num_true += 1
            elif person.customer_categrayAC is False:
                num_false += 1
        return num_true, num_false

    def get_BC_distribution(self):
        num_true, num_false = 0, 0
        for person in self.customers:
            if person.customer_categrayBC is True:
                num_true += 1
            elif person.customer_categrayBC is False:
                num_false += 1
        return num_true, num_false

    def get_AB_delat_days(self):
        days = list()
        for person in self.customers:
            nday = person.delat_AB_follow_sign_up()
            if abs(nday) < th_days:
                days.append(nday)
        days = np.array(days)
        return days

    def get_BC_delta_days(self):
        days = list()
        for person in self.customers:
            nday = person.delta_BC_sign_up_first_purchase()
            if abs(nday) < th_days:
                days.append(nday)
        days = np.array(days)
        return days

    def get_AC_delta_days(self):
        days = list()
        for person in self.customers:
            nday = person.delta_AC_follow_first_purchase()
            if abs(nday) < th_days:
                days.append(nday)
        days = np.array(days)
        return days


def write_excels(data_pd, filename):
    file = pd.ExcelWriter(filename)
    data_pd.to_excel(file, 'sheet1', float_format='%.5f', index=True, header=None)
    file.save()

filename = 'sumi.xlsx'
data = pd.read_excel(filename)
customerid = data['会员卡号']
first_purch_time = data['首次购买时间']
sign_up_time = data['注册/绑定时间']
follow_time = data['关注时间']

customers = cust_group(customerid, follow_time, sign_up_time, first_purch_time)

AC_NUM, CA_NUM = customers.get_AC_distribution()
BC_NUM, CB_NUM = customers.get_BC_distribution()

print('先关注再购买的顾客数:', AC_NUM)
print('先购买在关注的顾客数:', CA_NUM)

print('先注册再购买的顾客数:', BC_NUM)
print('先购买再注册的顾客数:', CB_NUM)

days_AB = customers.get_AB_delat_days()
days_BC = customers.get_BC_delta_days()
days_AC = customers.get_AC_delta_days()

days_AB = pd.DataFrame(days_AB)
days_BC = pd.DataFrame(days_BC)
days_AC = pd.DataFrame(days_AC)

ab = days_AB.dropna().astype(int)
bc = days_BC.dropna().astype(int)
ac = days_AC.dropna().astype(int)

result_ab = ab.apply(pd.value_counts)
result_bc = bc.apply(pd.value_counts)
result_ac = ac.apply(pd.value_counts)

print(result_ab)
print(type(result_ab))

write_excels(result_ab, 'A-B.xlsx')
write_excels(result_bc, 'B-C.xlsx')
write_excels(result_ac, 'A-C.xlsx')
# print(len(ab))
# print(len(bc))
# print(len(ac))
# bc = sns.distplot(days_BC, rug=True, hist=False)
sns.distplot(ab, rug=True, hist=True)
plt.show()
sns.distplot(bc, rug=True, hist=False)
plt.show()
sns.distplot(ac, rug=True, hist=False)
plt.show()

# for index in range(len(days_AB)):
#     if days_AB[index] is np.Inf or days_AB[index] is np.nan:
#         print(index)
# print('AB')
# #
# for index in range(len(days_BC)):
#     if days_BC[index] is np.Inf or days_AB[index] is np.nan:
#         print(index)
# print('BC')
#
# for index in range(len(days_AC)):
#     if days_AC[index] is np.Inf or days_AB[index] is np.nan:
#         print(index)
# print('AC')
#
# print(days_AB.shape)
# print(days_BC.shape)
# print(days_AC.shape)


































