#!/usr/bin/python3
import re
import math
def teleport(position,boundary):
    if position <  0:
        position *= -1
        multiplier = int(math.ceil(position / boundary))
        actualBoundary = multiplier * boundary
        return actualBoundary - position
    return position % boundary

def getPosition(x:int,y:int,dx:int,dy:int,height:int,width:int,seconds:int):
    curX = x + (seconds * dx)
    curY = y + (seconds * dy)
    curX = teleport(curX,width)
    curY = teleport(curY,height)
    return curX,curY

def getQuadrant(leftBoundary:int,topBoundary:int,x:int,y:int):
    if x < leftBoundary:
        if y < topBoundary:
            return "TL"
        elif y > topBoundary:
            return "BL"
    elif x > leftBoundary:
        if y < topBoundary:
            return "TR"
        elif y > topBoundary:
            return "BR"
    return "M"

def getSafetyFactor(robotsInfo:list,height:int=7,width:int=11,seconds:int=100):
    leftBoundary = int(width/2)
    topBoundary = int(height/2)
    quadrants = {
        "TL":0,
        "BL":0,
        "TR":0,
        "BR":0
    }
    for robot in robotsInfo:
        x,y,dx,dy = robot
        curX, curY = getPosition(x,y,dx,dy,height,width,seconds)
        quadrant = getQuadrant(leftBoundary,topBoundary,curX,curY)
        if quadrant != "M":
            quadrants[quadrant]+=1
    safetyFactor = 1
    for count in quadrants.values():
        safetyFactor *= count
    return safetyFactor

def checkTouching(robotsInfo:list,height:int=103,width:int=101):
    seconds = 0
    nextToEachOther = 0
    robotCount = len(robotsInfo)

    while nextToEachOther * 2 < robotCount:
        nextToEachOther = 0
        seconds += 1
        curPositions = set()
        for robot in robotsInfo:
            x,y,dx,dy = robot
            curPosition = getPosition(x,y,dx,dy,height,width,seconds)
            curPositions.add(curPosition)
        
        
        #Bryan hinted if most are next to each other it'll be a tree
        for position in curPositions:
            for otherPosition in curPositions:
                if position == otherPosition: # Can't consider the same robot
                    continue
                robotX,robotY = position
                otherX,otherY = otherPosition
                # check same X
                if robotX == otherX:
                    Ydif = abs(robotY - otherY)
                    if Ydif <= 1: 
                        nextToEachOther +=1
                        break
                #check same Y
                if robotY == otherY:
                    Xdif = abs(robotX - otherX)
                    if Xdif <= 1: 
                        nextToEachOther +=1
                        break
        print(f"nextToEachOther is {nextToEachOther} and seconds is {seconds}")
    return seconds

                

def parseInput(fileName:str):
    with open(fileName, 'r') as file:
        robotsInfo = []
        for line in file:
            positionMatch = re.search(r"p=(-?\d+),(-?\d+)", line)
            velocityMatch = re.search(r"v=(-?\d+),(-?\d+)", line)
            x = int(positionMatch.group(1))
            y = int(positionMatch.group(2))
            dx = int(velocityMatch.group(1))
            dy = int(velocityMatch.group(2))
            robot = x,y,dx,dy
            robotsInfo.append(robot)
        return robotsInfo

def main():
    test = parseInput("test.txt")
    print(getSafetyFactor(test))
    input = parseInput("input.txt")
    print(getSafetyFactor(input,103,101))
    part2 = parseInput("input.txt")
    print(checkTouching(part2))

if __name__ == "__main__":
    main()

