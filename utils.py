def dictionify(keyList, valueList):
    retDict = {}
    for key, value in zip(keyList ,valueList):
        retDict[key] = value
    return retDict

def dictionifyString(string, splitTerm, numType):
    retDict = {}
    key, values = string.split(splitTerm)
    retDict[key] = numType(values)
    return retDict