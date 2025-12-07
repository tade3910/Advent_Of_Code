#!/usr/bin/python3

#PART1
def isValidLine(value:int,args:list[int],index:int=0,current:int = 0) -> bool:
    if index == 0:
        current = args[0]
    if index == len(args) - 1:
        return current == value
    if current > value: return False
    nextIndex = index + 1
    next = args[nextIndex]
    return isValidLine(value, args, nextIndex,  current + next) or isValidLine(value, args, nextIndex, current * next)

def parseLine(line:str) -> tuple[int,list[int]]:
    arr = line.split(':')
    val = int(arr[0].strip())
    args = list(map(int, arr[1].strip().split()))
    return val,args
    
def sumTrueEqautions(fileName:str):
    sum = 0
    with open(fileName, 'r') as file:
        for line in file:
            value,args = parseLine(line.strip())
            if isValidLine(value,args): 
                sum = sum + value 
    return sum

#PART2
def isSpecialValid(value:int,args:list[int],index:int=0,current:int = 0) -> bool:
    if index == 0:
        current = args[0]
    if index == len(args) - 1:
        return current == value
    if current > value: return False
    nextIndex = index + 1
    next = args[nextIndex]
    return isSpecialValid(value, args, nextIndex,  current + next) or isSpecialValid(value, args, nextIndex, current * next) or isSpecialValid(value,args,nextIndex,int(f"{current}{next}"))


def sumSpecialEquations(fileName:str):
    sum = 0
    with open(fileName, 'r') as file:
        for line in file:
            value,args = parseLine(line.strip())
            if isSpecialValid(value,args): 
                sum = sum + value 
    return sum

def main():
    print(sumTrueEqautions('input.txt'))
    print(sumSpecialEquations('input.txt'))

if __name__ == "__main__":
    main()