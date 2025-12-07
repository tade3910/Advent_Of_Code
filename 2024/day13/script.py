#!/usr/bin/python3
import re

def extract_variables(filename):
    # Regular expression patterns for each variable
    pattern = {
        'aX': r"Button A: X\+(\d+),",  # Matches "X+<number>" in Button A line
        'aY': r"Button A: .*, Y\+(\d+)",  # Matches "Y+<number>" in Button A line
        'bX': r"Button B: X\+(\d+),",  # Matches "X+<number>" in Button B line
        'bY': r"Button B: .*, Y\+(\d+)",  # Matches "Y+<number>" in Button B line
        'X': r"Prize: X=(\d+),",  # Matches "X=<number>" in Prize line
        'Y': r"Prize: .*, Y=(\d+)"   # Matches "Y=<number>" in Prize line
    }

    all_variables = []  # List to store all sets of variables

    with open(filename, 'r') as file:
        text = file.read()

        # Split the text into blocks based on the blank lines
        blocks = text.strip().split('\n\n')

        for block in blocks:
            variables = {}
            for var, pat in pattern.items():
                match = re.search(pat, block)
                if match:
                    variables[var] = int(match.group(1))
                else:
                    variables[var] = None  # In case a variable is not found

            all_variables.append(variables)

    return all_variables


def minimize(aX, bX, X, aY, bY, Y):
    minCost = None
    for i in range(101):
        curBX = bX * i
        topX = X - curBX
        curBY = bY * i
        topY = Y - curBY
        
        if topX % aX == 0 and topY % aY == 0:
            xA = topX // aX
            yA = topY // aY
            if 0 <= xA <= 100 and 0 <= yA <= 100:
                cost = xA * 3 + i
                if minCost is None or cost < minCost:
                    minCost = cost
                # return cost  
    return minCost

def determinant(a, b, X, c, d, Y,max=True):
    determinant = (a * d) - (b * c)
    if determinant != 0:
        xD = (X * d) - (b * Y)
        if xD % determinant != 0:
            return 0
        xD /= determinant
        yD = (a * Y) - (c * X)
        if yD %determinant != 0:
            return 0
        yD /= determinant
        if max:
            if 0 <= xD <= 100 and 0 <= yD <= 100:
                return (xD * 3) + yD
        else:
                return (xD * 3) + yD

    return 0


def main():
    filename = 'input.txt'  
    variables_list = extract_variables(filename)
    cost = 0
    for variables in variables_list:
        curCost = determinant(variables['aX'],variables['bX'],variables['X'],variables['aY'],variables['bY'],variables['Y'])
        cost += curCost
    print(cost)
    cost = 0
    for variables in variables_list:
        X = variables['X']
        X += 10000000000000
        Y = variables['Y']
        Y+= 10000000000000
        curCost = determinant(variables['aX'],variables['bX'],X,variables['aY'],variables['bY'],Y,False)
        cost += curCost
    print(cost)


if __name__ == "__main__":
    main()
