import sys

reg = {'000': "0000000000000000",
       '001': "0000000000000000",
       '010': "0000000000000000",
       '011': "0000000000000000",
       '100': "0000000000000000",
       '101': "0000000000000000",
       '110': "0000000000000000",
       '111': "0000000000000000"}
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

def convertTo16(a):
    b=[]
    k=""
    while a!=0:
        c = a%2
        d = a//2
        b.insert(0,c)
        a = d
    for i in range (0,len(b)):
        k=k+str(b[i])
    while (len(k) < 16) :
        k = "0" + k
    return (k)

def ls(line,pc):
    # making flags == 0 beforehand
    reg['111']="0000000000000000"
    
    #       01234    567       8910111213
    # line = 11001   000       100010
    #        opcode  register  Immediate
    # opcode = 0:5
    # register= 5:8
    # immediate=8:14
    reg_val=int(reg[line[5:8]],2)
    imm=int(line[8:],2)
    reg_val/=2**imm
    b=convert(reg_val)
    if (len(b) > 16):
        reg['111'] = (bin(int(reg['111'], 2) + 8))[2:]
    else:
        reg[line[5:8]] = b
    return convert(int(pc,2)+1)

def rs(line,pc):
    # making flags == 0 beforehand
    reg['111']="0000000000000000"

    reg_val=int(reg[line[5:8]],2)
    imm=int(line[8:],2)
    reg_val/=2**imm
    b=convert(reg_val)
    reg[line[5:8]] = b

    return convert(int(pc,2)+1)
def addition(line,pc):
    # add reg1 reg2 reg3
    # 10000 00 000 001 010
    # 01234 56 789 101112 131415
    # opcode =line[0:5]
    # reg1=line[7:10]
    # reg2=line[10:13]
    # reg3=line[13:]
    # to do reg3=reg1+reg2
    reg["111"] = "0000000000000000"
    reg1_val=int(reg[line[7:10]],2)
    reg2_val=int(reg[line[10:13]],2)
    reg3_val=int(reg[line[13:]],2)
    reg3_val=reg1_val+reg2_val
    b=bin(reg3_val)
    if (len(b) > 18):
        reg[line[7:10]] = b[-16:]
        reg['111'] = convertTo16(int(reg['111'], 2) + 8)
    else:
        reg[line[7:10]] = convertTo16(reg3_val)
    return convert(int(pc, 2) + 1)
    
def substraction(line,pc):
    # sub reg1 reg2 reg3
    # 10001 00 000 001 010
    # 01234 56 789 101112 131415
    # opcode =line[0:5]
    # reg1=line[7:10]
    # reg2=line[10:13]
    # reg3=line[13:]
    # to do reg3=reg1-reg2
    reg["111"] = "0000000000000000"
    reg1_val=int(reg[line[7:10]],2)
    reg2_val=int(reg[line[10:13]],2)
    reg3_val=int(reg[line[13:]],2)
    reg3_val=reg1_val-reg2_val
    if (reg3_val < 0):
        reg[line[7:10]] ="0000000000000000"
        reg['111'] = convertTo16(int(reg['111'], 2) + 8)
    else:
        reg[line[7:10]] = convertTo16(reg3_val)
    return convert(int(pc, 2) + 1)

def load(line,pc,Memory):
    # ld reg1 mem_addr
    reg["111"] = "0000000000000000"
    reg[line[5:8]] = Memory[line[8:]]
    # reg[line[5:8]] = MEM[line[8:]]
    return convert(int(pc,2)+1)

def store(line,pc,Memory):
    # st reg1 mem_addr
    reg["111"] = "0000000000000000"
    Memory[line[8:]] = reg[line[5:8]]
    # MEM[line[8:]] = reg[line[5:8]]
    return convert(int(pc,2)+1)

def mov_imm(line,pc):
    # mov reg1 $Imm
    # 10010 000 00000000
    # opcode =line[0:5]
    # reg1=line[5:8]
    # imm = line[8:]
    reg["111"] = "0000000000000000"
    # picking up the immediate value
    reg[line[5:8]]=convertTo16(int(line[8:], 2))
    return convert(int(pc,2)+1)

