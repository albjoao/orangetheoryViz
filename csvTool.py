import os
from gmailReader import GmailReader
from parseOrangeTheory import OrangeHTMLParser

class CSVTool():
    def __init__(self, path):
        self.path = path
    def createCSV(self, columns):
        with open(self.path, 'w') as f:
            line = ';'.join(columns) + '\n'
            f.write(line)
    def addLine(self, data):
        with open(self.path, 'a') as f:
            line = ';'.join( str(x) for x in data.values()) + '\n'
            f.write(self.removeUnicode(line))
    def removeUnicode(self, line):
        newLine = ''
        for char in line:
            if char != u'\u200c':
                newLine += char
        return newLine

if __name__ == "__main__":
    test = CSVTool('test.csv')
    gmail = GmailReader()
    messages = gmail.getUnreadMessages()
    workouts = []
    for message in messages:
        otParser = OrangeHTMLParser(message)
        workouts.append(otParser.getWorkOut())
    
    keys = workouts[0].keys()
    test.createCSV(keys)
    for workout in workouts:
        test.addLine(workout)