import math
from pprint import pprint
import numpy as np

class Scoring(object):
    # N number of Documents
    def __init__(self, terms, N):
        self.terms = terms
        self.N = N
        self.measureWeight()

    def measureWeight(self):
        self.weightTerms = {}
        self.lengths = {}
        for term in self.terms:
            word = term[0]
            df = term[1]
            self.weightTerms[word] = {}
            idf = math.log10(self.N / df)
            for doc in self.terms[term]:
                weight = (1 + math.log10(self.terms[term][doc])) * idf
                self.lengths[doc] = self.lengths.get(doc, 0) + math.pow(weight, 2)
                # pprint(weight)
                self.weightTerms[word][doc] = round(weight, 4)

    def printWeights(self):
        # self.lengths = np.sqrt(self.lengths.values())
        for key in self.lengths:
            self.lengths[key] = round(math.sqrt(self.lengths[key]), 6)
        pprint(self.weightTerms)
        pprint(self.lengths)
    # def produceLengths(self):
    #

    def immitateTerms(self, queryArr):
        terms = {}
        for token in queryArr:
            if not terms.get(token, False):
                terms[token] = 1
            else:
                terms[token] += 1
        # return [(token, terms[token]) for token in terms]
        weights = {}
        for token in terms:
            df = terms[token]
            idf = math.log10(self.N / df)
            weights[token] = (1 + math.log10(df))
        return weights

    def cosineScore(self, query):
        scores = {}
        queryArr = query.split(' ')
        qWeights = self.immitateTerms(queryArr)
        print(qWeights)
        for qTerm in qWeights:
            for term in self.weightTerms:
                # if qTerm in self.weightTerms:
                if qTerm == term:
                    for doc in self.weightTerms[qTerm]:
                        scores[doc] = scores.get(doc, 0) + self.weightTerms[qTerm][doc] * qWeights[qTerm]
                        pprint(qTerm)
                        # pprint(self.weightTerms[qTerm][doc])
        for doc in scores:
            pprint(self.lengths[doc])
            scores[doc] = scores[doc] / self.lengths[doc]
        return scores
