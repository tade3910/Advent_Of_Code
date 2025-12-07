#!/usr/bin/python3

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
                visited = False
                if val == '^':
                    startingPosition = rowNumb,colNumb
                    visited = True
                row.append((val,visited))
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

def inMap(row:int,col:int,map:list[list[tuple[str]]]):
    return row < len(map) and col < len(map[row])

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


def move(row:int,col:int,map:list[list[tuple[str,str]]]):
    direction,_ = map[row][col]
    nextRow,nextCol = getNextMove(direction,row,col)
    if not inMap(nextRow,nextCol,map): return nextRow,nextCol,direction
    nextPosition,_ = map[nextRow][nextCol]
    if nextPosition == '#':
        return row,col,turn90(direction)
    return nextRow,nextCol,direction

    

def countMoves(curPosition:tuple[int,int],map:list[list[tuple[str]]],count:int = 1):
    row,col = curPosition
    while inMap(row,col,map): 
        newPosition,row,col = move(row,col,map)
        count = count + newPosition
    return count


def getNumPositions(fileName:str):
    curPosition,map = setUpMap(fileName)
    count = countMoves(curPosition,map)
    return count
