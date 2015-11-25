import urllib.request
import urllib.error
from bs4 import BeautifulSoup
from searchEngine.Frontier import Frontier
from pprint import pprint
from searchEngine.PageRank import toMatrix
from searchEngine.PageRank import pageRank
# import html.parser
from html.parser import HTMLParser
from urllib.parse import urljoin
from searchEngine.Indexing import Indexing
from searchEngine.Scoring import Scoring
dataFromSite = []


def getUrl(number):
    return 'http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten'\
        '/WI-Dozenten/Classen/DAWeb/smdocs/d0' + str(number) + '.html'


def getAllUrl():
    return [getUrl(1), getUrl(6), getUrl(8)]


def readUrl(url):
    try:
        html = urllib.request.urlopen(url).read()
    except urllib.error.URLError as e:
        print(e.reason)
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def getText():
    textFromSite = ''
    for item in dataFromSite:
        # print(item)
        textFromSite += item
    return textFromSite


def getDocFromUrl(url):
    # TODO: should check if the url from current Page
    # return url.split('/').pop().split('.').pop(0)
    return url.split('/').pop()


def createLinksStructure(frontier):
    linkStructure = {}

    def addLinks(soupLinks, page):
        linkStructure[page] = {}
        for link in soupLinks:
            href = link.get('href')
            # add next Link for Parse
            frontier.addLink(urljoin(page, href))
            if(href not in linkStructure[page]):
                linkStructure[page][href] = 1
            else:
                linkStructure[page][href] += 1
        if(isNotTest):
            newPage = getDocFromUrl(page)
            linkStructure[newPage] = linkStructure.pop(page)

    for page in frontier.forParsing:
        soup = readUrl(page)
        myIndexing.addDoc(page, soup)
        soupLinks = soup.find_all('a')
        addLinks(soupLinks, page)

    return linkStructure

# isNotTest = input('Is it testMode? \n yes or no \n')
# switcher = {'yes': True, 'no': False}
# isNotTest = switcher.get(isNotTest.lower(), True)
isNotTest = True
stopWordsPath = 'web/searchEngine/stop_words.txt'
stopWords = open(stopWordsPath).read()
stopWords = stopWords.replace('\n', " ").replace("'", "").replace(',', '')
stopWords = ' '.join(stopWords.split()).split(' ')
urls = getAllUrl()
myIndexing = Indexing(stopWords)
myFrontier = Frontier(getAllUrl())
linkStructure = createLinksStructure(myFrontier)

pr = toMatrix(linkStructure)
# pr = pageRank(matrix)
pprint('PageRank: ')
pprint(pr)
myIndexing.start()
myIndexing.printTerms()
# Number of Documents
N = len(myIndexing.docs)
pprint(N)
myScoring = Scoring(myIndexing.terms, N)


def getLength():
    return myScoring.getLengthOfDocs()


def getLinkStruktur():
    return linkStructure


def getPageRank():
    return pr


def startSearching(query):
    # myScoring.printWeights()
    scores = myScoring.calculateCosineScore(query)
    myScoring.combineWithRanking(pr)
    res = {}
    pprint(query)
    # pprint('Without Ranking: ')
    pprint(scores)
    pprint(myScoring.getCosineScores())
    # pprint('With Ranking:')
    pprint(myScoring.getScoresWithRanking())
    res['PageRank'] = pr
    res['CosineScore'] = myScoring.getCosineScores()
    res['WithRanking'] = myScoring.getScoresWithRanking()
    return res

# pprint(myScoring.terms)
# pprint(myScoring.immitateTerms(['a', 'a', 'asd', 'token']))
