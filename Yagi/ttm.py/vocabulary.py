#!/usr/bin/env python
# -*- coding: utf-8 -*-


import nltk, re


def load_file(filename):
    corpus = []
    f = open(filename, 'r')
    for line in f:
        doc = re.findall(r'\w+',line)
        if len(doc)>0:
            corpus.append(doc)
    f.close()
    return corpus


class Vocabulary:
    def __init__(self):
        self.vocas = []        # id to word
        self.vocas_id = dict() # word to id
        self.docfreq = []      # id to document frequency

    def term_to_id(self, term):
        if term not in self.vocas_id:
            voca_id = len(self.vocas)
            self.vocas_id[term] = voca_id
            self.vocas.append(term)
            self.docfreq.append(0)
        else:
            voca_id = self.vocas_id[term]
        return voca_id

    def doc_to_ids(self, doc):
        list = []
        words = dict()
        for term in doc:
            id = self.term_to_id(term)
            list.append(id)
            if not id in words:
                words[id] = 1
                self.docfreq[id] += 1
        return list


    def __getitem__(self, v):
        return self.vocas[v]
    
    def size(self):
        return len(self.vocas)

