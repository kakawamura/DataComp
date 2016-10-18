#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

class TTM:
    def __init__(self, D, V ,K ,P ,I):
        self.alpha_m = np.ones(D) 
        self.beta_z = np.ones(K)  
        self.theta_z_t = np.ones((K, V))/V
        self.phi_m_z = np.ones((D, K))/K  

        self.docs = None
        self.docs_id = None
        self.docs_n = None
        self.V = V
        self.D = D
        self.K = K 
        self.P = P
        self.I = I

        self.z_m_n = [] 
        self.n_m_z = np.zeros((self.D, K))
        self.n_z_t = np.zeros((K, V))
        self.n_z = np.zeros(K) 

        self.N = None

    def initialize(self,docs_id, docs):
        self.N = 0
        for (m, doc) in zip(docs_id, docs):
            self.N += len(doc)
            z_n = []
            for t in doc:
                z = np.random.randint(0, self.K)
                z_n.append(z)
                self.n_m_z[m, z] += 1
                self.n_z_t[z, t] += 1
                self.n_z[z] += 1
            self.z_m_n.append(np.array(z_n))

    def get_new_z(self, n_m_z, m, t):
        a = (n_m_z + self.alpha_m[m]*self.phi_m_z[m])/(self.docs_n[m] - 1 + self.alpha_m[m]) 
        b = (self.n_z_t[:,t] + self.beta_z*self.theta_z_t[:,t])/(self.n_z_t[:,t] + self.beta_z)
        p_z = a*b
        new_z = np.random.multinomial(1, p_z / p_z.sum()).argmax()
        return new_z
 
    def gamma(self, x):
        import scipy.special as sp
        return sp.psi(x)
 
    def get_new_alpha(self, m):
        vf = np.vectorize(self.gamma)
        a = np.sum(self.phi_m_z.T*(vf(self.n_m_z.T + self.alpha_m*self.phi_m_z.T) - vf(self.alpha_m*self.phi_m_z.T)), axis=0)
        b = np.array(list(map(self.gamma, self.docs_n[m] + self.alpha_m))) - np.array(list(map(self.gamma, self.alpha_m)))
        new_alpha = self.alpha_m*a/b
        return new_alpha
 
    def get_new_beta(self, t):
        vf = np.vectorize(self.gamma)
        a = np.sum(self.theta_z_t.T*(vf(self.n_z_t.T + self.beta_z*self.theta_z_t.T) - vf(self.beta_z*self.theta_z_t.T)), axis=0)
        b = np.array(list(map(self.gamma, self.n_z_t[:,t] + self.beta_z))) - np.array(list(map(self.gamma, self.beta_z)))
        new_beta = self.beta_z*a/b
        return new_beta

    def get_new_phi(self):
        new_phi = ((self.n_m_z.T + self.alpha_m*self.phi_m_z.T)/( + self.alpha_m)).T
        return new_phi

    def get_new_theta(self):
        new_theta = ((self.n_z_t.T + self.beta_z*self.theta_z_t.T)/( + self.beta_z)).T
        return new_theta

    def inference(self):
        for (m, doc) in zip(self.docs_id, self.docs):
            z_n = self.z_m_n[m]
            n_m_z = self.n_m_z[m]
            for n, t in enumerate(doc):

                z = z_n[n]
                n_m_z[z] -= 1
                self.n_z_t[z, t] -= 1
                self.n_z[z] -= 1

                new_z = self.get_new_z(n_m_z, m, t)

                z_n[n] = new_z
                n_m_z[new_z] += 1
                self.n_z_t[new_z, t] += 1
                self.n_z[new_z] += 1

        self.theta_z_t = self.get_new_theta()
        self.phi_m_z = self.get_new_phi()
        self.alpha_m = self.get_new_alpha(m)
        self.beta_z = self.get_new_beta(t)


    def perplexity(self):
        return 1


    def ttm_learning(self, filenames, path):
        import vocabulary

        for p in range(self.P):
            (self.docs_id, self.docs) = vocabulary.load_file(path, filenames[p])
            voca = vocabulary.Vocabulary()
            self.docs = [voca.doc_to_ids(doc) for doc in self.docs]
            self.docs_n = np.zeros(self.D)
            for (i, doc) in zip(self.docs_id, self.docs):
                self.docs_n[i] = len(doc)
            self.initialize(self.docs_id, self.docs)
            logfile = open("./"+path+"/priod"+str(p), "w")
    
            perp = self.perplexity()
            print ("initial perplexity=%f" % perp)
            logfile.write("\n--------------- computation --------------------\n")
            logfile.write("\ninitial perplexity=%f\n" % perp)
        
            for i in range(self.I):
                self.inference()
                perp = self.perplexity()
                if 1:
                    print ("iter%d perplexity=%f" % (i + 1, perp))
                    logfile.write("iter%d perplexity=%f\n" % (i + 1, perp))

            logfile.flush()
            logfile.close()


def main():
    import optparse
    import vocabulary
    import output
    import os
    import time
    parser = optparse.OptionParser()
    parser.add_option("-f", dest="filedir", help="directory name which have files")
    parser.add_option("-d", dest="D", type="int", help="number of customers")
    parser.add_option("-v", dest="V", type="int", help="number of vocabularys")
    parser.add_option("-k", dest="K", type="int", help="number of topics", default=20)
    parser.add_option("-p", dest="P", type="int", help="number of priods")
    parser.add_option("-i", dest="I", type="int", help="iteration count", default=100)
    (options, args) = parser.parse_args()

    if not options.filedir:
        parser.error("need fildirname(-f)")

    if not options.D:
        parser.error("need number of customers(-d)")

    if not options.V:
        parser.error("need number of items(-v)")

    if not options.P:
        parser.error("need number of priods(-p)")

    if options.filedir:
        filenames = vocabulary.load_filenames(options.filedir)

    path = output.get_path()

    ttm = TTM(options.D, options.V, options.K, options.P, options.I)
    ttm.ttm_learning(filenames, options.filedir)


if __name__ == "__main__":
    main()
