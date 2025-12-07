from functools import cache

# def convertDirectionToDirection(originalDirection:str):
#     direction = ""
#     row,col = directionCharToIndex("A")
#     for char in originalDirection:
#         nextRow,nextCol = directionCharToIndex(char)
#         colChange = getColChange(col,nextCol)
#         rowChange = getRowChange(row,nextRow)
#         if row == 0 and nextCol == 0:
#             # We touch blank if we move col first so move row first
#             direction += rowChange + colChange
#         else:
#             direction += colChange + rowChange
#         direction += "A"
#         row,col = nextRow,nextCol
#     return direction

def convertPasswordToDirection(password:str):
    direction = ""
    row,col = passwordCharToIndex("A")
    for char in password:
        nextRow,nextCol = passwordCharToIndex(char)
        colChange = getColChange(col,nextCol)
        rowChange = getRowChange(row,nextRow)
        if row == 3 and nextCol == 0:
            # We touch blank if we move col first so move row first
            direction += rowChange + colChange
        else:
            direction += colChange + rowChange
        direction += "A"
        row,col = nextRow,nextCol
    return direction


# def getShortestSequence(password:str):
#     directions = []
#     direction = convertPasswordToDirection(password)
#     directions.append(direction)
#     for _ in range(2):
#         nextDirection = convertDirectionToDirection(direction)
#         direction = nextDirection
#         directions.append(direction)
#     return direction,directions


def getColChange(currCol:int,nextCol:int):
    if currCol == nextCol: return ""
    colChange = ">" if nextCol > currCol else  "<"
    diff = abs(nextCol - currCol)
    return colChange * diff

def getRowChange(currRow:int,nextRow:int):
    if currRow == nextRow: return ""
    rowChange = "^" if nextRow < currRow else  "v"
    diff = abs(nextRow - currRow)
    return rowChange * diff

def directionCharToIndex(char:str):
    if char == " ":
        return 0,0
    elif char == "^":
        return 0,1
    elif char == "A":
        return 0,2
    elif char == "<":
        return 1,0
    elif char == "v":
        return 1,1
    elif char == ">":
        return 1,2
    else:
        raise Exception("Invalid direction char passed")
    
def passwordCharToIndex(char:str):
    if char == "7":
        return 0,0
    elif char == "8":
        return 0,1
    elif char == "9":
        return 0,2
    elif char == "4":
        return 1,0
    elif char == "5":
        return 1,1
    elif char == "6":
        return 1,2
    elif char == "1":
        return 2,0
    elif char == "2":
        return 2,1
    elif char == "3":
        return 2,2
    elif char == " ":
        return 3,0
    elif char == "0":
        return 3,1
    elif char == "A":
        return 3,2
    else:
        raise Exception("Invalid password char passed")

@cache
def convertToDirection(start:str,end:str):
    directions = set(["<","v",">","^"])
    if start in directions or end in directions:
        #we're using num pad
        empty = directionCharToIndex(" ")
        startRow,startCol = directionCharToIndex(start)
        endRow,endCol = directionCharToIndex(end)
        colChange = getColChange(startCol,endCol)
        rowChange = getRowChange(startRow,endRow)
        rowDiff,colDiff = endRow - startRow, endCol - startCol
        if empty != (0,colDiff):
            if rowDiff > 0 or empty == (rowDiff,0):
                return rowChange + colChange + "A"
        return colChange + rowChange + "A"
    else:
        startRow,startCol = passwordCharToIndex(start)
        endRow,endCol = passwordCharToIndex(end)
        colChange = getColChange(startCol,endCol)
        rowChange = getRowChange(startRow,endRow)
        return colChange + rowChange + "A"

        
@cache
def length(code, depth, s=0):
    if depth == 0: return len(code)
    for i, c in enumerate(code):
        s += length(convertToDirection(code[i-1], c), depth-1)
    return s

def parseInput(fileName:str):
    sequences = []
    with open(fileName, 'r') as file:
        for line in file:
            sequences.append(line.strip())
    return sequences

def getSum(fileName:str):
    codes = parseInput(fileName)
    print(sum(int(code[:-1]) * length(code, 3) for code in codes))
    print(sum(int(code[:-1]) * length(code, 26) for code in codes))

print(getSum("input.txt"))
# print(getSum("input.txt"))


