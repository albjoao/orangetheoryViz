def dictionify(keyList, valueList):
    retDict = {}
    for key, value in zip(keyList ,valueList):
        retDict[key] = value
    return retDict