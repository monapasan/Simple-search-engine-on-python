from pprint import pprint


class Indexing(object):
    def __init__(self, stopWords):
        self.terms = {}
        self.docs = {}
        self.stopWords = stopWords

    def start(self):
        self.minifyDocs()
        self.tokenize()

    def minifyDocs(self):
        self.minDocs = {}
        # self.minDocs = [(self.docs[name[1]], name[0])
        # for name in enumerate(self.docs, 1)]
        for name in enumerate(self.docs, 1):
            key = name[1].split('/')[-1]
            # key = name[0]
            self.minDocs[key] = self.docs[name[1]]
        # pprint(self.minDocs)

    def addDoc(self, page, soup):
        if(page not in self.docs):
            self.docs[page] = self.normalize(soup.getText())

    def normalize(self, text):
        text = ' '.join(text.split())
        # TODO: replace with regex
        text = text.lower().replace(',', ' ').replace(';', ' ')
        text = text.replace(':', ' ').replace('/', ' ').replace('.', ' ')
        terms = list(filter(None, text.split(' ')))
        return terms

    def tokenize(self):
        terms = {}
        docs = self.minDocs
        for doc in docs:
            docArr = docs[doc]
            for token in docArr:
                if token in self.stopWords:
                    continue
                if not terms.get(token, False):
                    terms[token] = {}
                if(doc not in terms[token]):
                    terms[token][doc] = 1
                else:
                    terms[token][doc] += 1
        self.terms = terms
        return self.terms

    def getTerms(self):
        return self.terms

    def buildDocFreq(self):
        x = [(token, len(self.terms[token])) for token in self.terms]
        for key in x:
            self.terms[key] = self.terms.pop(key[0])
        return x

    def getTerms(self):
        return self.terms

    def printTerms(self):
        # pprint(self.terms)
        # pprint(len(self.terms))
        self.buildDocFreq()
        # pprint(self.terms)
