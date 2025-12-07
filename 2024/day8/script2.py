#!/usr/bin/python3

def getRowColStr(row:int,col:int):
    return f"{row}:{col}"

def strToRowCol(formatedString:str):
    strList = formatedString.split(':')
    row = int(strList[0])
    col = int(strList[1])
    return row,col

def getAntenaLocations(fileName:str):
    antenaLocations:dict[str,set[str]] = {}
    lines = []
    with open(fileName, 'r') as file:
        row = 0
        for line in file:
            line = line.strip()
            lines.append(line)
            for col in range(len(line)):
                val = line[col]
                if val != '.':
                    #We're at an antena
                    location = getRowColStr(row,col)
                    if val not in antenaLocations:
                        antenaLocations[val] = set([location])
                    else:
                        antenaLocations[val].add(location)
            row = row + 1
    return antenaLocations,lines

def isInWorld(row,col,world:list[list]):
    return row >= 0 and row < len(world) and col >= 0 and col < len(world[row])


def getDifs(row:int,col:int,locationRow:int,locationCol:int):
    rowDif = locationRow - row
    colDif = locationCol - col
    return rowDif,colDif        

def getMatch(row:int,rowDif:int,col:int,colDif:int):
    matchingRow = row + rowDif
    matchingCol = col + colDif
    return matchingRow,matchingCol

def getAntiNodeLocations(coordinates:set[str],lines:list[list[str]],antiNodes:set,part2 = True):
    for coordinate in coordinates:
        for otherCoordinate in coordinates:
            if otherCoordinate != coordinate:
                row,col = strToRowCol(coordinate)
                otherRow,otherCol = strToRowCol(otherCoordinate)
                rowDif,colDif = getDifs(row,col,otherRow,otherCol)
                matchingRow,matchingCol = getMatch(otherRow,rowDif,otherCol,colDif)
                if isInWorld(matchingRow,matchingCol,lines): antiNodes.add(getRowColStr(matchingRow,matchingCol))
                if not part2: continue
                antiNodes.add(coordinate)
                antiNodes.add(otherCoordinate)
                matchingRow,matchingCol = getMatch(matchingRow,rowDif,matchingCol,colDif)
                while isInWorld(matchingRow,matchingCol,lines):
                    antiNodes.add(getRowColStr(matchingRow,matchingCol))
                    matchingRow,matchingCol = getMatch(matchingRow,rowDif,matchingCol,colDif)


# Optimized solution for part1 and part2 solution
def countLocations(fileName:str):
    antenaLocations,lines = getAntenaLocations(fileName)
    antiNodes = set()
    part1Nodes = set()
    for antenaCords in antenaLocations.values():
        getAntiNodeLocations(antenaCords,lines,antiNodes)
        getAntiNodeLocations(antenaCords,lines,part1Nodes,False)
    return len(antiNodes),len(part1Nodes)

def main():
    print(countLocations('input.txt'))

if __name__ == "__main__":
    main()