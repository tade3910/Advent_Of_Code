
import heapq
WALL = '#'
START = 'S'
END = 'E'
import time
def getOpositeDirection(direction:str):
     if direction == 'E':
          return 'W'
     elif direction == 'W':
          return 'E'
     elif direction == 'N':
          return 'S'
     else:
          return 'N'

def getNeigbor(currentDirection:str,displacement:tuple[int,int,str],curentRow:int,currentCol:int):
     neigborDirection = displacement[2] 
     if neigborDirection == currentDirection:
          return curentRow + displacement[0],currentCol + displacement[1],1
     elif neigborDirection == getOpositeDirection(currentDirection):
          return curentRow,currentCol,2000
     else:
          return curentRow,currentCol,1000

def exploreNeigbors(world:list[list[str]],currentEntry:tuple[int,int,str],currentDistance,queu:list[tuple[int,int,str]],distances:dict[tuple[int,int,str],int],prevs:dict[tuple[int,int,str],list[tuple[int,int,str]]]):
        curentRow,currentCol,currentDirection = currentEntry
        displacements = [(-1,0,'N'),(1,0,'S'),(0,-1,'W'),(0,1,'E')]
        for displacement in displacements:
             neigborRow,neigborCol,scoreChange = getNeigbor(currentDirection,displacement,curentRow,currentCol)
             if world[neigborRow][neigborCol] == WALL: 
                  continue
             neigborDirection = displacement[2]
             newDistance = currentDistance + scoreChange
             neigborEntry = neigborRow,neigborCol,neigborDirection
             oldDistance = distances.get(neigborEntry,float('inf'))
             if newDistance <= oldDistance:
                  if newDistance < oldDistance:
                       prevs[neigborEntry] = []
                       distances[neigborEntry] = newDistance
                  prevs[neigborEntry].append(currentEntry)
                  heapq.heappush(queu,(newDistance,neigborEntry))    
             
def dikstras(world:list[list[str]],start:tuple[int,int]):
    queu = []
    startRow,startCol = start
    startEntry = startRow,startCol,'E'
    distances = {startEntry:0}
    visited = set()
    prevs = {startEntry:None}
    heapq.heappush(queu,(0,startEntry))
    while queu:
        currentDistance,currentEntry = heapq.heappop(queu)
        if currentEntry in visited: continue
        visited.add(currentEntry)
        exploreNeigbors(world,currentEntry,currentDistance,queu,distances,prevs)
    return distances,prevs

def getPossibleEnds(endEntry:tuple[int,int]):
    possibilities = []
    endRow,endCol = endEntry
    for direction in ['N','S','E','W']:
         possibilities.append((endRow,endCol,direction))
    return possibilities
     

#row 7 col 5
def countTiles(prevs:dict[tuple[int,int,str],list[tuple[int,int,str]]],endEntry:tuple[int,int,str],startEntry:tuple[int,int,str]):
    startLocation = startEntry[0],startEntry[1]
    endLocation = endEntry[0],endEntry[1]
    tiles = set([startLocation,endLocation])
    queu = [endEntry]
    while queu:
    #   print(f"curLocation is {curLocation} and distance is {distances[curLocation]}")
        curLocation = queu.pop()
        if curLocation == startEntry:
             continue
        for prev in prevs[curLocation]:
             tile = (prev[0],prev[1])
             tiles.add(tile)
             queu.append(prev)
    return len(tiles)

def getShortest(distances:dict[tuple[int, int, str], int],endLocation:tuple[int,int]):
    possibleEnds = getPossibleEnds(endLocation)
    shortestEnd = 0
    for i in range(len(possibleEnds)):
        if distances[possibleEnds[i]] < distances[possibleEnds[shortestEnd]]:
            shortestEnd = i
    return distances[possibleEnds[shortestEnd]],possibleEnds[shortestEnd]

def parseInput(fileName:str):
    startTime = time.time() 
    with open(fileName, 'r') as file:
        world:list[list[str]] = []
        endLocation = (0,0)
        startLocation = (0,0)
        for i,line in enumerate(file):
            row = []
            for j,char in enumerate(line.strip()):
                row.append(char)
                if char == START:
                      startLocation = (i,j)
                elif char == END:
                     endLocation = (i,j)
            world.append(row)
        
        distances,prevs = dikstras(world,startLocation)
        distance,endEntry = getShortest(distances,endLocation)
        startEntry = (startLocation[0],startLocation[1],'E')
        count = countTiles(prevs,endEntry,startEntry)
        print(f"distance is {distance} and count is {count}")
        endTime = time.time()
        runTime = endTime - startTime
        print(f"completed in {runTime:.4f} seconds")

def main():
    parseInput('test.txt')
    parseInput('test2.txt')
    parseInput('input.txt')

if __name__ == "__main__":
     main()



