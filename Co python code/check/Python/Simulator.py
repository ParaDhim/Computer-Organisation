import matplotlib.pyplot as plt

import numpy as np
X=[]
Y=[]
def plot( x_dim, y_dim):
    '''
    x_dim and y_dim should be such that both the figures are visible inside the plot
    '''
    x_dim, y_dim = 1.2 * x_dim, 1.2 * y_dim
    plt.plot((0, x_dim), [0, 0], 'k-')
    plt.plot([0, 0], (0, y_dim), 'k-')
    plt.xlim(0, x_dim)
    plt.ylim(0, y_dim)
    plt.xlabel("Cycle number")
    plt.ylabel("Accessed memory address")
    plt.grid()
    sams="CO"+str(len(X))+".png"
    plt.savefig(sams)
    plt.show()
def Pd():
    plt.scatter(X,Y,c="blue")
    plot(max(X),max(Y))

def convert1(a):
    # convert integer to 16 bit binary
    bnr = bin(a).replace('0b', '')
    x = bnr[::-1]  # this reverses an array
    while len(x) < 16:
        x += '0'
    bnr = x[::-1]
    return bnr


def convert(a):
    # convert integer to 8 bit binary
    bnr = bin(a).replace('0b', '')
    x = bnr[::-1]  # this reverses an array
    while len(x) < 8:
        x += '0'
    bnr = x[::-1]
    return bnr
statements = {}
var = 0
pc ="00000000"
reg = {'000': "0000000000000000",
       '001': "0000000000000000",
       '010': "0000000000000000",
       '011': "0000000000000000",
       '100': "0000000000000000",
       '101': "0000000000000000",
       '110': "0000000000000000",
       '111': "0000000000000000"}
while (1):
    try:
        line = input()
        if(line!=""):
            statements[convert(var)] = line
            var += 1
    except EOFError:
        break
MEM = statements.copy()
mlen = len(MEM)
while (mlen <= 255):
    MEM[convert(mlen)] = "0000000000000000"
    mlen+=1
def mov1(l,pc):
    reg["111"]="0000000000000000"
    reg[l[5:8]]=convert1(int(l[8:], 2))
    return convert(int(pc,2)+1)


def mov2(l,pc):
    reg[l[10:13]]=convert1(int(reg[l[13:]],2))
    reg["111"]="0000000000000000"
    return convert(int(pc,2)+1)


def add(l,pc):
    reg["111"] = "0000000000000000"
    n1 = int(reg[l[10:13]], 2)
    n2 = int(reg[l[13:16]], 2)
    x = (n1 + n2)
    y = bin(x)
    if len(y) > 18:
        reg[l[7:10]] = y[-16:]
        reg['111'] = convert1(int(reg['111'], 2) + 8)
    else:
        reg[l[7:10]] = convert1(x)
    return convert(int(pc, 2) + 1)

def sub(l,pc):
    reg["111"] = "0000000000000000"
    n1 = int(reg[l[10:13]], 2)
    n2 = int(reg[l[13:]], 2)
    x = (n1 - n2)
    if x < 0:
        reg[l[7:10]] ="0000000000000000"
        reg['111'] = convert1(int(reg['111'], 2) + 8)
    else:
        reg[l[7:10]] = convert1(x)
    return convert(int(pc,2)+1)

def mul(l,pc):
    reg["111"] = "0000000000000000"
    n1 = int(reg[l[10:13]], 2)
    n2 = int(reg[l[13:16]], 2)
    x = (n1 * n2)
    y = bin(x)
    if len(y) > 18:
        reg[l[7:10]]=y[-16:]
        reg['111'] = convert1(int(reg['111'], 2) + 8)

    else:
        reg[l[7:10]] = convert1(x)
    return convert(int(pc,2)+1)

