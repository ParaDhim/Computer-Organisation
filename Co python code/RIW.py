import sys
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
def load(l,registers,opcodes,variables):
    op=opcodes[l[0]]
    reg1=registers[l[1]][0]
    mem_addr=variables[l[2]]
    return op+reg1+mem_addr
def store(l,registers,opcodes,variables):
    op=opcodes[l[0]]
    reg1=registers[l[1]][0]
    mem_addr=variables[l[2]]
    return op+reg1+mem_addr
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
def Lessjump(l,registers,opcodes,labels):
    op=opcodes[l[0]]
    mem_addr=labels[l[1]]
    return op+"000"+mem_addr
def greaterjump(l,registers,opcodes,labels):
    op=opcodes[l[0]]
    mem_addr=labels[l[1]]
    return op+"000"+mem_addr
def Equaljump(l,registers,opcodes,labels):
    op=opcodes[l[0]]
    mem_addr=labels[l[1]]
    return op+"000"+mem_addr
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
def UndefVar(l,registers,opcodes,variables):
        for i in l:
            if i[0] in labels.keys():
                if i[1] == "ld" or i[1] == "st":
                    if i[-1] not in variables.keys():
                        sys.exit("Error! Use of Undefined Variables")
            elif i[0] == "ld" or i[0] == "st":
                if i[-1] not in variables.keys():
                    sys.exit("Error! Use of Undefined Variables")

def UndefLabel(l,registers,opcodes,labels):
    for i in l:
        if i[0] in labels.keys():
            if i[1] == "jmp" or i[1] == "jlt" or i[1] == "jgt" or i[1] == "je":
                if i[-1] not in labels.keys():
                    sys.exit("Error! Use of Undefined Labels")
        elif i[0] == "jmp" or i[0] == "jlt" or i[0] == "jgt" or i[0] == "je":
                if i[-1] not in labels.keys():
                    sys.exit("Error! Use of Undefined Labels")
def MissHaltCondn(l,opcodes,registers):
    count = 0
    for i in l:
        if i[0] in labels.keys():
            if i[1] == "hlt":
                count+= 1
        elif i[0] == "hlt":
                count+= 1
    if count == 0:
        sys.exit("Error! Missing hlt condition") 

