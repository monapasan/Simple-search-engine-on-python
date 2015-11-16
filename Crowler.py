import urllib.request
import urllib.error
from bs4 import BeautifulSoup
from Frontier import Frontier
from pprint import pprint
from PageRank import toMatrix
from PageRank import pageRank
# import html.parser
from html.parser import HTMLParser
from urllib.parse import urljoin
from Indexing import Indexing
from Scoring import Scoring
dataFromSite = []

isNotTest = input('Is it testMode? \n yes or no \n')
switcher = {'yes': True, 'no': False}
isNotTest = switcher.get(isNotTest.lower(), True)

stopWordsPath = './stop_words.txt'
stopWords = open(stopWordsPath).read()
stopWords = stopWords.replace('\n', " ").replace("'", "").replace(',', '')
stopWords = ' '.join(stopWords.split()).split(' ')


def getUrl(number):
    return 'http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI'\
        '-Dozenten/Classen/DAWeb/smdocs/d0' + str(number) + '.html'


def getAllUrl():
    return [getUrl(1), getUrl(6), getUrl(8)]


def readUrl(url):
    try:
        html = urllib.request.urlopen(url).read()
    except urllib.error.URLError as e:
        print(e.reason)
    soup = BeautifulSoup(html, 'html.parser')
    return soup

# try:
#     handle = urllib.request.urlopen(getUrl(fromUser))
# except urllib.error.URLError as e:
#     print(e.reason)

# html = handle.read(getUrl(fromUser))
# soup = readUrl(getUrl(fromUser))

# Retrieve all of the anchor tags
# tags = soup.get_text()


def getText():
    textFromSite = ''
    for item in dataFromSite:
        # print(item)
        textFromSite += item
    return textFromSite

urls = getAllUrl()
myIndexing = Indexing(stopWords)
myFrontier = Frontier(getAllUrl())


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
linkStructure = createLinksStructure(myFrontier)


matrix = toMatrix(linkStructure)
pr = pageRank(matrix)
myIndexing.start()
myIndexing.printTerms()
# Number of Documents
N = len(myIndexing.docs)
pprint(N)
myScoring = Scoring(myIndexing.terms, N)
myScoring.printWeights()
pprint(myScoring.cosineScore('classification'))
# pprint(myScoring.terms)
# pprint(myScoring.immitateTerms(['a', 'a', 'asd', 'token']))
