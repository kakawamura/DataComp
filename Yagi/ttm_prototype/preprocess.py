# -*- coding:utf-8 -*-
import optparse
import numpy as np
import scipy.special as sp
import pandas as pd

def time2month(t):
    import datetime
    tdatetime = datetime.datetime.strptime(t, '%Y-%m-%d %H:%M')
    return int(tdatetime.month)

def get_table():
    order = pd.read_csv("/Users/TakayukiYagi/Developer/M1/competition/data/order.csv")
    detail = pd.read_csv("/Users/TakayukiYagi/Developer/M1/competition/data/order_detail.csv")
    item = pd.read_csv("/Users/TakayukiYagi/Developer/M1/competition/data/item.csv")
    
    df = pd.merge(pd.merge(order, detail, on='order_id', how='left'), item, on=['item_id', 'item_detail_id'], how='left')[['order_date', 'customer_id', 'item_category_2']].dropna()
    
    unique_customer_id = set(df.customer_id)
    dict_customer_id = dict(zip(list(unique_customer_id), [i for i in range(len(unique_customer_id))]))
    df.customer_id= df.customer_id.apply(lambda x: dict_customer_id[x])

    df["order_month"] = df.order_date.apply(time2month)
    return df

def make_basket(table):
    X = table.as_matrix()
    basket = {}
    
    for i in range(len(X)):
        if X[i,1] not in basket:
            basket[X[i,1]] = [str(X[i,2])]
        else:
            basket[X[i,1]].append(str(X[i,2]))
    return basket

def write_log(table, path):
    N_user = len(set(table['customer_id']))
    N_category = len(set(table['item_category_2']))
    log_file = open(path + '/log.txt', 'w')
    log_file.write("user number : "+str(N_user) + "\n")
    log_file.write("category number : "+str(N_category) + "\n")
    log_file.flush()
    log_file.close()


# 購入点数でフィルタリング（min <= 購入点数 <= max のみ採用)
def write_file(filepath, basket, MIN, MAX):
    output_file = open(filepath, 'w')
    for (key, value) in basket.items():
        n = len(value)
        if MAX >=n >= MIN:
            output_file.write(str(key)+' ')
            output_file.write(" ".join(value) + "\n")
    output_file.flush()
    output_file.close()

def main():
    import os
    parser = optparse.OptionParser()
    parser.add_option("--min", dest="MIN", type="int", help="analysis customer who buy at least min items", default=1)
    parser.add_option("--max", dest="MAX", type="int", help="analysis customer who buy at most items", default=9999999)
    (options, args) = parser.parse_args()


    table = get_table()
    path = "./baskets"
    os.mkdir(path)
    os.mkdir(path+"/baskets_per_month")
    write_log(table, path)
    # make basket per month
    for i in range(1,13):
        table_per_month = table[table["order_month"]==i]
        basket = make_basket(table_per_month)
        filepath = path + "/baskets_per_month/basket_" + str(i).zfill(2) + ".txt"
        write_file(filepath, basket, options.MIN, options.MAX)

if __name__ == "__main__":
    main()    
