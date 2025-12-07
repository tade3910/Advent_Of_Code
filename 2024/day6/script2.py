#!/usr/bin/python3
import copy
def setUpMap(fileName:str):
    map = []
    startingPosition = (0,0)
    rowNumb = 0
    with open(fileName, 'r') as file:
        for line in file:
            row = []
            curLine = line.strip()
            for colNumb in range(len(curLine)):
                val = curLine[colNumb]
                if val == '^':
                    startingPosition = rowNumb,colNumb
                row.append((val,''))
            map.append(row)
            rowNumb = rowNumb + 1               
    return startingPosition,map

def getNextMove(direction:str,row:int,col:int):
    if direction == "^":
        return row -1,col
    if direction == 'd':
        return row + 1,col
    if direction == '<':
        return row,col - 1
    if direction == '>':
        return row,col + 1
    raise RuntimeError(f"I did smth wrong,because direction shouldn't be {direction}")

def inMap(row:int,col:int,map:list[list[tuple[str,str]]]):
    return row < len(map) and row >= 0 and col < len(map[row]) and col >= 0

def turn90(direction:str):
    if direction == "^":
        return '>'
    if direction == 'd':
        return '<'
    if direction == '<':
        return '^'
    if direction == '>':
        return 'd'
    raise RuntimeError(f"I did smth wrong,because direction shouldn't be {direction}")

def getPrevDirections(prevDirections:str,direction:str):
    return f"{prevDirections}{direction}"

def move(row:int,col:int,map:list[list[tuple[str,str]]]):
    direction,curPrevs = map[row][col]
    nextRow,nextCol = getNextMove(direction,row,col)
    if not inMap(nextRow,nextCol,map): return nextRow,nextCol
    nextPosition,prevDirections = map[nextRow][nextCol]
    if nextPosition == '#' or nextPosition == 'O':
        map[row][col] = turn90(direction), getPrevDirections(curPrevs,direction)
        return row,col
    map[nextRow][nextCol] = direction,prevDirections
    map[row][col] = 'X',getPrevDirections(curPrevs,direction)
    return nextRow,nextCol
    
def isLoop(row:int,col:int,map:list[list[tuple[str,str]]]):
    val,prevDirection = map[row][col]
    return val in prevDirection


def checkLoop(map:list[list[tuple[str,str]]],row:int,col:int):
    while inMap(row,col,map):
        if isLoop(row,col,map):
            return True
        row,col = move(row,col,map)
    return False

def nextObstacle(row:int,col:int,map:list[list[tuple[str,str]]]):
    direction,_ = map[row][col]
    nextRow,nextCol = getNextMove(direction,row,col)
    if not inMap(nextRow,nextCol,map): return nextRow,nextCol,direction
    nextPosition,_ = map[nextRow][nextCol]
    if nextPosition == '#':
        return row,col,turn90(direction)
    return nextRow,nextCol,direction

def countObstacles(curPosition:tuple[int,int],map:list[list[tuple[str,str]]],count:int = 0):
    beenBefore = set()
    row,col = curPosition
    originalRow,originalCol = row,col
    direction = map[row][col]
    prevMap = copy.deepcopy(map)
    while True: 
        updatedMap = copy.deepcopy(map)
        prevRow,prevCol = row,col
        row,col,direction = nextObstacle(row,col,prevMap)
        while (row == originalRow and col == originalCol) or f"row:{row}col:{col}" in beenBefore:
            prevMap[row][col] = direction,direction
            row,col,direction = nextObstacle(row,col,prevMap)
        if not inMap(row,col,map):
            return count
        updatedMap[row][col] = 'O','O'
        prevMap[prevRow][prevCol] = 'X','X'
        prevMap[row][col] = direction,direction
        beenBefore.add(f"row:{row}col:{col}")
        beenBefore.add(f"row:{prevRow}col:{prevCol}")
        if checkLoop(updatedMap,originalRow,originalCol): 
            count = count + 1


def getNumPositions(fileName:str):
    curPosition,map = setUpMap(fileName)
    count = countObstacles(curPosition,map)
    return count


def main():
    print(getNumPositions('input.txt'))
   
if __name__ == "__main__":
    main()