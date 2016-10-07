# -*- coding:utf-8 -*-
import numpy as np
import scipy.special as sp
import pandas as pd
import matplotlib.pyplot as plt
import seaborn


# INTPUT
# D(購入者数), K(潜在クラス数), V(商品数), N=(n_1,n_2,..., n_D)(購入者ごとの購入商品数)
# w_dn 
# ITE_NUM

# sample input
D = 10
K = 3
V = 5
N = [7, 4, 6, 4, 2, 9, 3, 7, 4, 5]
w_dn = np.array([
    [1, 1, 1, 1, 3, 3, 4, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 2, 2, 2, 2, 0, 0, 0, 0],
    [2, 2, 2, 2, 0, 0, 0, 0, 0, 0],
    [3, 3, 0, 0, 0, 0, 0, 0, 0, 0],
    [3, 3, 3, 1, 1, 1, 3, 3, 3, 0],
    [0, 0, 4, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 4, 4, 0, 0, 0],
    [0, 0, 4, 4, 0, 0, 0, 0, 0, 0],
    [0, 1, 2, 3, 4, 0, 0, 0, 0, 0]
    ])
ITE_NUM = 5
alpha_k = np.ones(K)
beta_v = np.ones(V)

theta_dk = np.zeros((D, K))
phi_kv = np.zeros((K, V))

# カウントを初期化 (N_dk = N_kv = N_k = 0)
N_dk = np.zeros((D, K)).astype(np.integer) # 顧客dで潜在クラスkが割り当てられた商品数
N_kv = np.zeros((K, V)).astype(np.integer) # 潜在クラスkに割り当てられた語彙vの単語数
N_k = np.zeros(K).astype(np.integer) # 潜在クラスkに割り当てられた商品数

# トピックを初期化 (z_dn = 0)
z_dn = np.ones(w_dn.shape).astype(np.integer)*(-1)

# p(z_dn=k)を初期化
p_k = np.zeros(K) 

# 関数を定義

def get_zdn(d, n):
    # p(z_dn=k)を初期化
    p_k = np.zeros(K) 
    # サンプリング確率を計算
    for k in range(K):
        p_k[k] =  (N_dk[d][k] + alpha_k[k])*(N_kv[k][w_dn[d][n]] + beta_v[w_dn[d][n]])/(N_k[k] + sum(beta_v))
    p_k /= sum(p_k)
    print(p_k)
    # 潜在クラスをサンプリング
    topic = int(np.argmax(np.random.multinomial(1, p_k)))
    return topic

# ディガンマ関数
def dig(x):
    return sp.psi(x)

# alphaの更新
def new_alpha():
    new_alpha_k = np.zeros(K)
    mother = 0 
    for k in range(K):
        child = 0 # 分子を初期化
        for d in range(D):
            if k==0:
                mother += dig(N[d] + sum(alpha_k))
            child += dig(N_dk[d][k] + alpha_k[k])
        if k==0:
            mother -= D*dig(sum(alpha_k))
        child -= D*dig(alpha_k[k])
        new_alpha_k[k] = alpha_k[k]*child/mother
    return new_alpha_k

# betaの更新

def new_beta():
    new_beta_v = np.zeros(V)
    mother = 0
    for v in range(V):
        child = 0
        for k in range(K):
            if v==0:
                mother += dig(N_k[k] + sum(beta_v))
            child += dig(N_kv[k][v] + beta_v[v])
        if v==0:
            mother -= K*dig(sum(beta_v))
        child -= K*dig(beta_v[v])
    new_beta_v[v] = beta_v[v]*child/mother
    return new_beta_v


# main
for i in range(ITE_NUM):
    for d in range(D):
        for n in range(N[d]):
            if z_dn[d][n] > -1:
                # カウントからz_dnの割当分を引く
                N_dk[d][z_dn[d][n]] -= 1
                N_kv[z_dn[d][n]][w_dn[d][n]] -= 1
                N_k[z_dn[d][n]] -= 1
            
            # z_dnをサンプリング
            z = get_zdn(d, n)
            z_dn[d][n] = z

            # カウントに新たに割り当てられたトピック分を加える
            N_dk[d][z] += 1 
            N_kv[z][w_dn[d][n]] += 1
            N_k[z] += 1

    # ハイパーパラメータを更新
    alpha_k = new_alpha()
    beta_v = new_beta()

for d in range(D):
    for k in range(K):
        theta_dk[d][k] = (N_dk[d][k] + alpha_k[k])/(N[d] + alpha_k[k]*K)

for k in range(K):
    for v in range(V):
        phi_kv[k][v] = (N_kv[k][v] + beta_v[v])/(N_k[k] + beta_v[v]*V)


print('z_dn')
print(z_dn)
print('N_dk')
print(N_dk)
print('N_kv')
print(N_kv)
print("N_k")
print(N_k)
print('alpha_k')
print(alpha_k)
print('beta_k')
print(beta_v)
print('theta_dk')
print(theta_dk)
print('phi_kv')
print(phi_kv)

plt.figure(figsize=(10, 10))
plt.subplots_adjust(hspace=0.8, bottom=0.2)
for d in range(D):
    plt.subplot(int(D/2), 2, d+1)
    plt.title('customer%d' %d)
    plt.bar(np.arange(K), theta_dk[d], align="center")
    plt.xlabel('topic')
    plt.xticks([0, 1, 2])
plt.show()

plt.figure(figsize=(10, 10))
plt.subplots_adjust(hspace=0.8, bottom=0.2)
for k in range(K):
    plt.subplot(int(K/2)+1, 2, k+1)
    plt.title('topic%d' %k)
    plt.bar(np.arange(V), phi_kv[k], align="center")
    plt.xlabel('item')
    plt.xticks([0, 1, 2, 3, 4])
plt.show()