def LastHalt(l,opcodes,registers):
    if l[-1][0] in labels.keys():
        if l[-1][1] != "hlt":
            sys.exit("Error! hlt condition not used at last") 
    elif l[-1][0] != "hlt":
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
        if i[0] in labels.keys():
                if i[1] == "var":
                    continue
                if i[1] not in opcodes.keys():
                    sys.exit("Error! Please check for Typo in instruction name")
                elif (i[1] == "add") or (i[1] == "sub") or (i[1] == "mul") or (i[1] == "xor") or (i[1] == "or") or (i[1] == "and"):
                    if ((i[1] not in registers.keys()) and (i[2] not in registers.keys()) and (i[2] not in registers.keys()) and (i[2] not in registers.keys())):

                        sys.exit("Error! Please check for Typo in registers name1")
                elif (i[1] == "mov" and i[2][0] == "$"):
                    if (i[1] not in registers.keys()):
                        sys.exit("Error! Please check for Typo in registers name2")
                elif (i[1] == "mov" and i[2][0] != "$"):
                    if (i[2] not in registers.keys()) and (i[3] not in registers.keys()):
                        sys.exit("Error! Please check for Typo in registers name3")
                elif (i[1] == "div") or (i[1] == "not") or (i[1] == "cmp"):
                    if ((i[2] not in registers.keys()) and (i[3] not in registers.keys()) and (i[4] not in registers.keys())):
                        sys.exit("Error! Please check for Typo in registers name4")
                elif (i[1] == "rs") or (i[1] == "ls") or (i[1] == "rs"):
                    if (i[2] not in registers.keys()):
                        sys.exit("Error! Please check for Typo in registers name5")
        else:
            # for i in l:
                if i[0] == "var":
                    continue
                if i[0] not in opcodes.keys():
                    sys.exit("Error! Please check for Typo in instruction name")
                elif (i[0] == "add") or (i[0] == "sub") or (i[0] == "mul") or (i[0] == "xor") or (i[0] == "or") or (i[0] == "and"):
                    if ((i[1] not in registers.keys()) and (i[2] not in registers.keys()) and (i[2] not in registers.keys()) and (i[2] not in registers.keys())):

                        sys.exit("Error! Please check for Typo in registers name1")
                elif (i[0] == "mov" and i[1][0] == "$"):
                    if (i[1] not in registers.keys()):
                        sys.exit("Error! Please check for Typo in registers name2")
                elif (i[0] == "mov" and i[1][0] != "$"):
                    if (i[1] not in registers.keys()) and (i[2] not in registers.keys()):
                        sys.exit("Error! Please check for Typo in registers name3")
                elif (i[0] == "div") or (i[0] == "not") or (i[0] == "cmp"):
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
        UndefVar(l,registers,opcodes,variables)
        UndefLabel(l,registers,opcodes,labels)
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
    if l[0].upper()=="HLT":
        print(Halt(l,registers,opcodes))
        break
    elif l[0].upper()=="MOV" or l[1].upper()=="MOV":
        if l[1].upper()=="MOV":
            print(mov(l[1:],registers,opcodes))
        else:
            print(mov(l,registers,opcodes))
    elif l[0].upper()=="ADD" or l[1].upper()=="ADD":
        if l[1].upper()=="ADD":
            print(add(l[1:],registers,opcodes))
        else:
            print(add(l,registers,opcodes))
    elif l[0].upper()=="SUB" or l[1].upper()=="SUB":
        if l[1].upper()=="SUB":
            print(sub(l[1:],registers,opcodes))
        else:
            print(sub(l,registers,opcodes))

    elif l[0].upper()=="MUL" or l[1].upper()=="MUL":
        if l[1].upper()=="MUL":
            print(mul(l[1:],registers,opcodes))
        else:
            print(mul(l,registers,opcodes))

    elif l[0].upper()=="DIV" or l[1].upper()=="DIV":
        if l[1].upper()=="DIV":
            print(divide(l[1:],registers,opcodes))
        else:
            print(divide(l,registers,opcodes))

    elif l[0].upper()=="LD" or l[1].upper()=="LD":
        if l[1].upper()=="LD":
            print(load(l[1:],registers,opcodes,variables))
        else:
            print(load(l,registers,opcodes,variables))

    elif l[0].upper()=="ST"or l[1].upper()=="ST":
        if l[1].upper()=="ST":
            print(store(l[1:],registers,opcodes,variables))
        else:
            print(store(l,registers,opcodes,variables))

    elif l[0].upper()=="RS" or l[1].upper()=="RS":
        if l[1].upper()=="RS":
            print(rs(l[1:],registers,opcodes))
        else:
            print(rs(l,registers,opcodes))


    elif l[0].upper()=="LS" or l[1].upper()=="LS":
        if l[1].upper()=="LS":
            print(ls(l[1:],registers,opcodes))
        else:
            print(ls(l,registers,opcodes))

    elif l[0].upper()=="XOR" or l[1].upper()=="XOR":
        if l[1].upper()=="XOR":
            print(xor(l[1:],registers,opcodes))
        else:
            print(xor(l,registers,opcodes))


    elif l[0].upper()=="OR" or l[1].upper()=="OR":
        if l[1].upper()=="OR":
            print(OR(l[1:],registers,opcodes))
        else:
            print(OR(l,registers,opcodes))

    elif l[0].upper()=="AND" or l[1].upper()=="AND":
        if l[1].upper()=="AND":
            print(AND(l[1:],registers,opcodes))
        else:
            print(AND(l,registers,opcodes))


    elif l[0].upper()=="NOT" or l[1].upper()=="NOT":
        if l[1].upper()=="NOT":
            print(NOT(l[1:],registers,opcodes))
        else:
            print(NOT(l,registers,opcodes))

    elif l[0].upper()=="JMP" or l[1].upper()=="JMP":
        if l[1].upper()=="JMP":
            print(Ujump(l[1:],registers,opcodes,labels))
        else:
            print(Ujump(l,registers,opcodes,labels))

    elif l[0].upper()=="JLT" or l[1].upper()=="JLT":
        if l[1].upper()=="JLT":
            print(Lessjump(l[1:],registers,opcodes,labels))
        else:
            print(Lessjump(l,registers,opcodes,labels))


    elif l[0].upper()=="JGT" or l[1].upper()=="SUB":
        if l[1].upper()=="JGT":
            print(greaterjump(l[1:],registers,opcodes,labels))
        else:
            print(greaterjump(l,registers,opcodes,labels))

    elif l[0].upper()=="JE" or l[1].upper()=="JE":
        if l[1].upper()=="JE":
            print(Equaljump(l[1:],registers,opcodes,labels))
        else:
            print(Equaljump(l,registers,opcodes,labels))