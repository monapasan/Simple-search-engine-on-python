class PageRank(object):
    OUTPUT_FILENAME = "page_ranks.txt"

    # standard konstruktor, werte wie in aufgabe vorgegeben
    def __init__(self):
        self.daempfung = 0.95
        self.teleportation = 0.05
        # delta-Schwellwert zum Abbruch
        self.deltaCancel = 0.04

    # test matrix erstellen und zurückgeben
    def generateMatrix(self):
        matrix = [
            [0, 1, 1, 1, 0, 0, 0, 0],
            [1, 0, 1, 1, 1, 0, 0, 0],
            [1, 1, 0, 1, 1, 0, 0, 0],
            [1, 1, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]
        return matrix

    # Zählt die Inlinks und Outlinks
    # erwartet eine Matrix als Parameter
    # return: dictionary -> {pageNumber : [inlinks], [outlinks]}
    def checkLinks(self, mtx):
        matrixSize = len(mtx)
        result = {}
        # 1. iteration - outlinks in dictionary eintragen
        for row in range(matrixSize):
            # 2 Arrays erstellen, in denen out- und inlinks gespeichert werden
            result[row] = [],[]
            for col in range(matrixSize):
                # outlink adden
                if mtx[row][col] == 1:
                    result[row][0].append(col)

        # 2. iteration - inlinks in dictionary eintragen
        for col in range(matrixSize):
            for row in range(matrixSize):
                if mtx[row][col] == 1:
                    result[col][1].append(row)

        # dictionary zurückgeben -> {pageNumber : [inlinks, outlinks]}
        return result

    # formatiert PageRank Ergebniss zur Ausgabe / Speicherung
    # return formatierter String
    def formatOutput(self, pRanks):
        # header
        s = "\t\t"
        for i in range(1,9):
            s += "d0" + str(i) + "\t"
        s += "diff"
        # zeilen beschriften
        for row in range(len(pRanks)):
            s += "\n step: " + str(row) + "\t"
            # pageranks hinzufügen
            for col in range(len(pRanks[1])):
                s += '{:1.4f}'.format(pRanks[row][col]) + "\t"
        # formatierten String zurückgeben
        return s

    # speichert das PageRank Ergebnis in einer lokalen Datei
    # erwartet einen Dateinamen und formatierten String als Parameter
    def saveToFile(self, fileName, pRankString):
        file = open(fileName, "w")
        file.write(pRankString)
        file.close()

    # main Funktion zur PageRank Berechnung
    # erwartet eine Matrix als Parameter
    def getPageRank(self, mtx):
        # Matrix für PageRank Ergebnisse
        pageRanks = [[]]
        # Seitenzahl
        pageCount = len(mtx)

        # inlinks und outlinks aus matrix bestimmen, gibt Dictionary zurück
        links = self.checkLinks(mtx)

        # pageRanks initialisieren
        for i in range(pageCount):
            # Initialwert = 1 / Seitenzahl
            pageRanks[0].append(1.0 / pageCount)
        # delta startwert hinzufügen für einfachere Formatierung später
        pageRanks[0].append(0)

        # delta und step initialisieren
        delta = 1
        step = 0

        # solange der errechnete delta-Wert größer als Abbruchbedingung ist
        while delta > self.deltaCancel:
            # delta resetten
            delta = 0
            pageRanks.append([])
            # für jede Seite Pi
            for pi in range(pageCount):
                # neu berechneter Pagerank
                pr = 0
                # für jede Seite Pj
                for pj in range(pageCount):
                    # PageRank der Seite pj in Schritt k (vorheriger Schritt)
                    rk = pageRanks[step][pj]

                    # schaue in inlinks, ob pj auf pi verweist -> Backlink
                    if pj in links[pi][1]:
                        # pr = alter PageRank / Outlinks
                        pr += rk / len(links[pj][0])

                    # wenn es keine Outlinks gibt
                    elif len(links[pj][0]) == 0:
                        # alter PageRank / Seitenzahl
                        pr += rk / pageCount
                # dämpfung und teleportation einberechnen
                pr = (pr * self.daempfung) + (self.teleportation / pageCount)
                # neu berechneten PageRank hinzufügen
                pageRanks[step + 1].append(pr)
                # delta Berechnung, berechnet positiven Teil
                delta += abs(pr - pageRanks[step][pi])
            # delta hinzufügen
            pageRanks[step + 1].append(delta)
            step += 1
        # Ergebnis formatieren
        output = self.formatOutput(pageRanks)
        # Ergebnis ausgeben
        print(output)
        # Ergebnis in lokale Datei speichern
        self.saveToFile(self.OUTPUT_FILENAME, output)
        # Ergebnis zurückgeben
        return pageRanks

p = PageRank()
matrix = p.generateMatrix()
p.getPageRank(matrix)
