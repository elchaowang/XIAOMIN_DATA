import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

def write_excels(a, filename):
    data_pd = pd.DataFrame(a)
    file = pd.ExcelWriter(filename)
    data_pd.to_excel(file, 'sheet1', float_format='%.5f', index=False, header=None)
    file.save()

def write_dict2excel(dict, output_filename):
    keyList = list()
    valueList = list()
    for key in dict.keys():
        keyList.append(key)
        valueList.append(dict[key])
    matrix = [keyList, valueList]
    matrix = np.transpose(matrix)
    del keyList
    del valueList
    write_excels(matrix, output_filename)


class Cust:

    def __init__(self, customerid):
        self.customerid = customerid
        self.firstTimeSku = list()
        self.secondTimeSku = list()
        self.flag = 0

    def add_sku_to_first(self, sku):
        self.firstTimeSku.append(sku)

    def add_sku_to_second(self, sku):
        self.secondTimeSku.append(sku)

    def get_overlap(self):
        overlapSku = list()
        for item in self.firstTimeSku:
            if item in self.secondTimeSku:
                overlapSku.append(item)
        overlap = sorted(set(overlapSku), key=overlapSku.index)
        self.overlap = overlap
        return overlap

    def get_repurch_flag(self):
        self.flag = 0
        for item in self.firstTimeSku:
            if item in self.secondTimeSku:
                self.flag = 1
        return self.flag

    def get_combination(self):
        self.combination = list()
        firstTimeSku = sorted(set(self.firstTimeSku), key=self.firstTimeSku.index)
        secondTimeSku = sorted(set(self.secondTimeSku), key=self.secondTimeSku.index)
        if self.flag == 0:
            for sku1 in firstTimeSku:
                for sku2 in secondTimeSku:
                    s = str(sku1)+'_'+str(sku2)
                    self.combination.append(s)
        return self.combination

# 'secondTimeOrds.xlsx'
# 'firstTimeOrds.xlsx'
def init_Custs(filename2, filename1):
    global outputMessage
    firstTimeData = pd.read_excel(filename2)
    customerid = list(firstTimeData['customerid'])
    custsid = sorted(set(customerid), key=customerid.index)
    # print('the total number customers who comes back and buy:')
    outputMessage += 'the total number customers who comes back and purchase the same product again: '
    # print(len(custsid), '\n')
    outputMessage += str(len(custsid))
    custsDict = {}
    for id in custsid:
        custsDict[str(id)] = Cust(id)
    for i in range(len(firstTimeData)):
        custsDict[str(firstTimeData['customerid'][i])].add_sku_to_second(firstTimeData['sku'][i])
    ### import the first time orders records to the customer objects
    secondTimeData = pd.read_excel(filename1)
    for i in range(len(secondTimeData)):
        custsDict[str(secondTimeData['customerid'][i])].add_sku_to_first(secondTimeData['sku'][i])
    ### create a dictionary which stores how many time each sku has been rebrought
    skuDict = {}
    for sku in firstTimeData['sku']:
        skuDict[sku] = 0

    return skuDict, custsDict


def calculate_repurch_numbers(filename2, filename1):
    global outputMessage
    skuDict, custsDict = init_Custs(filename2, filename1)
    ### overlapNums: each customer's repurch flag ( 1 or 0 )
    overlapNums = list()
    # nonrepurchCombination = list()
    for cust in custsDict:
        overlapNums.append(custsDict[cust].get_repurch_flag())
        # nonrepurchCombination.append(custsDict[cust].get_combination())

    overlapNums = np.array(overlapNums)
    outputMessage += '\n\nthe total number of customers who has purchased the same sku as the first time: '
    outputMessage += str(overlapNums.sum())
    # print('the total number of customers who has bought the same sku as the first time:')
    # print(overlapNums.sum(), '\n')
    nonOverlapNumb = len(custsDict) - overlapNums.sum()
    del overlapNums
    outputMessage += '\n\nthe total number of customers who has not purchased the same sku as the first time: '
    outputMessage += str(nonOverlapNumb)
    # print('the total number of customers who has not bought the same sku as the first time:')
    # print(nonOverlapNumb, '\n')
    del nonOverlapNumb

    ### calculate the time for each sku
    for cust in custsDict:
        custOverlap = custsDict[cust].get_overlap()
        for overlaps in custOverlap:
            skuDict[overlaps] += 1
    # for i, key in enumerate(skuDict):
    #     plt.bar(i, skuDict[key], color='r', width=0.1)
    # plt.xticks(np.arange(len(skuDict))+0.1, skuDict.keys())
    # plt.yticks(skuDict.values())
    # plt.grid(True)
    # print('the following figure has shows how many time each sku has been bought by people in their second buy:')
    # print(skuDict, '\n')
    write_dict2excel(skuDict, 'sku_repurch_distribution.xlsx')

    dictCombination = {}
    for cust in custsDict:
        for key in custsDict[cust].get_combination():
             try:
                 dictCombination[key] += 1
             except KeyError:
                 dictCombination[key] = 1
    write_dict2excel(dictCombination, 'combination.xlsx')
    # plt.show()

