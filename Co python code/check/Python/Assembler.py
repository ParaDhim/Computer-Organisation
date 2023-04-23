def spaceerror():
    for i in statements.keys():
        for j in statements[i][0]:
            x=len(j)
            j=j.strip()
            y=len(j)
            if(x!=y):
                print("More than one spaces for separating different elements of an instruction at line "+str(statements[i][1]))
                exit(0)
def checkr():   #function to check if any variable is defined after a non var instruction is given
    i=0
    while(statements[i][0][0]=="var"):
        i=i+1
    for j in range(i,len(statements)):
        if(statements[j][0][0]=="var"):
            print("variable decleration after an instruction at line "+str(statements[j][1]))
            exit(0)

def error():
    b = None
    for i in statements.keys():
        b = error1(statements[i])
        if (b == None):
            continue
        else:
            return b
    return False


def error1(l):
    if (l[0][0] != "var" and l[0][0] not in op.keys()):
        print("Typo in instruction in line "+str(l[1]))

        return True
    elif ((l[0][0] == 'jmp' or l[0][0] == 'jlt' or l[0][0] == 'jgt' or l[0][0] == 'je') and (
            l[0][1] in v.keys() or (l[0][1] in reg.keys() and l[0][1] !="FLAGS"))):
        print("Illegal memory address "+str(l[1]))
        return True
    # to check errors in A type instructions
    elif (l[0][0] == "add" or l[0][0] == "sub" or l[0][0] == "mul" or l[0][0] == "xor" or l[0][0] == "or" or l[0][0] == "and"):
        if (len(l[0]) != 4):
            print("Wrong syntax used for instructions in line "+str(l[1]))
            return True
        if(l[0][1]=="FLAGS"):
            print("Illegal use of flags register at line "+str(l[1]))
            return True
        elif (l[0][1] not in reg.keys() or l[0][2] not in reg.keys() or l[0][3] not in reg.keys()):
            print("Typos in register name in line "+str(l[1]))
            return True
    # to check errors in both mov type instructions
    elif(l[0][0]=="mov"):
        if (len(l[0]) != 3):
            print("Wrong syntax used for instructions in line "+str(l[1]))
            return True
        if (l[0][1] == "FLAGS"):
            print("Illegal use of flags register at line "+str(l[1]))
            return True
        elif(l[0][2][0:1]=="R"):
            if(l[0][2] not in reg.keys()):
                print("Invalid register name in line "+str(l[1]))
                return True
        elif(l[0][2][0:1]=="$"):
            if (int(l[0][2][1:],10)<0 and int(l[0][2][1:],10)>255):
                print("Invalid immidiete in line "+str(l[1]))
                return True
    # to check errors in B type instructions
    elif ( l[0][0] == "rs" or l[0][0] == "ls"):
        if (len(l[0]) != 3):
            print("Wrong syntax used for instructions in line "+str(l[1]))
            return True
        if (l[0][1] == "FLAGS" or l[0][2]=="FLAGS"):
            print("Illegal use of flags register")
            return True
        elif (l[0][1] not in reg.keys()):
            print("Typos in register name "+str(l[1]))
            return True
#        elif (l[0][2] not in reg.keys() and l[0][2] not in v.keys()):
#            print("invalid register/variable name/immidiete in line "+str(l[1]))
    # to check errors in C type instructions
    elif (l[0][0] == "div" or l[0][0] == "not" or l[0][0] == "cmp"+str(l[1])):
        if (len(l[0]) != 3):
            print("Wrong syntax used for instructions in line "+str(l[1]))
            return True
        if(l[0][0]=="not" and l[0][1]=="FLAGS"):
            print("Illegal use of flags register")
            return True
        elif (l[0][2] not in reg.keys()):
            print("Typos in register name in line "+str(l[1]))
            return True
        elif (l[0][1] not in reg.keys()):
            print("Typo in register name in line "+str(l[1]))
    # to check errors in D type instructions
    elif (l[0][0] == "ld" or l[0][0] == "st"):
        if (len(l[0]) != 3):
            print("Wrong syntax used for instructions in line "+str(l[1]))
            return True
        if (l[0][1] not in reg.keys()):
            print("Typo in register name in line "+str(l[1]))
            return True
        if(l[0][0]=="ld" and l[0][1]=="FLAGS"):
            print("Illegal use of flags register")
            return True
        if l[0][2] not in v.keys():
            print("Typo in memory address in line "+str(l[1]))
            return True
    # to check errors in E type instructions
    elif (l[0][0] == "jmp" or l[0][0] == "jlt" or l[0][0] == "jgt" or l[0][0] == "je"):
        if (len(l[0]) != 2):
            print("Wrong syntax used for instructions in line "+str(l[1]))
            return True
        if l[0][1] not in labels.keys():
            print("Typo in memory address in line "+str(l[1]))
            return True
    # to check errors in F type instructions
    elif (l[0][0] == "hlt"):
        if (len(l[0]) != 1):
            print("Wrong syntax used for instructions in line "+str(l[1]))
            return True


