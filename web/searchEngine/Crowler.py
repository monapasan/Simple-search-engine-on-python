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
import os
dataFromSite = []

# read text files
# stop words will be avoided by Indexing
# urls will be crowl by Crowler
stopWordsPath = os.path.join(os.path.dirname(__file__), "stop_words.txt")
urlsToCrowlPath = os.path.join(os.path.dirname(__file__), "urlsToCrowl.txt")
urls = open(urlsToCrowlPath).read().split()
stopWords = open(stopWordsPath).read()
stopWords = stopWords.replace('\n', " ").replace("'", "").replace(',', '')
stopWords = ' '.join(stopWords.split()).split(' ')


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
            # newPage = getDocFromUrl(page)
            linkStructure[page] = linkStructure.pop(page)

    for page in frontier.forParsing:
        soup = readUrl(page)
        myIndexing.addDoc(page, soup)
        soupLinks = soup.find_all('a')
        addLinks(soupLinks, page)

    return linkStructure

isNotTest = True

myIndexing = Indexing(stopWords)
myFrontier = Frontier(urls)
linkStructure = createLinksStructure(myFrontier)

pr = toMatrix(linkStructure)
myIndexing.start()
# Number of Documents
N = len(myIndexing.docs)
myScoring = Scoring(myIndexing.terms, N)


def getLength():
    return myScoring.getLengthOfDocs()


def getLinkStruktur():
    return linkStructure


def getPageRank():
    return pr


def getTerms():
    return myIndexing.terms


def startSearching(query):
    scores = myScoring.calculateCosineScore(query)
    myScoring.combineWithRanking(pr)
    res = {}
    res['PageRank'] = pr
    res['CosineScore'] = myScoring.getCosineScores()
    res['WithRanking'] = myScoring.getScoresWithRanking()
    return res
