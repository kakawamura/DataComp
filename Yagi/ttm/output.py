# -*- coding:utf-8 -*-

def get_path():
    import datetime
    import os
    now = datetime.datetime.today()
    path = "./log_" + "-".join([str(now.year), str(now.month).zfill(2), str(now.day).zfill(2), str(now.hour).zfill(2)]) + "/"
    os.mkdir(path)
    return path



def show_cpt(logfile, cpt):
   d, tmp = cpt//86400, cpt%86400
   h, tmp = tmp//3600, tmp%3600
   m, s = tmp//60, tmp%60
   print("computation time : {0}day, {1}hour, {2}minute, {3}second".format(round(d), round(h), round(m), round(s)))
   logfile.write("\ncomputation time : {0}day, {1}hour, {2}minute, {3}second\n".format(round(d), round(h), round(m), round(s)))


def show_parameters(logfile, ttm):
    phi = ttm.worddist()
    logfile.write("\n------------------- parameters------------------\n")
    logfile.write("\nalphaf\n")
    logfile.write(" ".join(list(map(str, ttm.alpha_z))))
    logfile.write("\n------------------------------------------------\n")


def output_word_topic_dist(ttm, voca, p, log_path):
    import numpy as np
    log_worddist = open(log_path+"itemdist_%d.txt" %p, "w")

    theta = ttm.theta_z_t
    for k in range(ttm.K):
        print ("\n-- topic: %d " %k)
        log_worddist.write("\n-- topic: %d\n" %k)
        for w in np.argsort(-theta[k])[:20]:
            print ("%s: %f " % (voca[w], theta[k,w]))
            log_worddist.write("%s: %f \n" % (voca[w], theta[k,w])) 
    log_worddist.flush()
    log_worddist.close()


def save_fig(ttm, K, path):
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn
    phi = ttm.worddist()

    plt.figure(figsize=(180, 100))
    plt.subplots_adjust(hspace=0.8, bottom=0.2)
    for k in range(K):
        plt.subplot(int(K)+1, 2, k+1)
        plt.title('topic%d' %k)
        plt.bar(np.arange(ttm.V), phi[k], align="center")
        plt.xlabel('item')
        plt.xticks(np.arange(ttm.V))
    plt.savefig(path + 'itemdist.png')

