# -*- coding:utf-8 -*-
import optparse
import numpy as np
import scipy.special as sp
import pandas as pd

def get_table():
    order = pd.read_csv("/Users/TakayukiYagi/Developer/M1/competition/data/order.csv")
    detail = pd.read_csv("/Users/TakayukiYagi/Developer/M1/competition/data/order_detail.csv")
    item = pd.read_csv("/Users/TakayukiYagi/Developer/M1/competition/data/item.csv")
    
    df = pd.merge(pd.merge(order, detail, on='order_id', how='left'), item, on=['item_id', 'item_detail_id'], how='left')[['customer_id', 'item_category_2']].dropna()
    
    unique_customer_id = set(df.customer_id)
    dict_customer_id = dict(zip(list(unique_customer_id), [i for i in range(len(unique_customer_id))]))
    df.customer_id= df.customer_id.apply(lambda x: dict_customer_id[x])
    return df

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


# 購入点数でフィルタリング（min <= 購入点数 <= max のみ採用)
def write_file(filename, basket, MIN, MAX):
    output_file = open(filename, 'w')
    for i in range(len(basket)):
        n = len(basket[i])
        if max >=n >= min:
            output_file.write(" ".join(basket[i]) + "\n")
    output_file.flush()
    output_file.close()

def main():
    parser = optparse.OptionParser()
    parser.add_option("-f", dest="filename", help="filename")
    parser.add_option("--min", dest="MIN", type="int", help="analysis customer who buy at least min items", default=1)
    parser.add_option("--max", dest="MAX", type="int", help="analysis customer who buy at most items", default=9999999)
    (options, args) = parser.parse_args()

    if not options.filename:
        parser.error("need filename(-f)")

    table = get_table()
    basket = make_basket(table)
    write_file(options.filename,basket, options.MIN, options.MAX)

if __name__ == "__main__":
    main()    
