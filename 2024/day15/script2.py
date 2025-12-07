#!/usr/bin/python3

LEFTBOX = '['
RIGHTBOX = ']'
OLDBOX = 'O'
WALL = '#'
FREESPACE = '.'
ROBOT = '@'


#cur location is always O and need to be moved
def moveBoxes(world:list[list[str]],curLocation:tuple[int,int],direction:str):
    if direction == '^':
        return moveBoxesVertically(world,curLocation,-1)
    elif direction == 'v':
        return moveBoxesVertically(world,curLocation,1)
    elif direction == '<':
        return moveBoxesLeft(world,(curLocation[0],curLocation[1] + 1))
    else:
        return moveBoxesRight(world,curLocation)

def getDisplacement(direction:str):
    if direction == '^':
        return -1,0
    elif direction == 'v':
        return 1,0
    elif direction == '<':
        return 0,-1
    else:
        return 0,1


def moveBoxesLeft(world:list[list[str]],curLocation:tuple[int,int]):
    curRow,curCol = curLocation
    nextRow,nextCol = curRow, curCol - 2
    if world[nextRow][nextCol] == WALL:
        return False
    elif world[nextRow][nextCol] == FREESPACE or moveBoxesLeft(world,(nextRow,nextCol)):
        world[curRow][curCol] = FREESPACE
        world[curRow][curCol - 1] = RIGHTBOX
        world[nextRow][nextCol] = LEFTBOX
        return True
    return False

def moveBoxesRight(world:list[list[str]],curLocation:tuple[int,int]):
    curRow,curCol = curLocation
    nextRow,nextCol = curRow, curCol + 2
    if world[nextRow][nextCol] == WALL:
        return False
    elif world[nextRow][nextCol] == FREESPACE or moveBoxesRight(world,(nextRow,nextCol)):
        world[curRow][curCol] = FREESPACE
        world[curRow][curCol + 1] = LEFTBOX
        world[nextRow][nextCol] = RIGHTBOX
        return True
    return False

def doVerticalMove(world:list[list[str]],curLocation:tuple[int,int],displacement:int):
    row,leftCol = curLocation
    rightCol = leftCol + 1
    nextRow = row + displacement
    world[nextRow][leftCol] = world[row][leftCol]
    world[nextRow][rightCol] = world[row][rightCol]
    world[row][leftCol] = '.'
    world[row][rightCol] = '.'

def moveBoxesVertically(world:list[list[str]],curLocation:tuple[int,int],displacement:int):
    row,leftCol = curLocation
    rightCol = leftCol + 1
    nextRow = row + displacement
    if world[nextRow][leftCol] == WALL or world[nextRow][rightCol] == WALL:
        return False
    elif world[nextRow][leftCol] == FREESPACE:
        if world[nextRow][rightCol] == FREESPACE or moveBoxesVertically(world,(nextRow,leftCol + 1),displacement):
            doVerticalMove(world,curLocation,displacement)
            return True
    elif world[nextRow][rightCol] == FREESPACE and moveBoxesVertically(world,(nextRow,leftCol - 1),displacement):
        doVerticalMove(world,curLocation,displacement)
        return True
    else:
        if world[nextRow][leftCol] == LEFTBOX: # moving 1
            if moveBoxesVertically(world,(nextRow,leftCol),displacement):
                doVerticalMove(world,curLocation,displacement)
                return True
        elif moveBoxesVertically(world,(nextRow,leftCol - 1),displacement) and moveBoxesVertically(world,(nextRow,leftCol + 1),displacement):
            #2 being moved
            doVerticalMove(world,curLocation,displacement)
            return True
    return False
        
    
def makeMove(world:list[list[str]],direction:str,robotLocation:tuple[int,int]):
    displacement = getDisplacement(direction)
    curRow,curCol = robotLocation
    nextRow,nextCol = curRow + displacement[0], curCol + displacement[1]
    moved = False
    if world[nextRow][nextCol] == LEFTBOX:
        leftCol = nextCol
        if moveBoxes(world,(nextRow,leftCol),direction):
            moved = True
    elif world[nextRow][nextCol] == RIGHTBOX:
        leftCol = nextCol - 1
        if moveBoxes(world,(nextRow,leftCol),direction):
            moved = True
    elif world[nextRow][nextCol] == '.':
        moved = True

    if moved:
        world[curRow][curCol] = '.'
        world[nextRow][nextCol] = '@'
        return nextRow,nextCol
    else: return robotLocation
    
def getGPSSum(world:list[list[str]]):
    sum = 0
    for i,row in enumerate(world):
        for j,col in enumerate(row):
            if col == LEFTBOX:
                sum += (100 * i + j)
    return sum

def addDuplicateMove(tile:str,row:list[str]): 
    if tile == WALL:
        row.append(tile)
        row.append(WALL)
    elif tile == OLDBOX:
        row.append(LEFTBOX)
        row.append(RIGHTBOX)
    elif tile == FREESPACE:
        row.append(tile)
        row.append(tile)
    else:
        row.append(ROBOT)
        row.append(FREESPACE)

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
                    if char == '@':
                        robotLocation = i,j * 2
                    addDuplicateMove(char,row)
                world.append(row)
            else:
                moves += line
        for k,move in enumerate(moves):
            robotLocation = makeMove(world,move,robotLocation)
        print(getGPSSum(world))
        
        
       
# parseInput("test3.txt")
parseInput("test1.txt")
parseInput("input.txt")

