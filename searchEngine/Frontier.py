

class Frontier(object):
    def __init__(self, urls):
        self.parsed = []
        self.forParsing = urls

    def getNext(self):
        el = self.forParsing.pop()
        if(el in self.parsed):
            return self.getNext()
        self.parsed.append(el)
        return el

    def addLink(self, link):
        if(link not in self.forParsing):
            self.forParsing.append(link)
