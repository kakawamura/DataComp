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
    log = pd.read_csv("/Users/TakayukiYagi/Developer/M1/competition/data/log_comp_analyzed.csv")
    df = log[['order_date', 'new_customer_id', 'item_id']]
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
    N_user = len(set(table['new_customer_id']))
    N_item = len(set(table['item_id']))
    log_file = open(path + '/log.txt', 'w')
    log_file.write("user number : "+str(N_user) + "\n")
    log_file.write("category number : "+str(N_item) + "\n")
    log_file.flush()
    log_file.close()


def write_file(filepath, basket):
    output_file = open(filepath, 'w')
    for (key, value) in basket.items():
        output_file.write(str(key)+',')
        output_file.write(",".join(value) + "\n")
    output_file.flush()
    output_file.close()

def main():
    import os
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
        write_file(filepath, basket)

if __name__ == "__main__":
    main()    