def div(l,pc):
    reg["111"]="0000000000000000"
    n1 = int(reg[l[10:13]], 2)
    n2 = int(reg[l[13:16]], 2)
    x = (n1 // n2)
    y = n1 % n2
    x = convert1(x)
    y = convert1(y)
    reg["000"]=x
    reg["001"]=y
    return convert(int(pc,2)+1)

def left_shift(l,pc):
    reg["111"] = "0000000000000000"
    x = int(reg[l[5:8]], 2) << int(l[8:], 2)
    x = convert1(x)
    if (len(x) > 16):
        reg['111'] = (bin(int(reg['111'], 2) + 8))[2:]
    else:
        reg[l[5:8]] = x
    return convert(int(pc,2)+1)

def right_shift(l,pc):
    reg["111"] = "0000000000000000"
    x = int(reg[l[5:8]], 2) >> int(l[8:], 2)
    x = convert1(x)
    reg[l[5:8]] = x
    return convert(int(pc,2)+1)

def xor_fnc(l,pc):
    reg["111"] = "0000000000000000"
    reg[l[7:10]] = convert1(int(reg[l[10:13]], 2) ^ int(reg[l[13:]], 2))
    return convert(int(pc,2)+1)

def or_fnc(l,pc):
    reg["111"] = "0000000000000000"
    reg[l[7:10]] = convert1(int(reg[l[10:13]], 2) | int(reg[l[13:]], 2))
    return convert(int(pc,2)+1)

def and_fnc(l,pc):
    reg["111"] = "0000000000000000"
    reg[l[7:10]] = convert1(int(reg[l[10:13]], 2) & int(reg[l[13:]], 2))

    return convert(int(pc,2)+1)
def not_fnc(l,pc):
    
    reg["111"] = "0000000000000000"
    lam=convert1(int(reg[l[13:]], 2))
    lam=lam.replace("0","2")
    lam=lam.replace("1","0")
    lam=lam.replace("2","1")
    reg[l[10:13]] = lam
    return convert(int(pc,2)+1)

def load(l,pc):
    reg["111"] = "0000000000000000"
    reg[l[5:8]] = MEM[l[8:]]
    X.append(X[-1])
    Y.append(int(l[8:], 2))
    return convert(int(pc,2)+1)

def store(l,pc):
    reg["111"] = "0000000000000000"
    MEM[l[8:]] = reg[l[5:8]]
    X.append(X[-1])
    Y.append(int(l[8:], 2))
    return convert(int(pc,2)+1)

def compare(l,pc):

    reg['111'] = '0000000000000000'
    if int(reg[l[10:13]], 2) == int(reg[l[13:]], 2):
        reg['111'] = convert1(int(reg['111'], 2) + 1)
    elif int(reg[l[10:13]], 2) > int(reg[l[13:]], 2):
        reg['111'] = convert1(int(reg['111'], 2) + 2)
    elif int(reg[l[10:13]], 2) < int(reg[l[13:]], 2):
        reg['111'] = convert1(int(reg['111'], 2) + 4)
    return convert(int(pc,2)+1)

def jump_uncond(l,pc):
    return l[8:]
def jump_if_less(l,pc):
    if (reg['111'][-3] == '1'):
        return l[8:]
    else:
        return convert(int(pc, 2) + 1)

def jump_if_greater(l,pc):
    if (reg['111'][-2] == '1'):
        return l[8:]
    return convert(int(pc, 2) + 1)

def jump_if_equal(l,pc):
    if (reg['111'][-1] == '1'):
        return l[8:]
    return convert(int(pc, 2) + 1)

def halt(pc):
    RF_dump()
    print()
    return pc

def PC_dump(pc):####
    print(pc,end=" ")


def MEM_DUMP():
    for i in MEM.keys():
        print(MEM[i])


def RF_dump():
    for i in reg.keys():
        print(reg[i],end=" ")
    print()

def M(pc):
    c=0
    while(1):
    
        X.append(c)
        Y.append(int(pc, 2))
        c=c+1
        PC_dump(pc)####
        if(pc==convert(len(statements)-1)):
            RF_dump()
            break
        if (statements[pc][0:5] == "00000"):
            pc=add(statements[pc],pc)
            
        elif (statements[pc][0:5] == "00001"):
            pc=sub(statements[pc],pc)
        elif (statements[pc][0:5] == "00010"):
            pc=mov1(statements[pc],pc)
        elif (statements[pc][0:5] == "00011"):
            pc=mov2(statements[pc],pc)
        elif (statements[pc][0:5] == "00100"):
            pc=load(statements[pc],pc)
        elif (statements[pc][0:5] == "00101"):
            pc=store(statements[pc],pc)
        elif (statements[pc][0:5] == "00110"):
            pc=mul(statements[pc],pc)
        elif (statements[pc][0:5] == "00111"):
            pc=div(statements[pc],pc)
        elif (statements[pc][0:5] == "01000"):
            pc=right_shift(statements[pc],pc)
        elif (statements[pc][0:5] == "01001"):
            pc=left_shift(statements[pc],pc)
        elif (statements[pc][0:5] == "01010"):
            pc=xor_fnc(statements[pc],pc)
        elif (statements[pc][0:5] == "01011"):
            pc=or_fnc(statements[pc],pc)
        elif (statements[pc][0:5] == "01100"):
            pc=and_fnc(statements[pc],pc)
        elif (statements[pc][0:5] == "01101"):
            pc=not_fnc(statements[pc],pc)
        elif (statements[pc][0:5] == "01110"):
            pc=compare(statements[pc],pc)
        elif (statements[pc][0:5] == "01111"):
            pc=jump_uncond(statements[pc],pc)
        elif (statements[pc][0:5] == "10000"):
            pc=jump_if_less(statements[pc],pc)
            reg["111"] = "0000000000000000"
        elif (statements[pc][0:5] == "10001"):
            pc=jump_if_greater(statements[pc],pc)
            reg["111"] = "0000000000000000"
        elif (statements[pc][0:5] == "10010"):
            pc=jump_if_equal(statements[pc],pc)
            reg["111"] = "0000000000000000"
        elif (statements[pc][0:5] == "10011"):
            pc=halt(pc)
            RF_dump()
            break
        RF_dump()
        
    MEM_DUMP()
M(pc)
#Pd()

# print(convert1(int(reg['111'], 2) + 8));