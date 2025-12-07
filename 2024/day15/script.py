#!/usr/bin/python3

#cur location is always O and need to be moved
def moveOs(world:list[list[str]],curLocation:tuple[int,int],displacement:tuple[int,int]):
    curRow,curCol = curLocation
    nextRow,nextCol = curRow + displacement[0], curCol + displacement[1]
    if world[nextRow][nextCol] == '#':
        return False
    elif world[nextRow][nextCol] == '.' or moveOs(world,(nextRow,nextCol),displacement):
        world[curRow][curCol] = '.'
        world[nextRow][nextCol] = 'O'
        return True
    return False

def getDisplacement(direction:str):
    if direction == '^':
        return -1,0
    elif direction == 'v':
        return 1,0
    elif direction == '<':
        return 0,-1
    else:
        return 0,1

    
def makeMove(world:list[list[str]],direction:str,robotLocation:tuple[int,int]):
    displacement = getDisplacement(direction)
    curRow,curCol = robotLocation
    nextRow,nextCol = curRow + displacement[0], curCol + displacement[1]
    if world[nextRow][nextCol] == 'O' and moveOs(world,(nextRow,nextCol),displacement):
        world[curRow][curCol] = '.'
        world[nextRow][nextCol] = '@'
        return nextRow,nextCol
    elif world[nextRow][nextCol] == '.':
        world[curRow][curCol] = '.'
        world[nextRow][nextCol] = '@'
        return nextRow,nextCol
    else: return robotLocation

def getGPSSum(world:list[list[str]]):
    sum = 0
    for i,row in enumerate(world):
        for j,col in enumerate(row):
            if col == 'O':
                sum += (100 * i + j)
    return sum

def parseInput(fileName:str):
    with open(fileName, 'r') as file:
        world:list[list[str]] = []
        moves = ""
        parseMoves = False
        robotLocation = (0,0)
        for i,line in enumerate(file):
            line = line.strip()
            if len(line) == 0:
                parseMoves = True
                continue
            if not parseMoves:
                row =[]
                for j,char in enumerate(line):
                    row.append(char)
                    if char == '@':
                        robotLocation = i,j
                world.append(row)
            else:
                moves += line
        
        for move in moves:
            robotLocation = makeMove(world,move,robotLocation)
        print(getGPSSum(world))
        
        
       
parseInput("test.txt")
parseInput("test1.txt")
parseInput("input.txt")

