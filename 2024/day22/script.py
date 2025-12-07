def parseInput(fileName:str):
    secretNumbers = []
    with open(fileName, 'r') as file:
        for line in file:
            secretNumbers.append(int(line.strip()))
    return secretNumbers

def mix(value:int,secretNumber:int):
    return value ^ secretNumber

def prune(secretNumber:int):
    return secretNumber % 16777216

def stepOne(secretNumber:int):
    result = secretNumber * 64
    result = mix(result,secretNumber)
    return prune(result)

def stepTwo(secretNumber:int):
    result = secretNumber // 32
    result = mix(result,secretNumber)
    return prune(result)

def stepThree(secretNumber:int):
    result = secretNumber * 2048
    result = mix(result,secretNumber)
    return prune(result)

def generateNextSecret(secretNumber:int):
    secretNumber = stepOne(secretNumber)
    secretNumber = stepTwo(secretNumber)
    secretNumber = stepThree(secretNumber)
    return secretNumber

def generateXSecretNumbers(secretNumber:int,x:int):
    for _ in range(x):
        secretNumber = generateNextSecret(secretNumber)
    return secretNumber

def simulateBuys(secretNumber:int,x:int,sums:dict[tuple[int,int,int,int],int]):
    inital = [0,0,0,0]
    i = 0
    while i < 4:
        prevVal = secretNumber % 10
        secretNumber = generateNextSecret(secretNumber)
        curVal = secretNumber % 10
        change = curVal - prevVal
        inital[i] = change
        i += 1
    sequence = inital[0], inital[1], inital[2], inital[3]
    assigned = set([sequence])
    sums[sequence] = sums.get(sequence,0) + curVal
    for i in range(x):
        prevVal = secretNumber % 10
        secretNumber = generateNextSecret(secretNumber)
        curVal = secretNumber % 10
        change = curVal - prevVal
        sequence = sequence[1], sequence[2], sequence[3], change
        if sequence not in assigned:
            assigned.add(sequence)
            sums[sequence] = sums.get(sequence,0) + curVal

def partTwo(fileName:int,x:int):
    secretNumbers = parseInput(fileName)
    sums = {}
    for secretNumber in secretNumbers:
        simulateBuys(secretNumber,x,sums)
    max = 0
    for val in sums.values():
        if val > max:
            max = val
    print(max)


def partOne(fileName:int,x:int):
    secretNumbers = parseInput(fileName)
    sum = 0
    for secretNumber in secretNumbers:
        sum += generateXSecretNumbers(secretNumber,x)
    print(f"sum is {sum}")

partOne("test.txt",2000)
partOne("input.txt",2000)
partTwo("test3.txt",2000)
partTwo("input.txt",2000)