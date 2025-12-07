def parseInput(fileName:str):
    locks:list[list[int]] = []
    keys:list[list[int]] = []
    with open(fileName, 'r') as file:
        availableHeight = -2
        for line in file:
            line = line.strip()
            if len(line) == 0: break
            availableHeight += 1
    with open(fileName, 'r') as file:
        isLock = True
        firstLine = True
        cur:list[int] = []
        for line in file:
            line = line.strip()
            if firstLine:
                firstLine = False
                for char in line:
                    cur.append(0)
                    if char != "#":
                        isLock = False
            elif len(line) == 0:
                if isLock:
                    locks.append(cur)
                else:
                    for index in range(len(cur)):
                        cur[index] -= 1
                    keys.append(cur)
                isLock = True
                firstLine = True
                cur = []
            else:
                for index,char in enumerate(line):
                    if char == "#":
                        cur[index] += 1
        #Get last part
        if isLock:
            locks.append(cur)
        else:
            for index in range(len(cur)):
                cur[index] -= 1
            keys.append(cur)
    return locks,keys,availableHeight


def isOverlap(key:list[int],lock:list[int],availableHeight:int):
    for index in range(len(key)):
        sumHeight = key[index] + lock[index]
        if sumHeight > availableHeight: return False 
    return True

def countOverlaps(keys:list[list[int]],locks:list[list[int]],availableHeight:int):
    count = 0
    for lock in locks:
        for key in keys:
            if isOverlap(key,lock,availableHeight):
                count += 1
    return count

locks,keys,availableHeight = parseInput("test.txt")
print(countOverlaps(keys,locks,availableHeight))

locks,keys,availableHeight = parseInput("input.txt")
print(countOverlaps(keys,locks,availableHeight))

