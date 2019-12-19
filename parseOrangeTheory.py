from bs4 import BeautifulSoup
from gmailReader import GmailReader
from utils import dictionify, dictionifyString

class OrangeHTMLParser():
    def __init__(self, message):
        self.message = message
        self._cleanRawMessage()
        self.soup = BeautifulSoup(self.message, 'html.parser')
        self._parseTD()

    #Functions to Parse Document
    def _cleanRawMessage(self):
        self.message = self.message.replace('=\r\n', '')
        self.message = self.message.replace('=C2=A0', '')
        self.message = self.message.replace('=E2=80=8C', '')

    def _parseTD(self):
        self.tdStrings = []
        for td in self.soup.find_all('td'):
            if td.string:
                self.tdStrings.append(td.string)

    def getPeakHR(self):
        for p in self.soup.find_all('p'):
            if p.find('span') and "Peak HR" in p.getText():
                return dictionifyString(p.getText(), ':', int)

    def getTreadmillPerfomanceTotals(self):
        keys = ['Total Distance', 'Total Time']
        for table in self.soup.find_all('table'):
            if table.find('tbody') and \
                len(table.tbody.find_all('tr')) == 1 and \
                'Total' in table.getText():
                    treadTotals = table.getText().encode('ascii', 'ignore').decode('ascii')
                    treadTotals = treadTotals.replace(keys[0], ' ')
                    treadTotals = treadTotals.replace(keys[1], ' ')
                    treadTotals = treadTotals.replace(' miles ', ' ').split(' ')
                    treadTotals[0] = float(treadTotals[0])
                    return dictionify(keys, treadTotals)

    #Functions to get info we want
    #TODO still need to get treadmill data and peak heart rate
    #get name of person preforming exercise
    def getZones(self):
        startIndex = self.tdStrings.index('MINUTES / ZONE')
        zonesList = ['Grey', "Blue", "Green", "Orange", "Red"]
        subList = self.tdStrings[startIndex - 5 : startIndex]
        return dictionify(zonesList, subList)
    
    def getWorkoutSummary(self):
        titles = ['CALORIES BURNED', 'SPLAT POINTS', 'AVG. HEART-RATE', 'STEPS']
        values = [self.tdStrings[self.tdStrings.index(title)-1] for title in titles]
        return dictionify(titles, values)
    
    def getMetaData(self):
        keys = ['Location', 'Date', 'Time', 'Coach']
        values = self.tdStrings[1:5]
        return dictionify(keys, values)



if __name__ == "__main__":
    gmail = GmailReader()
    messages = gmail.getUnreadMessages()
    for message in messages:
        otParser = OrangeHTMLParser(message)
        print(otParser.getTreadmillPerfomanceTotals())
        print(otParser.getMetaData())
        print(otParser.getWorkoutSummary())
        print(otParser.getZones())
        print('******')
