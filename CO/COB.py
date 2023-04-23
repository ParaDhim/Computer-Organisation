import sys
from tabnanny import check
def convert(a):
    b=[]
    k=""
    while a!=0:
        c = a%2
        d = a//2
        b.insert(0,c)
        a = d
    for i in range (0,len(b)):
        k=k+str(b[i])
    while (len(k) < 8) :
        k = "0" + k
    return (k) 

def mov(l,registers,opcodes):
    if("$" in l[2]):
       op=opcodes[l[0]][0:5]
       reg1=registers[l[1]][0]
       imm_bin=convert(int(l[2][1:]))
       registers[l[1]][1]=int(l[2][1:])
       return op+reg1+imm_bin
    else:
       op=opcodes[l[0]][5:10]
       reg1=registers[l[1]][0]
       reg2=registers[l[2]][0]
       registers[l[1]][1]=registers[l[2]][1]
       return op+"00000"+reg1+reg2

    # To set Flags in case of add sub mul div
    # Load store functions are left
    # Can be done after VARiables only
def add(l,registers,opcodes):
    op=opcodes[l[0]]
    reg1=registers[l[1]][0]
    reg2=registers[l[2]][0]
    reg3=registers[l[3]][0]
    registers[l[3]][1]=registers[l[2]][1]+registers[l[1]][1]
    return op+"00"+reg1+reg2+reg3

def sub(l,registers,opcodes):
    op=opcodes[l[0]]
    reg1=registers[l[1]][0]
    reg2=registers[l[2]][0]
    reg3=registers[l[3]][0]
    registers[l[3]][1]=registers[l[1]][1]-registers[l[2]][1]
    return op+"00"+reg1+reg2+reg3

def mul(l,registers,opcodes):
    op=opcodes[l[0]]
    reg1=registers[l[1]][0]
    reg2=registers[l[2]][0]
    reg3=registers[l[3]][0]
    registers[l[3]][1]=registers[l[1]][1]*registers[l[2]][1]
    return op+"00"+reg1+reg2+reg3

def divide(l,registers,opcodes):
    op=opcodes[l[0]]
    reg1=registers[l[1]][0]
    reg2=registers[l[2]][0]
    registers["R0"][1]=registers[l[1]][1]/registers[l[2]][1]
    registers["R1"][1]=registers[l[1]][1]%registers[l[2]][1]
    return op+"00000"+reg1+reg2

# Done by multiplying by 2**n
def rs(l,registers,opcodes):
    op=opcodes[l[0]]
    reg1=registers[l[1]][0]
    imm=int(l[2][1:])
    registers[l[1]][1]=2*(imm)
    imm_bin=convert(imm)
    return op+reg1+imm_bin

# Done by dividing by 2**n
def ls(l,registers,opcodes):
    op=opcodes[l[0]]
    reg1=registers[l[1]][0]
    imm=int(l[2][1:])
    registers[l[1]][1]/=2**(imm)
    imm_bin=convert(imm)
    return op+reg1+imm_bin

def xor(l,registers,opcodes):
    op=opcodes[l[0]]
    reg1=registers[l[1]][0]
    reg2=registers[l[2]][0]
    reg3=registers[l[3]][0]
    registers[l[3]][1]=registers[l[2]][1]^registers[l[1]][1]
    return op+"00"+reg1+reg2+reg3

def OR(l,registers,opcodes):
    op=opcodes[l[0]]
    reg1=registers[l[1]][0]
    reg2=registers[l[2]][0]
    reg3=registers[l[3]][0]
    registers[l[3]][1]=registers[l[2]][1]|registers[l[1]][1]
    return op+"00"+reg1+reg2+reg3

def AND(l,registers,opcodes):
    op=opcodes[l[0]]
    reg1=registers[l[1]][0]
    reg2=registers[l[2]][0]
    reg3=registers[l[3]][0]
    registers[l[3]][1]=registers[l[2]][1]&registers[l[1]][1]
    return op+"00"+reg1+reg2+reg3

def NOT(l,registers,opcodes):
    op=opcodes[l[0]]
    reg1=registers[l[1]][0]
    reg2=registers[l[2]][0]
    registers[l[2]][1]=~registers[l[1]][1]
    return op+"00000"+reg1+reg2

def Ujump(l,registers,opcodes):
    # jmp mem_addr
    op=opcodes[l[0]]
    mem_add=labels[l[1]]
    return op+"000"+mem_add
def Halt(l,registers,opcodes):
    op=opcodes[l[0]]
    return op+("0"*11)
# def set_flags(tv,tl,tg,te):
    
def lines(file):
    f=open(file,"r")
    t=f.readlines()
    n_lines=0
    for i in t:
        l=i.split()
        if l[0].upper()!="VAR":
            n_lines+=1
    return n_lines

        
# MAIN PROGRAM

file = "paras.txt"
f = open(file,"r")
t = f.readlines()

# l is the list with individual words of lines as string elements
l =[]
f = open(file,"r")
t = f.readlines()
for i in (t):
    ele = i.split()
    l.append(ele)
# print(l)

