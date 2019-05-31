# -*- coding: utf-8 -*-
import pypyodbc
from pandas import DataFrame
import pandas as pd
import pickle

def read_data_to_file(database, storageFile, cmd):
    pypyodbc.lowercase = False
    conn = pypyodbc.connect(database)
    cur = conn.cursor()
    cur.execute(cmd)
    orders = list()
    while True:
        tmp = list()
        row = cur.fetchone()
        if row is None:
            break
        for item in row:
            tmp.append(item)
        orders.append(tmp)
    orderFrame = DataFrame(orders)
    orderFrame.rename(columns={0: 'part', 1: 'storeid', 2: 'storename', 3: 'customerid', 4: 'customername', 5: 'btd',
                               6: 'tier', 7: 'club', 8: 'salesorder', 9: 'createtime', 10: 'ordertype', 11: 'sku',
                               12: 'skuname', 13: 'itemtype', 14: 'marketprice', 15: 'revenue', 16: 'quantity', 17: 'fst',
                               18: 'fststore', 19: 'fstrevenue', 20: 'lst', 21: 'bcid', 22: 'bcname'}, inplace=True)
    file = storageFile
    f = open(file, 'wb')
    pickle.dump(orderFrame, f)
    f.close()
    cur.close()
    conn.close()