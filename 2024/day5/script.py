#!/usr/bin/python3
import math
def updatePrePostMaps(pre:dict[int,set],post:dict[int,set],input:str):
    line = input.split("|")
    postVal = line[0]
    preVal = line[1]
    if pre.get(preVal,False): pre[preVal].add(postVal)
    else: pre[preVal] = set([postVal]) 
    if post.get(postVal,False): post[postVal].add(preVal)
    else: post[postVal] = set([preVal])

def validPre(postSet:set[int],before:set[int]):
    for num in before:
        if num in postSet: return False
    return True

def validPost(preSet:set[int],after:set[int]):
    for num in after:
        if num in preSet: return False
    return True

def getBeforeAndAfter(index:int,fixedLine:int):
    if index == 0:
        return set(),set(fixedLine)
    if index == len(fixedLine):
        return set(fixedLine), set()
    return set(fixedLine[0:index]), set(fixedLine[index : len(fixedLine)])

def fixedLineMid(line:list,pre:dict[int,set],post:dict[int,set]):
    fixedLine = [line[0]]
    for val in line[1:]:
        index = 0
        for index in range(len(fixedLine) + 1):
            before,after = getBeforeAndAfter(index,fixedLine)
            preSet = pre.get(val,set())
            postSet = post.get(val,set())
            if validPre(postSet,before) and validPost(preSet,after):
                fixedLine.insert(index,val)
                break
    mid = math.floor(len(fixedLine)  /2)
    return fixedLine[mid]

def sumMidFixedLines(pre:dict[int,set],post:dict[int,set],curLine:str):
    values = curLine.split(",")
    for i in range(len(values)):
        value = values[i]
        preSet = pre.get(value,set())
        postSet = post.get(value,set())
        before = set(values[0:i])
        after = set(values[i+1:len(values)])
        if not validPre(postSet,before) or not validPost(preSet,after): return fixedLineMid(values,pre,post)
    return 0

def sumMiddlePageNumbers(pre:dict[int,set],post:dict[int,set],curLine:str):
    values = curLine.split(",")
    for i in range(len(values)):
        value = values[i]
        preSet = pre.get(value,set())
        postSet = post.get(value,set())
        before = set(values[0:i])
        after = set(values[i+1:len(values)])
        if not validPre(postSet,before) or not validPost(preSet,after): return 0
    mid = math.floor(len(values)  /2)
    return values[mid]

def parseFile():
    with open('input.txt', 'r') as file:
        getConfig = True
        pre = {}
        post = {}
        count = 0
        for line in file:
            curLine = line.strip()
            if curLine == "": 
                getConfig = False
                continue
            if getConfig:
                updatePrePostMaps(pre,post,curLine)
            else:
                count = count +int(sumMiddlePageNumbers(pre,post,curLine))
    return count

def parseFileFixes():
    with open('input.txt', 'r') as file:
        getConfig = True
        pre = {}
        post = {}
        count = 0
        for line in file:
            curLine = line.strip()
            if curLine == "": 
                getConfig = False
                continue
            if getConfig:
                updatePrePostMaps(pre,post,curLine)
            else:
                count = count +int(sumMidFixedLines(pre,post,curLine))
    return count

def main():
    print(parseFile())
    print(parseFileFixes())


if __name__ == "__main__":
    main()