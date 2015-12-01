import searchEngine.Crowler as Crowler


def startSearch(query):
    return Crowler.startSearching(query)


def getlength():
    return Crowler.getLength()


def getlinkstruktur():
    return Crowler.getLinkStruktur()


def getpagerank():
    return Crowler.getPageRank()


def getterms():
    return Crowler.getTerms()
