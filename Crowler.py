import urllib.request
import urllib.error
from bs4 import BeautifulSoup
from Frontier import Frontier
import pprint
# import html.parser
from html.parser import HTMLParser

dataFromSite = []


# class myHtmlParser(HTMLParser):
#     def handle_data(self, data):
#         if data != '/n':
#             dataFromSite.append(data)
#
# myParsInstance = myHtmlParser()

# fromUser = input('Which one?\n')


def getUrl(number):
    return 'http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI'\
        '-Dozenten/Classen/DAWeb/smdocs/d0' + str(number) + '.html'


def getAllUrl():
    return [getUrl(1), getUrl(4), getUrl(8)]


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
soup = readUrl(getUrl(fromUser))

# Retrieve all of the anchor tags
tags = soup.get_text()


def getText():
    textFromSite = ''
    for item in dataFromSite:
        # print(item)
        textFromSite += item
    return textFromSite

urls = getAllUrl()
myFrontier = Frontier(getAllUrl())


def createLinksStructure(froniter):
    linkStructure = {}

    def addLinks(soupLinks, page):
        linkStructure[page] = {}
        for link in soupLinks:
            href = link.get('href')
            if(href not in linkStructure[page]):
                linkStructure[page][href] = 1
            else:
                linkStructure[page][href] += 1

    for page in froniter.forParsing:
        soup = readUrl(page)
        soupLinks = soup.find_all('a')
        addLinks(soupLinks, page)

    return linkStructure
linkStructure = createLinksStructure(myFrontier)


pprint.pprint(linkStructure)


# for i in range(count):
#     tempUrl = tags[position].get('href')
#     print('Retriving ' + str(tempUrl))
#     tempSoup = readUrl(tempUrl)
#     tags = tempSoup.find_all('a')
# myParsInstance.feed(html)
# myParsInstance.close()
# print(html)
