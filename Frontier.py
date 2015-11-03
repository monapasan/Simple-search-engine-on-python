

class Frontier(object):
    def __init__(self, urls):
        self.parsed = []
        self.forParsing = urls

    def getNext(self):
        el = self.forParsing.pop()
        self.parsed.append(el)
        return el
