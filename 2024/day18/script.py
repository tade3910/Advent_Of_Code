from collections import deque
import time
def inWorld(row:int,col:int,boundary:int):
    return row >= 0 and col >= 0 and row <= boundary and col <= boundary

def getToEnd(corruptedMemory:set[tuple[int,int]],boundary):
    queu = deque()
    start = 0,0,0
    end = boundary,boundary
    queu.append(start)
    explored = set()
    while queu:
        curEntry = queu.popleft()
        row,col,distance  = curEntry
        curr = row,col
        if curr in explored:
            continue
        explored.add(curr)
        if curr == end:
            return distance
        for displacement in [(0,-1),(0,1),(-1,0),(1,0)]:
            neigborRow, neigborCol = row + displacement[0], col + displacement[1]
            neigbor = neigborRow,neigborCol
            if not inWorld(neigborRow,neigborCol,boundary):
                continue
            if neigbor in corruptedMemory:
                continue
            queu.append((neigborRow,neigborCol,distance + 1))
    return None
    

def traceBack(prev:dict[tuple[int,int],tuple[int,int]],boundary:int,corruptedMemory:set[tuple[int,int]]):
    world = [["."] * (boundary + 1) for _ in range(boundary + 1)]
    for memory in corruptedMemory:
        row,col = memory
        world[row][col] = "#"

    end = boundary,boundary
    stack = [end]
    while stack:
        curr = stack.pop()
        if curr == None:break
        row,col = curr
        world[row][col] = 'O'
        stack.append(prev[(row,col)])
    return world


def getCorruptedMemory(fileName:str,simulate:int | None=None):
    with open(fileName, 'r') as file:
        corruptedMemory = []
        for i,line in enumerate(file):
            if simulate != None and i == simulate:
                break
            parsed = line.strip().split(",")
            row = int(parsed[1])
            col = int(parsed[0])
            corruptedMemory.append((row,col))
        return corruptedMemory

def getFirstCorrupted(fileName:str,boundary:int):
    corruptedMemory = getCorruptedMemory(fileName)
    left, right = 0, len(corruptedMemory) - 1
    result = -1  # Default if no False is found
    while left <= right:
        mid = (left + right) // 2
        currentCorruptedMemory = set(corruptedMemory[:mid])
        if getToEnd(currentCorruptedMemory,boundary) == None:
            result = mid  # Update result since we found a False
            right = mid - 1  # Look to the left to find the first False
        else:
            left = mid + 1  # Look to the right for the first False
    if result != -1:
        row,col = corruptedMemory[result - 1]
        return col,row
    return result

def getShortestPath(fileName:str,boundary:int,simulate:int):
    corruptedMemory = getCorruptedMemory(fileName,simulate)
    distance = getToEnd(corruptedMemory,boundary)
    return distance

def main():
    startTime = time.time() 
    print(getShortestPath("test.txt",6,12))
    endTime = time.time()
    runTime = endTime - startTime
    print(f"completed in {runTime * 1000:.4f} ms")

    startTime = time.time() 
    print(getShortestPath("input.txt",70,1024))
    endTime = time.time()
    runTime = endTime - startTime
    print(f"completed in {runTime * 1000:.4f} ms")

    startTime = time.time() 
    print(getFirstCorrupted("test.txt",6))
    endTime = time.time()
    runTime = endTime - startTime
    print(f"completed in {runTime * 1000:.4f} ms")
    
    startTime = time.time() 
    print(getFirstCorrupted("input.txt",70))
    endTime = time.time()
    runTime = endTime - startTime
    print(f"completed in {runTime * 1000:.4f} ms")

if __name__ == "__main__":
    main()



