from bs4 import BeautifulSoup
from gmailReader import GmailReader
from utils import dictionify

class OrangeHTMLParser():
    def __init__(self, message):
        self.message = message
        self._cleanRawMessage()
        self.soup = BeautifulSoup(self.message, 'html.parser')
    #Functions to Parse Document
    def _cleanRawMessage(self):
        self.message = self.message.replace('=\r\n', '')
    def parseTD(self):
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
        values = [self.tdStrings[self.tdStrings.index(x)-1] for x in titles]
        return dictionify(titles, values)



if __name__ == "__main__":
    gmail = GmailReader()
    messages = gmail.getUnreadMessages()
    for message in messages:
        otParser = OrangeHTMLParser(message)
        otParser.parseTD()
        #print(otParser.tdStrings)
        print(otParser.getZones())
        print(otParser.getWorkoutSummary())
