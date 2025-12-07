#!/usr/bin/python3
def findTrailHeads(input:list[list[str]]):
    trailHeadLocations = []
    for row,line in enumerate(input):
        for col,val in enumerate(line):
            if val == '0':
                trailHeadLocations.append((row,col))
    return trailHeadLocations

def isInWorld(row,col,world:list[list]):
    return row >= 0 and row < len(world) and col >= 0 and col < len(world[row])

def find9s(row:int,col:int,input:list[list[str]],found:set[str],prev:int=-1):
    if not isInWorld(row,col,input):
        return 0
    curVal = input[row][col]
    if curVal == '.':
        return 0
    curVal = int(curVal)
    if prev + 1 != curVal:
        return 0
    if curVal == 9:
        found.add(f"{row}:{col}")
        return 1
    return (find9s(row,col -1,input,found,curVal) + 
            find9s(row,col + 1,input,found,curVal) +
            find9s(row - 1,col,input,found,curVal) + 
            find9s(row + 1,col,input,found,curVal))
   

def parseInput(fileName:str):
     input = []
     with open(fileName, 'r') as file:
        for line in file:
            input.append(line.strip())
        trailHeads = findTrailHeads(input)
        part1Count = 0
        part2Count = 0
        for trailHead in trailHeads:
            row,col = trailHead
            found = set()
            part2Count = part2Count + find9s(row,col,input,found)
            part1Count = part1Count + len(found)
        return part1Count,part2Count

def main():
    print(parseInput('input.txt'))
    print(parseInput('test6.txt'))

if __name__ == "__main__":
    main()

    
            
