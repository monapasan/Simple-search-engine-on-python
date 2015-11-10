from pprint import pprint


class Indexing(object):
    def __init__(self):
        self.terms = {}
        self.docs = {}

    def start(self):
        self.minifyDocs()
        self.tokenize()

    def minifyDocs(self):
        self.minDocs = {}
        for name in self.docs:
            key = name.split('/')[-1]
            self.minDocs[key] = self.docs[name]

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
                if not terms.get(token, False):
                    terms[token] = []
                if(doc not in terms[token]):
                    terms[token].append(doc)
        self.terms = terms
        return self.terms

    def getTerms(self):
        return self.terms

    def printTerms(self):
        pprint(self.terms)
        pprint(len(self.terms))
