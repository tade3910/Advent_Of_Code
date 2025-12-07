from collections import deque

START = "S"
END = "E"
WALL = "#"

def inWorld(row:int,col:int,track:list[list[str]]):
    return row >= 0 and col >= 0 and row < len(track) and col < len(track[row])

def getToEnd(track:list[list[str]],start:tuple[int,int],end:tuple[int,int]):
    queu:deque[tuple[int,int]] = deque()
    prev = {start:None}
    raceTimes = {start:0}
    queu.append(start)
    visited = set([start])
    while queu:
        curr = queu.popleft()
        row,col  = curr
        raceTime = raceTimes[curr]
        for displacement in [(0,-1),(0,1),(-1,0),(1,0)]:
            neigborRow, neigborCol = row + displacement[0], col + displacement[1]
            neigbor = neigborRow,neigborCol
            if neigbor in visited:
                continue
            visited.add(neigbor)
            if not inWorld(neigborRow,neigborCol,track):
                continue
            if track[neigborRow][neigborCol] == WALL:
                continue
            queu.append(neigbor)
            prev[neigbor] = curr
            raceTimes[neigbor] = raceTime + 1
            if neigbor == end:
                return raceTimes,prev
    return raceTimes,prev
    

def cheat(track:tuple[int,int],end:tuple[int,int],prevs:dict[tuple[int,int],tuple[int,int]],raceTimes:dict[tuple[int,int],int],threshhold:int):
    curr = prevs[end]
    timeSaves:dict[int,list[str]] = {}
    greaterThan = 0
    while curr != None:
        row,col = curr
        oldTime = raceTimes[curr]
        for wallDisplacement in [(0,-1),(0,1),(-1,0),(1,0)]:
            wallRow, wallCol = row + wallDisplacement[0], col + wallDisplacement[1]
            if not inWorld(wallRow,wallCol,track):
                continue
            if track[wallRow][wallCol] != WALL:
                continue
            wall = wallRow,wallCol
            for displacement in [(0,-1),(0,1),(-1,0),(1,0)]:
                cheatRow, cheatCol = wallRow + displacement[0], wallCol + displacement[1]
                cheatLocation = cheatRow,cheatCol
                if cheatLocation == curr:
                    continue
                if not inWorld(cheatRow,cheatCol,track):
                    continue
                if track[cheatRow][cheatCol] == WALL:
                    continue
                if cheatLocation not in raceTimes:
                    continue
                newTime = raceTimes[cheatLocation]
                timeSaved = newTime - oldTime - 2
                if timeSaved > 0:
                    curTimeSavesList = timeSaves.get(timeSaved,[])
                    curTimeSavesList.append(f"{curr} -> {wall} -> {cheatLocation}")
                    timeSaves[timeSaved] = curTimeSavesList
                    if timeSaved >= threshhold:
                        greaterThan += 1
        curr = prevs[curr]
    return timeSaves,greaterThan


def getTrack(fileName:str):
    with open(fileName, 'r') as file:
        track = []
        start = 0,0
        end = 0,0
        for i,line in enumerate(file):
            curLine = line.strip()
            curRow = []
            for j,col in enumerate(curLine):
                curRow.append(col)
                if col == END:
                    end = i,j
                elif col == START:
                    start = i,j
            track.append(curRow)
        return track,start,end

def getBestCheatCounts(fileName:str,threshhold:int):
    track,start,end = getTrack(fileName)
    raceTimes,prevs = getToEnd(track,start,end)
    timeSaves,greaterThan = cheat(track,end,prevs,raceTimes,threshhold)
    # for key,val in timeSaves.items():
    #     print(f"There are {len(val)} cheats that save {key} picoseconds")
    return greaterThan

def main():
    print(getBestCheatCounts("test.txt",40))
    print(getBestCheatCounts("input.txt",100))
    # print(getBestCheatCounts("input.txt",70,1024))

if __name__ == "__main__":
    main()


