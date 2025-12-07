from copy import deepcopy
def getTriangles(key:str,networkMap:dict[str,set[str]]):
    curList = list(networkMap[key])
    triangles = []
    for i in range(len(curList) - 1):
        curAdd = curList[i]
        curAddSet = networkMap[curAdd]
        for j in range(i + 1,len(curList)):
            val = curList[j]
            if val in curAddSet:
                triangle = tuple(sorted([key, curAdd, val]))
                triangles.append(triangle)
    return triangles

def getThreeComputerParties(fileName:str):
    networkMap = parseInput(fileName)
    threeComputerParties = []
    seen = set()
    for key in networkMap.keys():
        if key[0] == "t":
            triangles = getTriangles(key,networkMap)
            for triangle in triangles:
                if triangle not in seen:
                    threeComputerParties.append(triangle)
                    seen.add(triangle)
    print(len(threeComputerParties))
    return threeComputerParties

def getBiggerGroups(networkMap:dict[str,set[str]],curGroup:tuple[str]):
    groupSet = set(curGroup)
    potentialAdds = list(networkMap[curGroup[0]])
    groups = []
    for i in range(len(potentialAdds)):
        val = potentialAdds[i]
        if val not in groupSet:
            toAdd = True
            for k in range(1, len(curGroup)):
                if val not in networkMap[curGroup[k]]:
                    toAdd = False
                    break
            if toAdd:
                addedGroup = deepcopy(list(curGroup))
                addedGroup.append(val)
                groups.append(tuple(sorted(addedGroup)))
    return groups

def getBigestParty(fileName:str):
    networkMap = parseInput(fileName)
    parties = []
    seen = set()
    for key in networkMap.keys():
        triangles = getTriangles(key,networkMap)
        for triangle in triangles:
            if triangle not in seen:
                parties.append(triangle)
                seen.add(triangle)
    while len(parties) > 1:
        nextParties = []
        for party in parties:
            biggerGroups = getBiggerGroups(networkMap,party)
            for biggerGroup in biggerGroups:
                if biggerGroup not in seen:
                    nextParties.append(biggerGroup)
                    seen.add(biggerGroup)
        parties = nextParties
    print(",".join(parties[0]))
    return parties

def parseInput(fileName:str):
    networkMap:dict[str,set[str]] = {}
    with open(fileName, 'r') as file:
        for line in file:
            computers = line.strip().split('-')
            first = computers[0]
            second = computers[1]
            curFirst = networkMap.get(first,set())
            curFirst.add(second)
            networkMap[first] = curFirst
            curSecond = networkMap.get(second,set())
            curSecond.add(first)
            networkMap[second] = curSecond
    return networkMap

getThreeComputerParties("test.txt")
getThreeComputerParties("input.txt")
getBigestParty("test.txt")
getBigestParty("input.txt")