# def calculation():
#     try:
#         print('please input the filename of the second time orders in 90 days:')
#         filename2 = input()
#         print('please input the filename of the first time orders:')
#         filename1 = input()
#     except:
#         print('Unknown Error happened')
#     calculate_repurch_numbers(filename2, filename1)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(330, 250)
        MainWindow.setMinimumSize(QtCore.QSize(330, 250))
        MainWindow.setMaximumSize(QtCore.QSize(330, 251))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(330, 190))
        self.centralwidget.setMaximumSize(QtCore.QSize(330, 250))
        self.centralwidget.setObjectName("centralwidget")
        self.inputFilename2 = QtWidgets.QTextEdit(self.centralwidget)
        self.inputFilename2.setGeometry(QtCore.QRect(10, 10, 310, 25))
        self.inputFilename2.setObjectName("textEdit")
        self.inputFilename1 = QtWidgets.QTextEdit(self.centralwidget)
        self.inputFilename1.setGeometry(QtCore.QRect(10, 40, 310, 25))
        self.inputFilename1.setObjectName("inputFilename1")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(100, 200, 111, 31))
        self.pushButton.setObjectName("pushButton")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 70, 311, 121))
        self.textBrowser.setObjectName("textBrowser")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(self.calculation)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Distributions"))
        self.inputFilename2.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:italic;\">input the second time purchase filename here</span></p></body></html>"))
        self.inputFilename1.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:italic;\">input the first time purchase filename here</span></p></body></html>"))
        self.pushButton.setText(_translate("MainWindow", "Start"))

    def calculation(self):
        global outputMessage
        filename2 = self.inputFilename2.toPlainText()
        filename1 = self.inputFilename1.toPlainText()
        calculate_repurch_numbers(filename2, filename1)
        self.textBrowser.setText(outputMessage)
        outputMessage = ''

if __name__ == '__main__':
    outputMessage = ''
    app = QtWidgets.QApplication(sys.argv)
    wind = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(wind)
    wind.show()
    sys.exit(app.exec_())
    # print('please input the filename of the second time orders in 90 days:')
    # filename2 = input()
    # print('please input the filename of the first time orders:')
    # filename1 = input()
    # main(filename2, filename1)






# for cust in custsDict:
#     print(custsDict[cust].secondTimeSku)


# sku = list(data['sku'])
# skuList = sorted(set(sku), key=sku.index) # get the sku list for the distribution calculation
#
# filename = 'cust_test.xlsx'
# rankData = pd.read_excel(filename)
# custs = rankData['customerid']
# createtime = rankData['createtime']
# rank = rankData['rank']
# duration = rankData['duration']
# returnCusts = list()
# reCustsTime = list()
# for r in range(len(rank)):
#     if rank[r] == 2:
#         if duration[r] <= 90:
#             returnCusts.append(custs[r])
#             reCustsTime.append(createtime[r])
#
# for i in range(data.size):
#     print(i, 'finished')
#     for j in range(len(returnCusts)):
#         if data['customerid'][i] == returnCusts[j] and data['createtime'] == reCustsTime[j]:
#             print(data['sku'][i])





