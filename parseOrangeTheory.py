from bs4 import BeautifulSoup
from gmailReader import GmailReader
from utils import dictionify

class OrangeHTMLParser():
    def __init__(self, message):
        self.message = message
        self._cleanRawMessage()
        self.soup = BeautifulSoup(self.message, 'html.parser')
        self._parseTD()

    #Functions to Parse Document
    def _cleanRawMessage(self):
        self.message = self.message.replace('=\r\n', '')

    def _parseTD(self):
        self.tdStrings = []
        for td in self.soup.find_all('td'):
            if td.string:
                self.tdStrings.append(td.string)
    
    #Functions to get info we want
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
        print(otParser.getMetaData())
        print(otParser.getWorkoutSummary())
        print(otParser.getZones())