def convert1(a):
    # convert integer to 16 bit binary
    bnr = bin(a).replace('0b', '')
    x = bnr[::-1]
    while len(x) < 16:
        x += '0'
    bnr = x[::-1]
    return bnr


def convert(a):
    # convert integer to 8 bit binary
    bnr = bin(a).replace('0b', '')
    x = bnr[::-1]
    while len(x) < 8:
        x += '0'
    bnr = x[::-1]
    return bnr


def mov1(l):
    s = "00010"
    s = s + reg[l[1]][0]
    s = s + convert(int(l[2][1:]))
    return s


def mov2(l):
    s = "0001100000"
    s = s + reg[l[1]][0]
    s = s + reg[l[2]][0]
    return s


def add(l):
    s = "0000000"
    s = s + reg[l[1]][0]
    s = s + reg[l[2]][0]
    s = s + reg[l[3]][0]
    return s


def sub(l):
    s = "0000100"
    s = s + reg[l[1]][0]
    s = s + reg[l[2]][0]
    s = s + reg[l[3]][0]
    return s


def mul(l):
    s = "0011000"
    s = s + reg[l[1]][0]
    s = s + reg[l[2]][0]
    s = s + reg[l[3]][0]
    return s


def div(l):
    s = "0011100000"
    s = s + reg[l[1]][0]
    s = s + reg[l[2]][0]
    return s


def left_shift(l):
    s = "01001"
    s = s + reg[l[1]][0]
    s = s + convert(int(l[2][1:]))
    return s




def right_shift(l):
    s = "01000"
    s = s + reg[l[1]][0]
    s = s + convert(int(l[2][1:]))
    return s


def xor_fnc(l):
    s = "0101000"
    s = s + reg[l[1]][0]
    s = s + reg[l[2]][0]
    s = s + reg[l[3]][0]
    return s


def or_fnc(l):
    s = "0101100"
    s = s + reg[l[1]][0]
    s = s + reg[l[2]][0]
    s = s + reg[l[3]][0]
    return s


def and_fnc(l):
    s = "0110000"
    s = s + reg[l[1]][0]
    s = s + reg[l[2]][0]
    s = s + reg[l[3]][0]
    return s


def not_fnc(l):
    s = "0110100000"
    s = s + reg[l[1]][0]
    s = s + reg[l[2]][0]
    return s


def load(l):
    s = "00100"
    s = s + reg[l[1]][0]
    s = s + v[l[2]][0]
    return s


def store(l):
    s = "00101"
    s = s + reg[l[1]][0]
    s = s + v[l[2]][0]
    return s


def compare(l):
    s = "0111000000"
    s = s + reg[l[1]][0]
    s = s + reg[l[2]][0]
    return s


def jump_uncond(l):
    s = "01111000"
    s = s + labels[l[1]]
    return s


def jump_if_less(l):
    s = "10000000"
    s = s + labels[l[1]]
    return s


def jump_if_greater(l):
    s = "10001000"
    s = s + labels[l[1]]
    return s


def jump_if_equal(l):
    s = "10010000"
    s = s + labels[l[1]]
    return s


def halt(l):
    return "1001100000000000"

# the raise error line was used so that we can raise error during binary creation but then we handled the error generation using aa different fucntion
def main(line):
    if (line[0][0] in op.keys()):
        if (line[0][0] == 'mov'):
            if (line[0][2] in reg.keys()):
                ret.append(mov2(line[0]))
            else:
                ret.append(mov1(line[0]))
        elif (line[0][0] == "add"):
                ret.append(add(line[0]))
        elif (line[0][0] == "sub"):
                ret.append(sub(line[0]))
        elif (line[0][0] == "mul"):
                ret.append(mul(line[0]))
        elif (line[0][0] == "div"):
                ret.append(div(line[0]))
        elif (line[0][0] == "ld"):
                ret.append(load(line[0]))
        elif (line[0][0] == "st"):
                ret.append(store(line[0]))
        elif (line[0][0] == "rs"):
                ret.append(right_shift(line[0]))
        elif (line[0][0] == "ls"):
                ret.append(left_shift(line[0]))
        elif (line[0][0] == "or"):
                ret.append(or_fnc(line[0]))
        elif (line[0][0] == "xor"):
                ret.append(xor_fnc(line[0]))
        elif (line[0][0] == "and"):
                ret.append(and_fnc(line[0]))
        elif (line[0][0] == "not"):
                ret.append(not_fnc(line[0]))
        elif (line[0][0] == "cmp"):
                ret.append(compare(line[0]))
        elif (line[0][0] == "jmp"):
                ret.append(jump_uncond(line[0]))
        elif (line[0][0] == "jlt"):
                ret.append(jump_if_less(line[0]))
        elif (line[0][0] == "jgt"):
                ret.append(jump_if_greater(line[0]))
        elif (line[0][0] == "je"):
                ret.append(jump_if_equal(line[0]))
        elif (line[0][0] == "hlt"):
            ret.append(halt(line[0]))
    else:
        # raise error
        pass