# opcodes of the instructions
opcodes = {
      "add": '10000',
      "sub": '10001',
      "mov": '1001010011',
      "ld": '10100',
      "st": '10101',
      "mul": '10110',
      "div": '10111',
      "rs": '11000',
      "ls": '11001',
      "xor": '11010',
      "or": '11011',
      "and": '11100',
      "not": '11101',
      "cmp": '11110',
      "jmp": '11111',
      "jlt": '01100',
      "jgt": '01101',
      "je" : '01111',
      "hlt": '01010'}
# stores the registers and thier values 
registers = {
       'R0': ['000', 0],
       'R1': ['001', 0],
       'R2': ['010', 0],
       'R3': ['011', 0],
       'R4': ['100', 0],
       'R5': ['101', 0],
       'R6': ['110', 0],
       'FLAGS': ['111', 0]}

# variables dictionary : stores addresses as values
variables={}

# labels dictionary : stores labels as keys and values as their addresses
labels={}


k=0
# t is a list of lines in the text file
for i in range(len(t)):
    l=t[i].split()
    # l is a list conatining each word of a line as string element
    # for j in range(len(l)):
    if l[0].upper()=="VAR":
        variables[l[1]]=convert(lines(file)+k)
        k+=1
    elif l[0] not in opcodes.keys():
        labels[l[0]]=convert(i)   

# print(variables)
# print(labels)

    #   ERROR HANDLING

# to show the different error value for the differrent variables
# def showError():
# Checking the errors
# need to check the spacing also
# general also needed to form
# def genralErrorCheck():
# if the instruct given is correct or not
# here the spacing errors are needed to be check

def MissHaltCondn(l,opcodes,registers):
    count = 0
    for i in l:
        if i[0] == "hlt":
            count = 1
    if count == 0:
        sys.exit("Error! Missing hlt condition") 

def LastHalt(l,opcodes,registers):
    if l[-1][0] != "hlt":
        sys.exit("Error! hlt condition not used at last") 
def checkVarBegin(l,opcodes,registers):
    count = 0
    for i in range (1,len(l)+1):
        if l[0][0] == "var":
            count += 1
            if (count != i):
               sys.exit("Error! Please check if all the variables are declared at the beginning") 
def TypoIns(l,opcodes,registers):
    for i in l:
        if i[0] == "var":
            continue
        if i[0] not in opcodes.keys():
            
            sys.exit("Error! Please check for Typo in instruction name")

        elif (i[0] == "add") or (i == "sub") or (i == "mul") or (i == "xor") or (i == "or") or (i == "and"):
            if ((i[1] not in registers.keys()) and (i[2] not in registers.keys()) and (i[2] not in registers.keys()) and (i[2] not in registers.keys())):

                sys.exit("Error! Please check for Typo in registers name1")
        elif (i[0] == "mov" and i[1][0] == "$"):
            if (i[1] not in registers.keys()):
                sys.exit("Error! Please check for Typo in registers name2")
        elif (i[0] == "mov" and i[1][0] != "$"):
            if (i[1] not in registers.keys()) and (i[2] not in registers.keys()):
                sys.exit("Error! Please check for Typo in registers name3")
        elif (i[0] == "div") or (i == "not") or (i == "cmp"):
            if ((i[1] not in registers.keys()) and (i[2] not in registers.keys()) and (i[2] not in registers.keys())):
                sys.exit("Error! Please check for Typo in registers name4")
        elif (i[0] == "rs") or (i[0] == "ls") or (i[0] == "rs"):
            if (i[1] not in registers.keys()):
                sys.exit("Error! Please check for Typo in registers name5")

def CheckErrors(l,opcodes,registers):
        TypoIns(l,opcodes,registers)
        checkVarBegin(l,opcodes,registers)
        MissHaltCondn(l,opcodes,registers)
        LastHalt(l,opcodes,registers)
def ListCreation(file):
    l =[]
    f = open(file,"r")
    t = f.readlines()
    for i in (t):
        ele = i.split()
        l.append(ele)
    return(l)
file = "paras.txt"
a = ListCreation(file)
# print(a)
CheckErrors(a,opcodes,registers)

# PRINTING THE BINARY CODE 

for i in range(len(t)):
    l=t[i].split()
    if l[0].upper()=="MOV":
        print(mov(l,registers,opcodes))
    elif l[0].upper()=="ADD":
        print(add(l,registers,opcodes))
    elif l[0].upper()=="SUB":
        print(sub(l,registers,opcodes))
    elif l[0].upper()=="MUL":
        print(mul(l,registers,opcodes))
    elif l[0].upper()=="DIV":
        print(divide(l,registers,opcodes))
    elif l[0].upper()=="RS":
        print(rs(l,registers,opcodes))
    elif l[0].upper()=="LS":
        print(ls(l,registers,opcodes))
    elif l[0].upper()=="XOR":
        print(xor(l,registers,opcodes))
    elif l[0].upper()=="OR":
        print(OR(l,registers,opcodes))
    elif l[0].upper()=="AND":
        print(AND(l,registers,opcodes))
    elif l[0].upper()=="NOT":
        print(NOT(l,registers,opcodes))
    elif l[0].upper()=="HLT":
        print(Halt(l,registers,opcodes))
        break