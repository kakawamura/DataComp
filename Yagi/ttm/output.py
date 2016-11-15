# -*- coding:utf-8 -*-

def get_path(options):
    import datetime
    import os
    now = datetime.datetime.today()
    path = "./log_" + "-".join([str(now.year), str(now.month).zfill(2), str(now.day).zfill(2), str(now.hour).zfill(2)]) + "_K"+str(options.K) + "_P" + str(options.P) + "_I" + str(options.I) +"/"
    os.mkdir(path)
    return path



def show_computation_time(logfile, cpt):
   d, tmp = cpt//86400, cpt%86400
   h, tmp = tmp//3600, tmp%3600
   m, s = tmp//60, tmp%60
   print("computation time : {0}day, {1}hour, {2}minute, {3}second".format(round(d), round(h), round(m), round(s)))
   logfile.write("\n------------- computation time  --------------\n")
   logfile.write("\n{0}day, {1}hour, {2}minute, {3}second\n".format(round(d), round(h), round(m), round(s)))


def show_options(logfile, options):
    logfile.write("\n------------------- options ------------------\n")
    logfile.write("\nnumber of customers : " + str(options.D) +"\n")
    logfile.write("number of items : " + str(options.V) +"\n")
    logfile.write("number of topics : " + str(options.K) +"\n")
    logfile.write("number of priods : " + str(options.P) +"\n")
    logfile.write("iteration count : " + str(options.I) +"\n")


def output_word_topic_dist(ttm, voca, p, log_path):
    import numpy as np
    theta = ttm.theta_z_t

    log_worddist_simplified = open(log_path+"itemdist_simplified/itemdist_"+str(p).zfill(2)+".txt", "w")
    for k in range(ttm.K):
        print ("\n-- topic: %d " %k)
        log_worddist_simplified.write("\n-- topic: %d\n" %k)
        n = min(10,len(voca.vocas))
        for w in np.argsort(-theta[k])[:n]:
            print ("%s: %f " % (voca[w], theta[k,w]))
            log_worddist_simplified.write("%s: %f \n" % (voca[w], theta[k,w])) 
    log_worddist_simplified.flush()
    log_worddist_simplified.close()

    log_worddist = open(log_path+"itemdist/itemdist_"+str(p).zfill(2)+".txt", "w")

    for k in range(ttm.K):
        log_worddist.write(",".join(theta[k].astype(str))+"\n") 
    log_worddist.flush()
    log_worddist.close()


def output_word_topic_columns(ttm, voca, log_path):
    log_worddist_columns = open(log_path+"itemdist/itemdist_columns.txt", "w")
    log_worddist_columns.write(voca[0])
    for t in range(1,ttm.V):
        log_worddist_columns.write(","+voca[t]) 
    log_worddist_columns.flush()
    log_worddist_columns.close()


def output_topic_user_dist(ttm, voca, p, log_path):
    import numpy as np
    phi = ttm.phi_m_z
    log_topicdist = open(log_path+"topicdist/topicdist_"+str(p).zfill(2)+".txt", "w")
    for d in range(ttm.D):
        log_topicdist.write(",".join(phi[d].astype(str))+"\n") 
    log_topicdist.flush()
    log_topicdist.close()


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