#ret list is for storing the final binary output
ret = []

#statements dictionary is storing our input keys are line numbers (starting from 0 and are in base 10)
# values are a 2d list storing
#[ [<instuction in list format after splitting thee string >],line number of this instruction]
statements = {}

#op dictionary contains all our instructions as keys and values as their op codes
op = {"add": '00000',
      "sub": '00000',
      "mov": '0001100000',
      "ld": '00000',
      "st": '00000',
      "mul": '00000',
      "div": '00000',
      "rs": '00000',
      "ls": '00000',
      "xor": '00000',
      "or": '00000',
      "and": '00000',
      "not": '00000',
      "cmp": '00000',
      "jmp": '00000',
      "jlt": '00000',
      "jgt": '00000',
      "je": '00000',
      "hlt": '00000'}

#v dictionary to store keys as variable names and values as memory addresses
v = {}

#reg dictionary stores the register name as key and value is
#a list containing binary representation of register and the value contained in it'''
reg = {'R0': ['000', 0],
       'R1': ['001', 0],
       'R2': ['010', 0],
       'R3': ['011', 0],
       'R4': ['100', 0],
       'R5': ['101', 0],
       'R6': ['110', 0],
       'FLAGS': ['111', 0]}

#var is counting number of lines in our input
var = 0

#labels dictionary is for storing labels as keys and values are addresses
labels = {}
#to check if reserved words are used in variable and label name
reserved=["add","sub","mul","div","jmp","jgt","jlt","je","cpm","ld","st","not","xor","or","and","ls","rs","mov","hlt","R0","R1","R2","R3","R4","R5","R6","FLAGS","var",]
# to check if anything other than alphanumeric and _ is used in variable and label names
vname="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_"

# loop to take input from user(will end when the inout is completed
while (1):
    try:
        line = input()
        line=line.strip()
        if (line != ""):
            if (line.split()[0] != "hlt" and (len(line.split()) == 1)):
                print("Invalid Instruction at line "+str(var+1))
                exit(0)
            statements[var] = [line.split(), var]
            var += 1
    except EOFError:
        break

# storing variable addresses and removing labels after storing the label addresss in labels dictionary
for i in statements.keys():
    if (statements[i][0][0] == 'var'):
        if (len(statements[i][0]) == 1):
            print("Invalid Instruction at line "+str(statements[i][1]))
            exit(0)
        if(statements[i][0][1] in reserved):
            print("Reserved words cannot be used as variable names line no =>"+str(statements[i][1]))
            exit(0)
        for k in statements[i][0][1]:
            if(k not in vname):
                print("invalid literal in variable names at line "+str(statements[i][1]))
                exit(0)
        v[statements[i][0][1]] = 0
    elif (statements[i][0][0][-1:] == ':'):
        if (statements[i][0][0][:-1] in labels):
            print("Two labels with same name -> Invalid Instruction at line "+str(statements[i][1]))
            exit(0)
        if(statements[i][0][0][:-1] in reserved):
            print("Reserved words cannot be used as label names line number =>"+str(statements[i][1]))
            exit(0)
        for k in statements[i][0][0][:-1]:
            if(k not in vname):
                print("invalid literal in label names at line "+str(statements[i][1]))
                exit(0)
        # binary conversion
        labels[statements[i][0][0][:-1]] = convert(int(i) - len(v))
        del statements[i][0][0]

#assinging addresses to variables
k = 0
for i in v.keys():
    # binary
    v[i] = [convert(len(statements) - len(v) + k), ""]
    k += 1
# checking for more than one halt statement


spaceerror() # functio to check if multiple spaces are entered
checkr()    # to check if variables are decleared after an instruction of some opcode is given
for i in statements.keys():
    if (statements[i][0][0] == "hlt" and statements[i][1] != len(statements) - 1):
        print("More than one hlt statement at line "+str(statements[i][1])+"\n")
        exit(0)
        
if(len(statements)<256 and statements[len(statements)-1][0][0]!="hlt"):
    print("Missing halt statement")
    exit(0)
if (error()): #if any arror then we exit and do not print anything anymore
    exit()
# if no error found binary file creation starts and then printing it
else:
    sk = 0
    while (len(v) + sk in statements.keys()):
        main(statements[len(v) + sk])
        sk += 1
# Printing the binary file
    for i in range(len(ret)):
        print(ret[i])