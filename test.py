# -*- coding: utf-8 -*-
import pypyodbc
from pandas import DataFrame
import pickle
import matplotlib.pyplot as plt
from sales import *

storageFile = 'OrderObj.txt'
# database = r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};" + r"Dbq=D:\Python Projects\LG_DataAnalyzing\AnnualReport_Backup.accdb;"
# cmd = "SELECT * FROM AllSales where customerid<>'<null>' and createtime>='20180101' and createtime<'20190101' and 订单类型<>'退货' order by btd asc"
# read_data_to_file(database, storageFile, cmd)

fr = open(storageFile, 'rb')

orders = pickle.load(fr)

orders = orders.fillna('<null>')
orders = orders[orders['btd']!='<null>']

print(orders['btd'])

fr.close()