def mov_register(line,pc):
    # mov reg1 reg2
    # 10011 00 000 001 010
    # opcode =line[0:5]
    # 5 unused bits would be there
    # reg1=line[10:13]
    # reg2 = line[13:16]
    reg[line[10:13]]=convertTo16(int(reg[line[13:]],2))
    reg["111"] = "0000000000000000"

    return convert(int(pc,2)+1)

def multiply(line,pc):
    # mul reg1 reg2 reg3
    # 10110 00 000 001 010
    # 01234 56 789 101112 131415
    # opcode =line[0:5]
    # reg1=line[7:10]
    # reg2=line[10:13]
    # reg3=line[13:]
    # to do reg3=reg1*reg2
    reg["111"] = "0000000000000000"
    reg1_val=int(reg[line[7:10]],2)
    reg2_val=int(reg[line[10:13]],2)
    reg3_val=int(reg[line[13:]],2)
    reg3_val=reg1_val*reg2_val
    b=bin(reg3_val)
    if (len(b) > 18):
        reg[line[7:10]] = b[-16:]
        reg['111'] = convertTo16(int(reg['111'], 2) + 8)
    else:
        reg[line[7:10]] = convertTo16(reg3_val)
    return convert(int(pc, 2) + 1)


def xor(line,pc):
    # xor reg1 reg2 reg3
    # 11010 00 000 001 010
    # 01234 56 789 101112 131415
    # opcode =line[0:5]
    # reg1=line[7:10]
    # reg2=line[10:13]
    # reg3=line[13:]
    # to do reg3=reg1^reg2
    reg["111"] = "0000000000000000"
    reg1_val=int(reg[line[7:10]],2)
    reg2_val=int(reg[line[10:13]],2)
    reg3_val=int(reg[line[13:]],2)
    reg3_val=reg1_val^reg2_val
    b=convert(reg3_val)
    reg[line[13:]]=b

    return convert(int(pc,2)+1)

def OR(line,pc):
    reg["111"] = "0000000000000000"
    reg1_val=int(reg[line[7:10]],2)
    reg2_val=int(reg[line[10:13]],2)
    reg3_val=int(reg[line[13:]],2)
    reg3_val=reg1_val | reg2_val
    b=convert(reg3_val)
    reg[line[13:]]=b

    return convert(int(pc,2)+1)

def NOT(line,pc):
    reg["111"] = "0000000000000000"
    reg1_val=int(reg[line[10:13]],2)
    reg2_val=int(reg[line[13:16]],2)
    reg2_val=~reg1_val
    b=convert(reg2_val)
    reg[line[13:16]]=b

    return convert(int(pc,2)+1)

