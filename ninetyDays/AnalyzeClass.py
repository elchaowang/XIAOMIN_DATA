import pandas as pd

class Cust:

    def __init__(self, customerid):
        self.customerid = customerid
        self.firstTimeSku = list()
        self.secondTimeSku = list()

    def add_sku_to_first(self, sku):
        self.firstTimeSku.append(sku)

    def add_sku_to_second(self, sku):
        self.secondTimeSku.append(sku)

    def get_overlap(self):
        overlapSku = list()
        for item in self.firstTimeSku:
            if item in self.secondTimeSku:
                overlapSku.append(item)
        return overlapSku


