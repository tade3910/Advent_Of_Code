class Debugger:
    def __init__(self,A:int,B:int,C:int,program:list[int]):
        self.A = A
        self.B = B
        self.C = C
        self.program = program
        self.instructorPointer = 0
        self.output:list[int] = []
    
    def getComboOperand(self):
        value = self.program[self.instructorPointer]
        if 0 <= value <= 3:
            self.instructorPointer += 1
            return value
        elif value == 4: 
            self.instructorPointer += 1
            return self.A
        elif value == 5: 
            self.instructorPointer += 1
            return self.B
        elif value == 6:
            self.instructorPointer += 1
            return self.C
        raise Exception("Invalid argument")
    
    def getLiteral(self):
        value = self.program[self.instructorPointer]
        if value < -1 or value > 7: raise Exception("Invalid argument")
        self.instructorPointer += 1
        return value

    def intDivide(self):
        numerator = self.A
        denominator = self.getComboOperand()
        denominator  = 2 ** denominator
        result = numerator // denominator
        return result

    def adv(self):
        val = self.intDivide()
        self.A = val
    
    def bxl(self):
        currentB = self.B
        literal = self.getLiteral()
        result = currentB ^ literal
        self.B = result
    
    def bst(self):
        combo = self.getComboOperand()
        result = combo % 8
        self.B = result
    
    def jnz(self):
        jump = self.A
        nextIndex = self.getLiteral()
        if jump != 0:
            self.instructorPointer = nextIndex
    
    def bxc(self):
        result = self.B ^ self.C
        self.getLiteral() # increments pointer for legacy reasons
        self.B = result
    
    def out(self):
        combo = self.getComboOperand()
        result = combo % 8
        self.output.append(result)
    
    def bdv(self):
        self.B = self.intDivide()
    
    def cdv(self):
        self.C = self.intDivide()
    
    def doInstruction(self):
        instruction = self.getLiteral()
        if instruction == 0:
            self.adv()
        elif instruction == 1:
            self.bxl()
        elif instruction == 2:
            self.bst()
        elif instruction == 3:
            self.jnz()
        elif instruction == 4:
            self.bxc()
        elif instruction == 5:
            self.out()
        elif instruction == 6:
            self.bdv()
        elif instruction == 7:
            self.cdv()
    
    def printout(self):
        print(",".join(map(str, self.output)))
    
    def halt(self):
        if self.instructorPointer >= len(self.program):
            # self.printout()
            return True
        return False

def programStringToList(programStr:str):
    program = programStr.split(",")
    for i in range(len(program)):
        program[i] = int(program[i])
    return program

def runDebugger(a:int,b:int,c:int,programStr:str):
    program = programStringToList(programStr)
    debugger = Debugger(a,b,c,program)
    while (not debugger.halt()):
        debugger.doInstruction()
    return debugger.output



def reverseDebugger(input:str): # The debugger works on the last 3 bits then goes to the second to last 3 bits and so on
    program = programStringToList(input)
    programLength = len(program)
    valid = [0]
    for length in range(1,programLength+1): # we want to iterate from -1 -> - length
        oldvalid = valid
        valid = []
        for num in oldvalid:
            for offset in range(8): # Only working with numbers from 0 - 7
                next = 8*num+offset # Last number A was set to was num, shift up 3 bits to look at lower bits
                output = runDebugger(next,0,0,input)
                second = program[-length:] # compare with length amount of elements
                if output == second:
                    valid.append(next)
                    
    answer = min(valid)
    print(answer)

def tests():
    runDebugger(0,0,9,"2,6")
    runDebugger(10,0,0,"5,0,5,1,5,4")
    runDebugger(2024,0,0,"0,1,5,4,3,0")
    runDebugger(0,29,0,"1,7")
    runDebugger(0,2024,43690,"4,0")
    runDebugger(729,0,0,"0,1,5,4,3,0")
    reverseDebugger("0,3,5,4,3,0")

def main():
    # tests()
    print(runDebugger(65804993,0,0,"2,4,1,1,7,5,1,4,0,3,4,5,5,5,3,0"))
    reverseDebugger("2,4,1,1,7,5,1,4,0,3,4,5,5,5,3,0")

if __name__ == "__main__":
    main()

    
    