def div(line,pc):
    reg["111"]="0000000000000000"

    reg3_val= int(reg[line[10:13]], 2)
    reg4_val = int(reg[line[13:16]], 2)
    quotient = convertTo16(reg3_val//reg4_val)
    remainder= convertTo16(reg3_val % reg4_val)

    reg["000"]=quotient
    reg["001"]=remainder

    return convert(int(pc,2)+1)

def AND(line,pc):
    reg["111"] = "0000000000000000"
    reg1_val=int(reg[line[7:10]],2)
    reg2_val=int(reg[line[10:13]],2)
    reg3_val=int(reg[line[13:]],2)
    reg3_val=reg1_val & reg2_val
    b=convert(reg3_val)
    reg[line[13:]]=b

    return convert(int(pc,2)+1)

def Compare(line,pc):
    R1=int(reg[line[10:13]],2)
    R2=int(reg[line[13:]],2)
    num1 = R1
    num2 = R2
    flag_list = list(reg["111"])
    if(num1 == num2):
        flag_list[-1] == "1"
    elif(num1 > num2):
        flag_list[-2] == "1"
    else:
        flag_list[-3] = "1"
        reg["111"] == "".join(flag_list) 

    return convert(int(pc,2)+1)            

def jump_uncond(line):
    return line[8:]

def jump_if_less(line, pc):
    if (reg['111'][-3] == '1'):
        return line[8:]
    else:
        return convert(int(pc, 2)+1)


def jump_if_greater(line, pc):
    if (reg['111'][-2] == '1'):
        return line[8:]
    else:
        return convert(int(pc, 2)+1)


def jump_if_equal(line, pc):
    if (reg['111'][-1] == '1'):
        return line[8:]
    else:
        return convert(int(pc, 2)+1)

def MemoryAddresses(Memory):
    for i in Memory.keys():
        print(Memory[i])

# def PCValuesPrint():
def ProgramCounter(pc):
    print(pc,end = " ")
    
def Hlt(pc):
    for i in reg.keys():
        print(reg[i],end=" ")
    print()
    return pc

def RegisterFile_Dump():
    for i in reg.keys():
        print(reg[i],end=" ")
    print()


pc = "00000000"
BinInstruction = {}
# a = []
Memory = {}
var = 0
for line in sys.stdin:
    if '\n' == line:
        break
    BinInstruction[convert(var)] = line
    Memory[convert(var)] = line
    var += 1

MemLength = len(Memory)

while(MemLength < 256):
    Memory[convert(MemLength)] = "0000000000000000"
    MemLength += 1
def MEEM(pc):
    while(1):
        ProgramCounter(pc)
        if(pc==convert(len(BinInstruction)-1)):
            RegisterFile_Dump()
            break
        if (BinInstruction[pc][0:5] == "00000"):
            pc=addition(BinInstruction[pc],pc)
        elif (BinInstruction[pc][0:5] == "00001"):
            pc=substraction(BinInstruction[pc],pc)
        elif (BinInstruction[pc][0:5] == "00010"):
            pc=mov_imm(BinInstruction[pc],pc)
        elif (BinInstruction[pc][0:5] == "00011"):
            pc=mov_register(BinInstruction[pc],pc)
        elif (BinInstruction[pc][0:5] == "00100"):
            pc=load(BinInstruction[pc],pc)
        elif (BinInstruction[pc][0:5] == "00101"):
            pc=store(BinInstruction[pc],pc)
        elif (BinInstruction[pc][0:5] == "00110"):
            pc=multiply(BinInstruction[pc],pc)
        elif (BinInstruction[pc][0:5] == "00111"):
            pc=div(BinInstruction[pc],pc)
        elif (BinInstruction[pc][0:5] == "01000"):
            pc=rs(BinInstruction[pc],pc)
        elif (BinInstruction[pc][0:5] == "01001"):
            pc=ls(BinInstruction[pc],pc)
        elif (BinInstruction[pc][0:5] == "01010"):
            pc=xor(BinInstruction[pc],pc)
        elif (BinInstruction[pc][0:5] == "01011"):
            pc=OR(BinInstruction[pc],pc)
        elif (BinInstruction[pc][0:5] == "01100"):
            pc=AND(BinInstruction[pc],pc)
        elif (BinInstruction[pc][0:5] == "01101"):
            pc= NOT(BinInstruction[pc],pc)
        elif (BinInstruction[pc][0:5] == "01110"):
            pc=Compare(BinInstruction[pc],pc)
        elif (BinInstruction[pc][0:5] == "01111"):
            pc=jump_uncond(BinInstruction[pc],pc)
        elif (BinInstruction[pc][0:5] == "10000"):
            pc=jump_if_less(BinInstruction[pc],pc)
            reg["111"] = "0000000000000000"
        elif (BinInstruction[pc][0:5] == "10001"):
            pc=jump_if_greater(BinInstruction[pc],pc)
            reg["111"] = "0000000000000000"
        elif (BinInstruction[pc][0:5] == "10010"):
            pc=jump_if_equal(BinInstruction[pc],pc)
            reg["111"] = "0000000000000000"
        elif (BinInstruction[pc][0:5] == "10011"):
            # print(pc,end = " ")
            pc = Hlt(pc)
            # for i in reg.keys():
            #     print(reg[i],end=" ")
            # print()
            RegisterFile_Dump()
            break
        RegisterFile_Dump()

    MemoryAddresses(Memory)
MEEM(pc)