#!/usr/bin/env python
# -*- coding: utf-8 -*-


# ------------- memo ------------------
# n : 単語数
# z : トピック
# m : ドキュメント
# t : ボキャブラリー
# -------------------------------------

import numpy as np

class LDA:
    def __init__(self, K, alpha, beta, docs, V):
        self.K = K 
        self.alpha = alpha 
        self.beta = beta   
        self.docs = docs
        self.V = V

        self.z_m_n = [] # topics of words of documents
        self.n_m_z = np.zeros((len(self.docs), K)) + alpha     # word count of each document and topic
        self.n_z_t = np.zeros((K, V)) + beta # word count of each topic and vocabulary
        self.n_z = np.zeros(K) + V * beta    # word count of each topic

        self.N = 0
        for m, doc in enumerate(docs):
            self.N += len(doc)
            z_n = []
            for t in doc:
                z = np.random.randint(0, K)
                z_n.append(z)
                self.n_m_z[m, z] += 1
                self.n_z_t[z, t] += 1
                self.n_z[z] += 1
            self.z_m_n.append(np.array(z_n))

    def inference(self):
        """learning once iteration"""
        for m, doc in enumerate(self.docs):
            z_n = self.z_m_n[m]
            n_m_z = self.n_m_z[m]
            for n, t in enumerate(doc):
                # discount for n-th word t with topic z
                z = z_n[n]
                n_m_z[z] -= 1
                self.n_z_t[z, t] -= 1
                self.n_z[z] -= 1

                # sampling topic new_z for t
                p_z = self.n_z_t[:, t] * n_m_z / self.n_z
                new_z = np.random.multinomial(1, p_z / p_z.sum()).argmax()

                # set z the new topic and increment counters
                z_n[n] = new_z
                n_m_z[new_z] += 1
                self.n_z_t[new_z, t] += 1
                self.n_z[new_z] += 1

    def worddist(self):
        """get topic-word distribution"""
        return self.n_z_t / self.n_z[:, np.newaxis]

    #def perplexity(self, docs=None):
    def perplexity(self):
        docs = self.docs
        phi = self.worddist()
        log_per = 0
        N = 0
        Kalpha = self.K * self.alpha
        for m, doc in enumerate(docs):
            theta = self.n_m_z[m] / (len(self.docs[m]) + Kalpha)
            for w in doc:
                log_per -= np.log(np.inner(phi[:,w], theta))
            N += len(doc)
        return np.exp(log_per / N)

def lda_learning(lda, iteration, voca, logfile):

    perp = lda.perplexity()
    print ("initial perplexity=%f" % perp)
    logfile.write("\n--------------- computation --------------------\n")
    logfile.write("\ninitial perplexity=%f\n" % perp)

    for i in range(iteration):
        lda.inference()
        perp = lda.perplexity()
        if (i + 1)%10 == 0:
            print ("iter%d perplexity=%f" % (i + 1, perp))
            logfile.write("iter%d perplexity=%f\n" % (i + 1, perp))


def main():
    import optparse
    import vocabulary
    import output
    import os
    import time
    parser = optparse.OptionParser()
    parser.add_option("-f", dest="filename", help="filename")
    parser.add_option("--alpha", dest="alpha", type="float", help="parameter alpha", default=0.5)
    parser.add_option("--beta", dest="beta", type="float", help="parameter beta", default=0.5)
    parser.add_option("-k", dest="K", type="int", help="number of topics", default=20)
    parser.add_option("-i", dest="iteration", type="int", help="iteration count", default=100)
    (options, args) = parser.parse_args()

    if not options.filename:
        parser.error("need filename(-f)")

    if options.filename:
        corpus = vocabulary.load_file(options.filename)


    voca = vocabulary.Vocabulary()
    docs = [voca.doc_to_ids(doc) for doc in corpus]

    lda = LDA(options.K, options.alpha, options.beta, docs, voca.size())

    path = output.get_path(options.K)
    logfile = open(path+"log.txt", "w")
    output.show_options(logfile, corpus, voca, options)
    start = time.time()

    lda_learning(lda, options.iteration, voca, logfile)

    cpt = time.time() - start
    output.show_cpt(logfile, cpt)
    output.show_parameters(logfile, lda)
    logfile.flush()
    logfile.close()

    output.output_word_topic_dist(lda, voca, path)
    output.save_fig(lda, options.K, path)

if __name__ == "__main__":
    main()
