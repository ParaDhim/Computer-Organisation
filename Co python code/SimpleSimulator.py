import matplotlib.pyplot

#max allowed value
maxVal = 2**16 - 1

#inputting the machine code (16-bits)
"""[["1000000001010011"]
    ["1011000100101110"]
    ["1001000100000101"]
    ["0101000000000000"]
    ...]"""
normal = []
while True:
    try:
        line = input()
        normal.append(line)
    except EOFError:
        break

for i in normal:
    if i == []:
        normal.remove(i)

#memory dump
mem = []
def mem_dump():
    for line in normal:
        mem.append(line)
    while len(mem) < 256:
        mem.append("0000000000000000")

mem_dump()

#decimal to binary conversion
def ConvertBinary(number):
    if (number > 0 or number==0): 
        if number == 0:
            return "0"
        if number == 1:
            return "1"
        if number % 2 == 0:
            return ConvertBinary(number//2) + "0"
        else:
            return ConvertBinary(number//2) + "1"

#binary to decimal conversion
def ConvertDecimal(binary):
    decimal = 0
    for i in range(len(binary)):
        decimal += int(binary[i])*(2**(len(binary)-i-1))
    return decimal

#function to increase the length of a binary number
def IncBinarylength(binary,length):
    while len(binary) < length:
        binary = "0" + binary
    return binary

#resetting the flags
def FLAGS_reset():
    FLAGS["V"] = FLAGS["L"] = FLAGS["G"] = FLAGS["E"] = "0"

#registers
registers = ["R0", "R1", "R2", "R3", "R4", "R5", "R6", "FLAGS"]

#opcodes
opcode = {"add":"10000", "sub":"10001", "mov":["10010", "10011"], 
"ld":"10100", "st":"10101", "mul":"10110", "div":"10111", 
"rs":"11000", "ls":"11001", "xor":"11010", "or":"11011", 
"and":"11100", "not":"11101", "cmp":"11110", "jmp":"11111", 
"jlt":"01100", "jgt":"01101", "je":"01111", "hlt":"01010"}

#FLAGS Semantics
FLAGS = {"V":"0", "L":"0", "G":"0", "E":"0"}

#values of the registers initiated to 0
reg_vals = {
"000":0,  #R0
"001":0,  #R1
"010":0,  #R2
"011":0,  #R3
"100":0,  #R4
"101":0,  #R5
"110":0,  #R6
"111":0  #FLAGS Value
}  

#functions for instructions
def add(line):
    num = reg_vals[line[7:10]] + reg_vals[line[10:13]] 
    if num > maxVal:
        reg_vals[line[13:16]] = maxVal
        FLAGS["V"] = "1"
        reg_vals["111"] = ConvertDecimal(FLAGS["V"] + FLAGS["L"] + FLAGS["G"] + FLAGS["E"])
    else:
        reg_vals[line[13:16]] = num
        reg_vals["111"] = ConvertDecimal(FLAGS["V"] + FLAGS["L"] + FLAGS["G"] + FLAGS["E"])
    return reg_vals[line[13:16]]

def sub(line):
    num = reg_vals[line[7:10]] - reg_vals[line[10:13]]
    if num < 0:
        reg_vals[line[13:16]] = 0
        FLAGS["V"] = "1"
        reg_vals["111"] = ConvertDecimal(FLAGS["V"] + FLAGS["L"] + FLAGS["G"] + FLAGS["E"])
    else:
        reg_vals[line[13:16]] = num
        reg_vals["111"] = ConvertDecimal(FLAGS["V"] + FLAGS["L"] + FLAGS["G"] + FLAGS["E"])
    return reg_vals[line[13:16]]

def mov_imm(line):
    binary_num = line[8:16]
    num = ConvertDecimal(binary_num)
    if num > maxVal:
        reg_vals[line[5:8]] = maxVal
        FLAGS["V"] = "1"
        reg_vals["111"] = ConvertDecimal(FLAGS["V"] + FLAGS["L"] + FLAGS["G"] + FLAGS["E"])
    else:
        reg_vals[line[5:8]] = num
        reg_vals["111"] = ConvertDecimal(FLAGS["V"] + FLAGS["L"] + FLAGS["G"] + FLAGS["E"])
    return reg_vals[line[5:8]]

def mov_reg(line):
    num = reg_vals[line[10:13]]
    if num > maxVal:
        reg_vals[line[13:16]] = maxVal
        FLAGS["V"] = "1"
        reg_vals["111"] = ConvertDecimal(FLAGS["V"] + FLAGS["L"] + FLAGS["G"] + FLAGS["E"])
    else:
        reg_vals[line[13:16]] = num
        reg_vals["111"] = ConvertDecimal(FLAGS["V"] + FLAGS["L"] + FLAGS["G"] + FLAGS["E"])
    return reg_vals[line[13:16]]

def ld(line):
    reg_vals[line[5:8]] = ConvertDecimal(mem[ConvertDecimal(line[8:16])])

def st(line):
    mem[ConvertDecimal(line[8:16])] = IncBinarylength(ConvertBinary(reg_vals[line[5:8]]), 16)

def mul(line):
    num = reg_vals[line[7:10]] * reg_vals[line[10:13]]
    if num > maxVal:
        num = maxVal
        FLAGS["V"] = "1"
        reg_vals["111"] = ConvertDecimal(FLAGS["V"] + FLAGS["L"] + FLAGS["G"] + FLAGS["E"])
    else:
        reg_vals[line[13:16]] = num
        reg_vals["111"] = ConvertDecimal(FLAGS["V"] + FLAGS["L"] + FLAGS["G"] + FLAGS["E"])
    return reg_vals[line[13:16]]

def div(line):
    quotient = reg_vals[line[10:13]] // reg_vals[line[13:16]]
    remainder = reg_vals[line[10:13]] % reg_vals[line[13:16]]
    if quotient > maxVal:
        reg_vals["000"] = maxVal
        FLAGS["V"] = "1"
        reg_vals["111"] = ConvertDecimal(FLAGS["V"] + FLAGS["L"] + FLAGS["G"] + FLAGS["E"])
    else:
        reg_vals["000"] = quotient
        reg_vals["111"] = ConvertDecimal(FLAGS["V"] + FLAGS["L"] + FLAGS["G"] + FLAGS["E"])

    if remainder > maxVal:
        reg_vals["001"] = maxVal
        FLAGS["V"] = "1"
        reg_vals["111"] = ConvertDecimal(FLAGS["V"] + FLAGS["L"] + FLAGS["G"] + FLAGS["E"])
    else:
        reg_vals["001"] = remainder
        reg_vals["111"] = ConvertDecimal(FLAGS["V"] + FLAGS["L"] + FLAGS["G"] + FLAGS["E"])
    return [reg_vals["000"], reg_vals["001"]]

def rs(line):
    temp = int(ConvertDecimal(line[8:16]))
    num = reg_vals[line[5:8]] // (2**temp)
    if num > maxVal:
        reg_vals[line[5:8]] = maxVal
        FLAGS["V"] = "1"
        reg_vals["111"] = ConvertDecimal(FLAGS["V"] + FLAGS["L"] + FLAGS["G"] + FLAGS["E"])
    else:
        reg_vals[line[5:8]] = num
        reg_vals["111"] = ConvertDecimal(FLAGS["V"] + FLAGS["L"] + FLAGS["G"] + FLAGS["E"])
    return reg_vals[line[5:8]]

def ls(line):
    temp = int(ConvertDecimal(line[8:16]))
    num = reg_vals[line[5:8]] * (2**temp)
    if num > maxVal:
        reg_vals[line[5:8]] = maxVal
        FLAGS["V"] = "1"
        reg_vals["111"] = ConvertDecimal(FLAGS["V"] + FLAGS["L"] + FLAGS["G"] + FLAGS["E"])
    else:
        reg_vals[line[5:8]] = num
        reg_vals["111"] = ConvertDecimal(FLAGS["V"] + FLAGS["L"] + FLAGS["G"] + FLAGS["E"])
    return reg_vals[line[5:8]]

def xor(line):
    reg1 = ConvertBinary(reg_vals[line[7:10]])
    reg2 = ConvertBinary(reg_vals[line[10:13]])
    reg3 = ""
    max_len = max(len(reg1), len(reg2))
    while len(reg1) < max_len:
        reg1 = "0" + reg1
    while len(reg2) < max_len:
        reg2 = "0" + reg2

    for i in range(max_len):
        if reg1[i] == "1" and reg2[i] == "1":
            reg3 = reg3 + "0"
        elif reg1[i] == "0" and reg2[i] == "0":
            reg3 = reg3 + "0"
        else:
            reg3 = reg3 + "1"
    num = ConvertDecimal(reg3)
    if num > maxVal:
        reg_vals[line[13:16]] = maxVal
        FLAGS["V"] = "1"
        reg_vals["111"] = ConvertDecimal(FLAGS["V"] + FLAGS["L"] + FLAGS["G"] + FLAGS["E"])
    else:
        reg_vals[line[13:16]] = num
        reg_vals["111"] = ConvertDecimal(FLAGS["V"] + FLAGS["L"] + FLAGS["G"] + FLAGS["E"])
    return reg_vals[line[13:16]]

def OR(line):
    reg1 = ConvertBinary(reg_vals[line[7:10]])
    reg2 = ConvertBinary(reg_vals[line[10:13]])
    reg3 = ""
    max_len = max(len(reg1), len(reg2))
    while len(reg1) < max_len:
        reg1 = "0" + reg1
    while len(reg2) < max_len:
        reg2 = "0" + reg2

    for i in range(max_len):
        if reg1[i] == "1":
            reg3 = reg3 + "1"
        elif reg2[i] == "1":
            reg3 = reg3 + "1"
        else:
            reg3 = reg3 + "0"

    num = ConvertDecimal(reg3)
    if num > maxVal:
        reg_vals[line[13:16]] = maxVal
        FLAGS["V"] = "1"
        reg_vals["111"] = ConvertDecimal(FLAGS["V"] + FLAGS["L"] + FLAGS["G"] + FLAGS["E"])
    else:
        reg_vals[line[13:16]] = num
        reg_vals["111"] = ConvertDecimal(FLAGS["V"] + FLAGS["L"] + FLAGS["G"] + FLAGS["E"])
    return reg_vals[line[13:16]]

def AND(line):
    reg1 = ConvertBinary(reg_vals[line[7:10]])
    reg2 = ConvertBinary(reg_vals[line[10:13]])
    reg3 = ""
    max_len = max(len(reg1), len(reg2))
    while len(reg1) < max_len:
        reg1 = "0" + reg1
    while len(reg2) < max_len:
        reg2 = "0" + reg2

    for i in range(max_len):
        if reg1[i] == "1" and reg2[i] == "1":
            reg3 = reg3 + "1"
        else:
            reg3 = reg3 + "0"

    num = ConvertDecimal(reg3)
    if num > maxVal:
        reg_vals[line[13:16]] = maxVal
        FLAGS["V"] = "1"
        reg_vals["111"] = ConvertDecimal(FLAGS["V"] + FLAGS["L"] + FLAGS["G"] + FLAGS["E"])
    else:
        reg_vals[line[13:16]] = num
        reg_vals["111"] = ConvertDecimal(FLAGS["V"] + FLAGS["L"] + FLAGS["G"] + FLAGS["E"])
    return reg_vals[line[13:16]]

def invert(line):  #not
    reg1 = ConvertBinary(reg_vals[line[10:13]])
    reg2 = ""
    for bit in reg1:
        if bit == "1":
            reg2 = reg2 + "0"
        else:
            reg2 = reg2 + "1"
    num = ConvertDecimal(reg2)
    if num > maxVal:
        reg_vals[line[13:16]] = maxVal
        FLAGS["V"] = "1"
        reg_vals["111"] = ConvertDecimal(FLAGS["V"] + FLAGS["L"] + FLAGS["G"] + FLAGS["E"])
    else:
        reg_vals[line[13:16]] = num
        reg_vals["111"] = ConvertDecimal(FLAGS["V"] + FLAGS["L"] + FLAGS["G"] + FLAGS["E"])
    return reg_vals[line[13:16]]


def cmp(line):
    reg1 = reg_vals[line[10:13]]
    reg2 = reg_vals[line[13:16]]
    if reg1 > reg2:
        FLAGS["G"] = "1"
        FLAGS["E"] = "0"
        FLAGS["L"] = "0"
    elif reg1 == reg2:
        FLAGS["E"] = "1"
        FLAGS["G"] = "0"
        FLAGS["L"] = "0"
    elif reg1 < reg2:
        FLAGS["L"] = "1"
        FLAGS["E"] = "0"
        FLAGS["G"] = "0"
    reg_vals["111"] = ConvertDecimal(FLAGS["V"] + FLAGS["L"] + FLAGS["G"] + FLAGS["E"])


def jmp(line):
    mem_addr = line[8:16]
    reg_vals["111"] = ConvertDecimal(FLAGS["V"] + FLAGS["L"] + FLAGS["G"] + FLAGS["E"])
    return ConvertDecimal(mem_addr)

def jlt(line):
    mem_addr = line[8:16]
    reg_vals["111"] = ConvertDecimal(FLAGS["V"] + FLAGS["L"] + FLAGS["G"] + FLAGS["E"])
    return ConvertDecimal(mem_addr)

def jgt(line):
    mem_addr = line[8:16]
    reg_vals["111"] = ConvertDecimal(FLAGS["V"] + FLAGS["L"] + FLAGS["G"] + FLAGS["E"])
    return ConvertDecimal(mem_addr)

def je(line):
    mem_addr = line[8:16]
    reg_vals["111"] = ConvertDecimal(FLAGS["V"] + FLAGS["L"] + FLAGS["G"] + FLAGS["E"])
    return ConvertDecimal(mem_addr)


"""
def hlt(line):
    pass"""

def printf(PC, reg_vals):
    print(IncBinarylength(ConvertBinary(PC), 8), 
            IncBinarylength(ConvertBinary(reg_vals["000"]), 16),
            IncBinarylength(ConvertBinary(reg_vals["001"]), 16),
            IncBinarylength(ConvertBinary(reg_vals["010"]), 16),
            IncBinarylength(ConvertBinary(reg_vals["011"]), 16),
            IncBinarylength(ConvertBinary(reg_vals["100"]), 16),
            IncBinarylength(ConvertBinary(reg_vals["101"]), 16),
            IncBinarylength(ConvertBinary(reg_vals["110"]), 16),
            "000000000000" + FLAGS["V"] + FLAGS["L"] + FLAGS["G"] + FLAGS["E"])

#Bonus Question: Q4
def MemoryAccessTrace(x_axis, y_axis):
    matplotlib.pyplot.scatter(x_axis, y_axis)
    matplotlib.pyplot.show()

#function to print memory
def printMemory():
    for i in mem:
        print(i)

#program counter
PC = 0
cycle = 1

x_axis, y_axis = [], []

#executing the instructions
while normal[PC] != "0101000000000000":
        
    if normal[PC][0:5] == "10000":  #add
        FLAGS_reset()
        add(normal[PC])
        
        printf(PC, reg_vals)
        x_axis.append(cycle)
        y_axis.append(PC)
        PC += 1
        cycle += 1
    
    elif normal[PC][0:5] == "00000":  #addf
        FLAGS_reset()
        add(normal[PC])
        
        printf(PC, reg_vals)
        x_axis.append(cycle)
        y_axis.append(PC)
        PC += 1
        cycle += 1
        
    elif normal[PC][0:5] == "10001":  #sub
        FLAGS_reset()
        sub(normal[PC])
        
        printf(PC, reg_vals)
        x_axis.append(cycle)
        y_axis.append(PC)
        PC += 1
        cycle += 1

    elif normal[PC][0:5] == "10010":  #mov immediate
        FLAGS_reset()
        mov_imm(normal[PC])
        
        printf(PC, reg_vals)
        x_axis.append(cycle)
        y_axis.append(PC)
        PC += 1
        cycle += 1

    elif normal[PC][0:5] == "10011":  #mov register
        FLAGS_reset()
        mov_reg(normal[PC])
        
        printf(PC, reg_vals)
        x_axis.append(cycle)
        y_axis.append(PC)
        PC += 1
        cycle += 1

    elif normal[PC][0:5] == "10100":  #ld
        FLAGS_reset()
        ld(normal[PC])
        
        printf(PC, reg_vals)
        x_axis.append(cycle)
        y_axis.append(PC)
        PC += 1
        cycle += 1
        
    elif normal[PC][0:5] == "10101":  #st
        FLAGS_reset()
        st(normal[PC])
        
        printf(PC, reg_vals)
        x_axis.append(cycle)
        y_axis.append(PC)
        PC += 1
        cycle += 1

    elif normal[PC][0:5] == "10110":  #mul
        FLAGS_reset()
        mul(normal[PC])
        
        printf(PC, reg_vals)
        x_axis.append(cycle)
        y_axis.append(PC)
        PC += 1
        cycle += 1

    elif normal[PC][0:5] == "10111":  #div
        FLAGS_reset()
        div(normal[PC])[0]
        
        printf(PC, reg_vals)
        x_axis.append(cycle)
        y_axis.append(PC)
        PC += 1
        cycle += 1

    elif normal[PC][0:5] == "11000":  #rs
        FLAGS_reset()
        rs(normal[PC])
        
        printf(PC, reg_vals)
        x_axis.append(cycle)
        y_axis.append(PC)
        PC += 1
        cycle += 1

    elif normal[PC][0:5] == "11001":  #ls
        FLAGS_reset()
        ls(normal[PC])
        
        printf(PC, reg_vals)
        x_axis.append(cycle)
        y_axis.append(PC)
        PC += 1
        cycle += 1

    elif normal[PC][0:5] == "11010":  #xor
        FLAGS_reset()
        xor(normal[PC])
        
        printf(PC, reg_vals)
        x_axis.append(cycle)
        y_axis.append(PC)
        PC += 1
        cycle += 1
        

    elif normal[PC][0:5] == "11011":  #or
        FLAGS_reset()
        OR(normal[PC])
        
        printf(PC, reg_vals)
        x_axis.append(cycle)
        y_axis.append(PC)
        PC += 1
        cycle += 1
        
    elif normal[PC][0:5] == "11100":  #and
        FLAGS_reset()
        AND(normal[PC])
        
        printf(PC, reg_vals)
        x_axis.append(cycle)
        y_axis.append(PC)
        PC += 1
        cycle += 1

    elif normal[PC][0:5] == "11101":  #not
        FLAGS_reset()
        invert(normal[PC])
        
        printf(PC, reg_vals)
        x_axis.append(cycle)
        y_axis.append(PC)
        PC += 1
        cycle += 1

    elif normal[PC][0:5] == "11110":  #cmp 
        FLAGS_reset()
        cmp(normal[PC])
        printf(PC, reg_vals)
        x_axis.append(cycle)
        y_axis.append(PC)
        PC += 1
        cycle += 1
        

    elif normal[PC][0:5] == "11111":  #jmp
        FLAGS_reset()
        printf(PC, reg_vals)
        
        x_axis.append(cycle)
        y_axis.append(PC)
        newPC = jmp(normal[PC])
        PC = newPC
        cycle += 1

    elif normal[PC][0:5] == "01100":  #jlt
        x_axis.append(cycle)
        y_axis.append(PC)
        if FLAGS["L"] == "1":
            newPC = jlt(normal[PC])
            
            FLAGS_reset()
            printf(PC, reg_vals)
            PC = newPC
        else:
            FLAGS_reset()
            printf(PC, reg_vals)
            PC += 1
            
        cycle += 1

    elif normal[PC][0:5] == "01101":  #jgt
        x_axis.append(cycle)
        y_axis.append(PC)
        if FLAGS["G"] == "1":
            newPC = jgt(normal[PC])
            
            FLAGS_reset()
            printf(PC, reg_vals)
            PC = newPC
        else:
            FLAGS_reset()
            printf(PC, reg_vals)
            PC += 1
            
        cycle += 1
            
    elif normal[PC][0:5] == "01111":  #je
        x_axis.append(cycle)
        y_axis.append(PC)
        if FLAGS["E"] == "1":
            newPC = je(normal[PC])

            FLAGS_reset()
            printf(PC, reg_vals)
            PC = newPC
        else:
            FLAGS_reset()
            printf(PC, reg_vals)
            PC += 1
            
        cycle += 1  
        
x_axis.append(cycle)
y_axis.append(PC)
printf(PC, reg_vals)

printMemory()
MemoryAccessTrace(x_axis, y_axis)
