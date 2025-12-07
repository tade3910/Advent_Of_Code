#!/usr/bin/python3

def getDiskRepresentation(input:str):
    diskRepresntation:list[str] = []
    i = 0
    for index,val in enumerate(input) :
        id = i
        if index % 2 == 1:
            i = i + 1
            id = '.'
        for _ in range(int(val)):
            diskRepresntation.append(id)
    return diskRepresntation

def get2dMapAndLens(input:str):
    diskRepresntation:list[list[list[str]]] = []
    lens = []
    i = 0
    for index,val in enumerate(input) :
        id = i
        if index % 2 == 1:
            id = '.'
        else:
            diskRepresntation.append([])
            lens.append(int(val))
        cur = []
        for _ in range(int(val)):
            cur.append(id)
        diskRepresntation[i].append(cur)
        if index % 2 == 1:
            i = i + 1
    return diskRepresntation,lens

def update2dMap(diskRepresntation:list[list[list[str]]],lens:list):
    i = len(diskRepresntation) - 1
    while i > 0:
        cur = diskRepresntation[i][0]
        curLen = lens[i]
        for j in range(i):
            entry = diskRepresntation[j]
            emptySpace = entry[-1]
            remainder = len(emptySpace) - curLen
            if remainder >= 0 and emptySpace[0] == '.':
                moveUp = curLen < len(cur)
                entry[-1] = entry[-1][0:remainder]
                diskRepresntation[i][0] = cur[curLen:]
                for _ in range(curLen): 
                    if moveUp:
                        diskRepresntation[i - 1][-1].append('.')
                    else:
                        diskRepresntation[i][-1].append('.')
                    entry[0].append(cur[0])
                break           
        i = i-1

def count2dChecksum(diskRepresntation:list[list[list[str]]]):
    # I know it's inneffient, lol I don't care wanted to do it like this
    # wanted to see the change infront of me
    checkSum = 0
    index = 0
    for entryTuple in diskRepresntation:
        entry = entryTuple[0]
        skips = 0
        if len(entryTuple) == 2 : skips = len(entryTuple[1]) 
        for val in entry:
            if val != '.':
                checkSum = checkSum + (index * int(val))
            index = index + 1
        index = index + skips
    return checkSum


def getCheckSum(diskRepresntation:list[str]):
    checkSum = 0
    left = 0
    right = len(diskRepresntation) - 1
    while left <= right:
        if diskRepresntation[left] == '.':
            while left <= right and diskRepresntation[right] == '.':
                right = right - 1
            diskRepresntation[left] = diskRepresntation[right]
            diskRepresntation[right] = '.'
            right = right - 1
        checkSum = checkSum + (left * diskRepresntation[left])
        left = left + 1
    return checkSum
        
def calculateChecksum(fileName:str):
    with open(fileName, 'r') as file:
        lines = []
        for line in file:
            lines.append(line)
        input = lines[0]
        diskRepresntation = getDiskRepresentation(input)
        return getCheckSum(diskRepresntation)
    return 0

def doPart2(fileName:str):
    with open(fileName, 'r') as file:
        lines = []
        for line in file:
            lines.append(line)
        input = lines[0]
        diskRepresntation,lens = get2dMapAndLens(input)
        update2dMap(diskRepresntation,lens)
        return count2dChecksum(diskRepresntation)
    return 0


def main():
    print(calculateChecksum("input.txt")) #O(n) Tehee
    print(doPart2('input.txt')) 

if __name__ == "__main__":
    main()