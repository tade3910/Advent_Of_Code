#!/usr/bin/python3

def getRowColStr(row:int,col:int):
    return f"{row}:{col}"

def strToRowCol(formatedString:str):
    strList = formatedString.split(':')
    row = int(strList[0])
    col = int(strList[1])
    return row,col

def getAntenaLocations(fileName:str):
    antenaLocations:set[str] = set()
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
                    antenaLocations.add(location)
            row = row + 1
    return antenaLocations,lines

def isInWorld(row,col,world:list[list]):
    return row >= 0 and row < len(world) and col >= 0 and col < len(world[row])

def getMatchindCords(curRow:int,curCol:int,antenaRow:int,antenaCol:int):
    rowDif = antenaRow - curRow
    colDif = antenaCol - curCol
    matchingRow = antenaRow + rowDif
    matchingCol = antenaCol + colDif
    return matchingRow,matchingCol

def isAntiNodeLocation(row:int,col:int,antenaLocations:set[str],lines:list[list[str]]):
    for location in antenaLocations:
        locationRow,locationCol = strToRowCol(location)
        matchingRow,matchingCol = getMatchindCords(row,col,locationRow,locationCol)
        antenaType = lines[locationRow][locationCol]
        if matchingRow != locationRow and matchingCol != locationCol and isInWorld(matchingRow,matchingCol,lines) and lines[matchingRow][matchingCol] == antenaType:
            return True
    return False

def countLocations(fileName:str):
    antenaLocations,lines = getAntenaLocations(fileName)
    antinodeLocations = 0
    for row in range(len(lines)):
        line = lines[row]
        for col in range(len(line)):
            if isAntiNodeLocation(row,col,antenaLocations,lines): 
                antinodeLocations = antinodeLocations + 1
            

    return antinodeLocations

def main():
    # print(countLocations('test.txt'))
    # print(countLocations('test2.txt'))
    # print(countLocations('test3.txt'))
    print(countLocations('input.txt'))

if __name__ == "__main__":
    main()