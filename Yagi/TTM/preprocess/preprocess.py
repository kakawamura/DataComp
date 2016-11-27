# -*- coding:utf-8 -*-
import optparse
import numpy as np
import scipy.special as sp
import pandas as pd


def make_basket(table):
    X = table.as_matrix()
    item_per_cus = {}
    
    for i in range(len(X)):
        if X[i,0] not in item_per_cus:
            item_per_cus[X[i,0]] = [X[i,1]]
        else:
            item_per_cus[X[i,0]].append(X[i,1])
    basket = list(item_per_cus.values())
    return basket

def write_file(basket):
    output_file = open('basket.txt', 'w')
    for i in range(len(basket)):
        output_file.write(" ".join(map(str,basket[i])) + "\n")
    output_file.flush()
    output_file.close()

def main():
    log = pd.read_csv("/Users/TakayukiYagi/Developer/M1/competition/data/log_comp_analyzed.csv")[['customer_id', 'new_item_id']]
    basket = make_basket(log)
    write_file(basket)

if __name__ == "__main__":
    main()    
