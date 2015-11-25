import math
from pprint import pprint
import numpy as np
import operator
import copy


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
            # just an alias
            word = term[0]
            df = term[1]
            self.weightTerms[word] = {}
            # inverse document frequency
            idf = math.log10(self.N / df)
            for doc in self.terms[term]:
                tf = self.terms[term][doc]
                weight = (1 + math.log10(tf)) * idf
                # count length of document to normalizing later
                self.lengths[doc] = self.lengths.get(doc, 0) + math.pow(weight, 2)
                self.weightTerms[word][doc] = round(weight, 6)
        for key in self.lengths:
            self.lengths[key] = round(math.sqrt(self.lengths[key]), 6)

    def printWeights(self):
        # self.lengths = np.sqrt(self.lengths.values())
        pprint(self.weightTerms)
        pprint(self.lengths)

    # count terms in query
    # and do scoring
    def immitateTerms(self, queryArr):
        terms = {}
        for token in queryArr:
            terms[token] = terms.get(token, 0) + 1
        weights = {}
        for token in terms:
            tf = terms[token]
            for term in self.terms:
                word = term[0]
                df = term[1]
                if(word == token):
                    idf = math.log10(self.N / df)
                    weights[token] = (1 + math.log10(tf)) * idf
        return weights

    def calculateQueryLength(self, weights):
        weightList = list(weights.values())
        return math.sqrt(sum([pow(weight, 2) for weight in weightList]))

    def calculateCosineScore(self, query):
        scores = {}
        queryArr = query.split()
        qWeights = self.immitateTerms(queryArr)
        qLength = self.calculateQueryLength(qWeights)
        for qTerm in qWeights:
            if qTerm in self.weightTerms:
                for doc in self.weightTerms[qTerm]:
                    scores[doc] = scores.get(doc, 0) + self.weightTerms[qTerm][doc] * qWeights[qTerm]
        for doc in scores:
            scores[doc] = round(scores[doc] / (self.lengths[doc] * qLength), 6)
        self.scores = scores
        return scores

    def combineWithRanking(self, ranking, scores = False):
        if(not scores):
            scores = copy.deepcopy(self.scores)
        #  based on harmonic mean of two numbers, src:
        #  https://en.wikipedia.org/wiki/Harmonic_mean#Harmonic_mean_of_two_numbers
        for doc in scores:
            x1 = ranking.get(doc, 0)
            x2 = scores[doc]
            scores[doc] = 2 * (x1 * x2) / (x1 + x2)
        self.scoresWithRanking = scores

    def getScoresWithRanking(self):
        scores = self.scoresWithRanking
        return self.sortScore(scores)

    def getCosineScores(self):
        scores = self.scores
        return self.sortScore(scores)

    def sortScore(self, scores):
        sorted_score = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_score

    def getLengthOfDocs(self):
        return self.lengths
