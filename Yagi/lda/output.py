# -*- coding:utf-8 -*-

def get_path():
    import datetime
    import os
    # 現在時刻の取得
    now = datetime.datetime.today()
    path = "./log_" + "-".join([str(now.year), str(now.month).zfill(2), str(now.day).zfill(2), str(now.hour).zfill(2)]) + "/"
    # ディレクトリ生成
    os.mkdir(path)
    return path


def show_options(logfile, corpus, voca, options):
    logfile.write("\n------------------- options--------------------\n")
    logfile.write("\ncustomer=%d \nitems=%d \nK=%d \nalpha=%f \nbeta=%f \niteration=%d\nsave_fig=%s\n" % (len(corpus), len(voca.vocas), options.K, options.alpha, options.beta, options.iteration, options.save))
    print ("\ncustomer=%d, items=%d, K=%d, alpha=%f, beta=%f, iter=%d, save=%s\n" % (len(corpus), len(voca.vocas), options.K, options.alpha, options.beta, options.iteration, options.save))

def show_cpt(logfile, cpt):
   d, tmp = cpt//86400, cpt%86400
   h, tmp = tmp//3600, tmp%3600
   m, s = tmp//60, tmp%60
   print("computation time : {0}day, {1}hour, {2}minute, {3}second".format(round(d), round(h), round(m), round(s)))
   logfile.write("\ncomputation time : {0}day, {1}hour, {2}minute, {3}second\n".format(round(d), round(h), round(m), round(s)))


def show_parameters(logfile, lda):
    phi = lda.worddist()
    logfile.write("\n------------------- parameters------------------\n")
    logfile.write("\nalpha=%f \nbeta=%f\n" % (lda.alpha, lda.beta))
    logfile.write("\n------------------------------------------------\n")


def output_word_topic_dist(lda, voca, path):
    import numpy as np
    worddist = open(path+"itemdist.txt", "w")

    zcount = np.zeros(lda.K, dtype=int)
    wordcount = [dict() for k in range(lda.K)]
    for xlist, zlist in zip(lda.docs, lda.z_m_n):
        for x, z in zip(xlist, zlist):
            zcount[z] += 1
            if x in wordcount[z]:
                wordcount[z][x] += 1
            else:
                wordcount[z][x] = 1

    phi = lda.worddist()
    for k in range(lda.K):
        print ("\n-- topic: %d (%d words)" % (k, zcount[k]))
        worddist.write("\n-- topic: %d (%d words)\n" % (k, zcount[k]))
        for w in np.argsort(-phi[k])[:20]:
            print ("%s: %f (%d)" % (voca[w], phi[k,w], wordcount[k].get(w,0)))
            worddist.write("%s: %f (%d)\n" % (voca[w], phi[k,w], wordcount[k].get(w,0)))
    worddist.flush()
    worddist.close()


def save_fig(lda, K, path):
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn
    phi = lda.worddist()

    plt.figure(figsize=(180, 100))
    plt.subplots_adjust(hspace=0.8, bottom=0.2)
    for k in range(K):
        plt.subplot(int(K)+1, 2, k+1)
        plt.title('topic%d' %k)
        plt.bar(np.arange(lda.V), phi[k], align="center")
        plt.xlabel('item')
        plt.xticks(np.arange(lda.V))
    plt.savefig(path + 'itemdist.png')

