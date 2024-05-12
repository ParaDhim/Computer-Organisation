from operator import index
count = 0

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


normal = []
while True:
    try:
        line = input()
        normal.append(line.split())
    except EOFError:
        break

for i in normal:
    if i==[]:
        normal.remove(i)


instructions = ["add", "sub", "mov", "ld", "st", "mul", "div", "rs", "ls", "xor", "or", "and", "not", "cmp", "jmp", "jlt", "jgt", "je", "hlt","var"]
registers = ["R0", "R1", "R2", "R3", "R4", "R5", "R6","r0", "r1", "r2", "r3", "r4", "r5", "r6", "FLAGS"]

labels= []
for i in normal: 
    if i[0][-1]==":":
        labels.append(i[0][0:-1])

var_list = []
var={}
for i in range(len(normal)): 
            if normal[i][0] == "var" and len(normal[i])==2:
                var[i+1]=normal[i][1]
            elif normal[i][0] == "var" and len(normal[i])!=2:
                var[i+1]=0

for i in var:
            var_list.append(var[i])

var_mem={}
a=len(normal)-len(var_list)
for i in range(len(var_list)):
    b=ConvertBinary(a)
    while len(b)<8:
        b="0"+b
    var_mem[var_list[i]]=b
    a+=1

label_mem={}
for i in range(len(normal)):
    if normal[i][0][0:-1] in labels:
        a=i-len(var_list)
        b=ConvertBinary(a)
        while len(b)<8:
            b="0"+b
        label_mem[normal[i][0][0:-1]]=b

def Overflow_error(normal):
    if len(normal)>256:
        print("Error: Memory size exceeded")
        return 1

def halterror(normal , count):
    for i in range(len(normal)):
        if normal[i][0] =="hlt" and i!=len(normal)-1:
            print(f"Error: line {i+1}: hlt instruction not used as the last instruction")
            return 1
        elif normal[i][0]=="hlt":
            count+=1

    for i in range(len(normal)):
       
        if normal[i][0][0:-1] in labels and normal[i][1] =="hlt" and i!=len(normal)-1:
            print(f"Error: line {i+1}: hlt instruction not used as the last instruction")
            return 1
        elif normal[i][0][0:-1] in labels and normal[i][1]=="hlt":
            count+=1
            
    if count==0:
        print("Error: hlt instruction missing")
        return 1

def var_error(normal,var_list,var):
        count=0
        for i in var:
            if var[i]==0:
                print(f"Error: line {int(i)}: Syntax error")
                return 1
        for i in var:
            count+=1
            if int(i)!=count:
                print(f"Error: line {int(i)}: Variable not declared at the start")
                return 1
        
        for i in range(len(normal)): 
            if normal[i][0] == "ld" or normal[i][0] == "st":
                if normal[i][2] not in var_list and normal[i][2] in labels:
                    print(f"Error: line {i+1}: Invalid use of label as variable")  # misuse of labels as variables
                    return 1
                if normal[i][2] not in var_list and normal[i][2] not in labels:
                    print(f"Error: line {i+1}: Variable not declared")
                    return 1

def label_error(normal,labels,var_list):
    for i in range(len(normal)): 
        if normal[i][0] == "jmp" or normal[i][0] == "jlt" or normal[i][0] == "jgt" or normal[i][0] == "je":
            if normal[i][1] not in labels and normal[i][1] in var_list:
                print(f"Error: line {i+1}: Invalid use of variable as label")   # misuse of variabels as lables
                return 1
            if normal[i][1] not in labels and normal[i][1] not in var_list:
                print(f"Error: line {i+1}: Label not declared")
                return 1   

        elif (normal[i][0][0:-1] in labels) and (normal[i][1] == "jmp" or normal[i][1] == "jlt" or normal[i][1] == "jgt" or normal[i][1] == "jeq"):
            if normal[i][2] not in labels and normal[i][2] in var_list:
                print(f"Error: line {i+1}: Invalid use of variable as label")   # misuse of variabels as lables
                return 1
            if normal[i][2] not in labels and normal[i][2] not in var_list:
                print(f"Error: line {i+1}: Label not declared")
                return 1 

def typo_general_error(normal,labels):
    line=1

    for i in normal:
        if i[0] not in instructions and i[0][0:-1] not in labels: 
            print(f"Error: line {line}: Instruction not valid")
            return 1
        elif i[0] == "add" or i[0] == "sub" or i[0] == "mul" or i[0] == "xor" or i[0] == "or" or i[0] ==  "and":
            if len(i) != 4:
                print(f"Error: line {line}: General Syntax Error")
                return 1
            elif i[1] not in registers or i[2] not in registers or i[3] not in registers:
                print(f"Error: line {line}: General Syntax Error")
                return 1

        elif i[0] == "mov":    
            if len(i) != 3:
                print(f"Error: line {line}: General Syntax Error")
                return 1
            elif i[1] not in registers:
                print(f"Error: line {line}: General Syntax Error")
                return 1

            elif i[1] in registers and i[1]!="FLAGS":
                if i[2] in registers and i[2]!="FLAGS":
                    pass
                elif i[2][0]=="$" and i[2][1:].isdigit():
                    pass
                elif i[2][0]=="$" and i[2][1]=="-" and i[2][2:].isdigit():
                    pass
                else:
                    print(f"Error: line {line}: General Syntax Error")
                    return 1
            elif i[1]=="FLAGS":
                if i[2] in registers and i[2]!="FLAGS":
                    pass
                else:
                    print(f"Error: line {line}: Invalid operation on FLAGS register")
                    return 1
        elif i[0] == "ld" or i[0] == "st":
            if len(i) != 3:
                print(f"Error: line {line}: General Syntax Error")
                return 1
            elif i[1] not in registers:
                print(f"Error: line {line}: General Syntax Error")
                return 1


        elif i[0] == "div" or i[0] == "not" or i[0] == "cmp":
            if len(i) != 3:
                print(f"Error: line {line}: General Syntax Error")
                return 1
            elif i[1] not in registers or i[2] not in registers:
                print(f"Error: line {line}: General Syntax Error")
                return 1

        elif i[0] == "rs" or i[0] == "ls":    #changes needed for $Imm #changes made for $Imm
            if len(i) != 3:
                print(f"Error: line {line}: General Syntax Error")
                return 1
            elif i[1] not in registers:
                print(f"Error: line {line}: General Syntax Error")
                return 1
            elif i[2][0] != "$":
                print(f"Error: line {line}: General Syntax Error")
                return 1
            elif (i[2][1:].isdigit() or (i[2][1]=="-" and i[2][2:].isdigit()) ) == False:
                print(f"Error: line {line}: General Syntax Error")
                return 1

        elif i[0] == ("jmp" or i[0] == "jlt" or i[0] == "jgt" or i[0] == "je") and len(i) != 2:
                    print(f"Error: line {line}: General Syntax Error")
                    return 1

        elif i[0]=="hlt" and len(i)!=1:
            print(f"Error: line {line}: General Syntax Error")
            return 1

        elif i[0][0:-1] in labels and len(i) == 1:
            print(f"Error: line {line}: Invalid label") 
            return 1

        elif i[0][0:-1] in labels and (i[1] == "add" or i[1] == "sub" or i[1] == "mul" or i[1] == "xor" or i[1] == "or" or i[1] ==  "and"):
            if len(i) != 5:
                print(f"Error: line {line}: General Syntax Error")
                return 1
            elif i[2] not in registers or i[3] not in registers or i[4] not in registers:
                print(f"Error: line {line}: General Syntax Error")
                return 1

        elif i[0][0:-1] in labels and i[1] == "mov":  #changes needed for $Imm #changes made for $Imm   
            if len(i) != 4:
                print(f"Error: line {line}: General Syntax Error")
                return 1
            elif i[2] not in registers:
                print(f"Error: line {line}: General Syntax Error")
                return 1

            elif i[2] in registers:
                if i[3] in registers:
                    pass
                elif i[3][0]=="$" and i[3][1:].isdigit():
                    pass
                elif i[3][0]=="$" and i[3][1]=="-" and i[3][2:].isdigit():
                    pass
                else:
                    print(f"Error: line {line}: General Syntax Error")
                    return 1
            elif i[2] in registers and i[2]=="FLAGS":
                if i[3] in registers and i[3]!="FLAGS":
                    pass
                else:
                    print(f"Error: line {line}: Invalid operation on FLAGS register")
                    return 1

        elif i[0][0:-1] in labels and (i[1] == "ld" or i[1] == "st"):
            if len(i) != 4:
                print(f"Error: line {line}: General Syntax Error")
                return 1
            elif i[2] not in registers:
                print(f"Error: line {line}: General Syntax Error")
                return 1

        elif i[0][0:-1] in labels and (i[1] == "div" or i[1] == "not" or i[1] == "cmp"):
            if len(i) != 4:
                print(f"Error: line {line}: General Syntax Error")
                return 1
            elif i[2] not in registers or i[3] not in registers:
                print(f"Error: line {line}: General Syntax Error")
                return 1

        elif i[0][0:-1] in labels and (i[1] == "rs" or i[1] == "ls"):    #changes needed for $Imm #changes made for $Imm
            if len(i) != 4:
                print(f"Error: line {line}: General Syntax Error")
                return 1
            elif i[2] not in registers:
                print(f"Error: line {line}: General Syntax Error")
                return 1
            elif i[3][0] != "$":
                print(f"Error: line {line}: General Syntax Error")
                return 1
            elif i[3][1:].isdigit() == False:
                print(f"Error: line {line}: General Syntax Error")
                return 1    

        elif i[0][0:-1] in labels and (i[1] == "jmp" or i[1] == "jlt" or i[1] == "jgt" or i[1] == "je"):
            if len(i) != 3:
                    print(f"Error: line {line}: General Syntax Error")
                    return 1 

        elif i[0][0:-1] in labels and i[1]=="hlt" and len(i)!=2:
            print(f"Error: line {line}: General Syntax Error")
            return 1
        
        line+=1 


def Imm_value_error(normal):
    for i in range(len(normal)):
        if normal[i][0] == "ls" or normal[i][0] == "rs" or normal[i][0] == "mov":
            if normal[i][2][0] == "$":
                num=normal[i][2][1:]
                if int(num)<0:
                    print(f"Error: line {i+1}: Invalid immediate value")
                    return 1
                binary_num= ConvertBinary(int(num))
                if len(binary_num)>8:
                    print(f"Error: line {i+1}: Immediate value out of range")
                    return 1
                
opcode = {"add":"10000", "sub":"10001", "mov":["10010", "10011"], "ld":"10100", "st":"10101", "mul":"10110", "div":"10111", "rs":"11000", "ls":"11001", "xor":"11010", "or":"11011", "and":"11100", 
"not":"11101", "cmp":"11110", "jmp":"11111", "jlt":"01100", "jgt":"01101", "je":"01111", "hlt":"01010"}

reg_code = {"R0":"000", "R1":"001", "R2":"010", "R3":"011", "R4":"100", "R5":"101", "R6":"110","r0":"000", "r1":"001", "r2":"010", "r3":"011", "r4":"100", "r5":"101", "r6":"110", "FLAGS":"111"}

def reg_code_getter(reg):
    for i in reg_code:
        if i == reg:
            return reg_code[i]

def op_code_getter(opcode_key):
    for i in opcode:
        if i == opcode_key:
            return opcode[i]

typeA = ["add", "sub", "mul", "xor", "or", "and"]
typeB = ["mov", "ls", "rs"]
typeC = ["mov", "div", "not", "cmp"]
typeD = ["ld", "st"]
typeE = ["jmp", "jlt", "jgt", "je"]
typeF = ["hlt"]

def TypeA_machineCode(type, instr, machine_code):
    machine_code = machine_code + op_code_getter(typeA[typeA.index(instr[0])]) + "00"
    for reg in instr[1:]:
        machine_code = machine_code + reg_code_getter(reg)
    return machine_code

def TypeB_machineCode(type, instr, machine_code):
    if instr[0] == "mov":
        machine_code = machine_code + "10010"
    else:
        machine_code = machine_code + op_code_getter(typeB[typeB.index(instr[0])])
    machine_code = machine_code + reg_code_getter(instr[1])
    num = ConvertBinary(int(instr[2][1:]))
    while len(num)<8:
        num = "0" + num
    machine_code = machine_code + num
    return machine_code

def TypeC_machineCode(type, instr, machine_code):
    if instr[0] == "mov":
        machine_code = machine_code + "10011" + "00000"
    else:
        machine_code = machine_code + op_code_getter(typeC[typeC.index(instr[0])]) + "00000"
    for reg in instr[1:]:
        machine_code = machine_code + reg_code_getter(reg)
    return machine_code

def TypeD_machineCode(type, instr, machine_code):
    machine_code = machine_code + op_code_getter(typeD[typeD.index(instr[0])]) + reg_code_getter(instr[1]) + var_mem[instr[2]]
    return machine_code

def TypeE_machineCode(type, instr, machine_code):
    machine_code = machine_code + op_code_getter(typeE[typeE.index(instr[0])]) + "000" + label_mem[instr[1]]
    return machine_code

def TypeF_machineCode(type, instr, machine_code):
    return "0101000000000000"

def TypeA_label_machineCode(type, instr, machine_code):
    machine_code = machine_code + op_code_getter(typeA[typeA.index(instr[1])]) + "00"
    for reg in instr[2:]:
        machine_code = machine_code + reg_code_getter(reg)
    return machine_code

def TypeB__label_machineCode(type, instr, machine_code):
    if instr[1] == "mov":
        machine_code = machine_code + "10010"
    else:
        machine_code = machine_code + op_code_getter(typeB[typeB.index(instr[1])])
    machine_code = machine_code + reg_code_getter(instr[2])
    num = ConvertBinary(int(instr[3][1:]))
    while len(num)<8:
        num = "0" + num
    machine_code = machine_code + num
    return machine_code

def TypeC_label_machineCode(type, instr, machine_code):
    if instr[1] == "mov":
        machine_code = machine_code + "10011" + "00000"
    else:
        machine_code = machine_code + op_code_getter(typeC[typeC.index(instr[1])]) + "00000"
    for reg in instr[2:]:
        machine_code = machine_code + reg_code_getter(reg)
    return machine_code

def TypeD_label_machineCode(type, instr, machine_code):
    machine_code = machine_code + op_code_getter(typeD[typeD.index(instr[1])]) + reg_code_getter(instr[2]) + var_mem[instr[3]]
    return machine_code

def TypeE_label_machineCode(type, instr, machine_code):
    machine_code = machine_code + op_code_getter(typeE[typeE.index(instr[1])]) + "000" + label_mem[instr[2]]
    return machine_code

def TypeF_label_machineCode(type, instr, machine_code):
    return "0101000000000000"

def machineCode(normal):
    for instr in normal:
        #Type A
        machine_code = ""
        if instr[0] in typeA:
            print(TypeA_machineCode(instr[0], instr, machine_code))
            machine_code = ""
        #Type B
        if instr[0] in typeB and instr[2] not in registers:
            print(TypeB_machineCode(instr[0], instr, machine_code))
            machine_code = ""
        #Type C
        if instr[0] in typeC and instr[2] in registers:
            print(TypeC_machineCode(instr[0], instr, machine_code))
            machine_code = ""
        #Type D
        if instr[0] in typeD:
            print(TypeD_machineCode(instr[0], instr, machine_code))
            machine_code = ""
        #Type E
        if instr[0] in typeE:
            print(TypeE_machineCode(instr[0], instr, machine_code))
            machine_code = ""
        #Type F
        if instr[0] in typeF:
            print(TypeF_machineCode(instr[0], instr, machine_code))
            machine_code = ""

        #label handling
        if instr[0][0:-1] in labels and instr[1] in typeA:
            print(TypeA_label_machineCode(instr[1], instr, machine_code))
            machine_code = ""
        #Type B
        if instr[0][0:-1] in labels and instr[1] in typeB and instr[3] not in registers:
            print(TypeB__label_machineCode(instr[1], instr, machine_code))
            machine_code = ""
        #Type C
        if instr[0][0:-1] in labels and instr[1] in typeC and instr[3] in registers:
            print(TypeC_label_machineCode(instr[1], instr, machine_code))
            machine_code = ""
        #Type D
        if instr[0][0:-1] in labels and instr[1] in typeD:
            print(TypeD_label_machineCode(instr[1], instr, machine_code))
            machine_code = ""
        #Type E
        if instr[0][0:-1] in labels and instr[1] in typeE:
            print(TypeE_label_machineCode(instr[1], instr, machine_code))
            machine_code = ""
        #Type F
        if instr[0][0:-1] in labels and instr[1] in typeF:
            print(TypeF_label_machineCode(instr[1], instr, machine_code))
            machine_code = ""

while True:
    if Overflow_error(normal):
        break
    if typo_general_error(normal, labels):
        break
    if var_error(normal, var_list, var):
        break
    if Imm_value_error(normal):
        break
    if label_error(normal, labels, var_list):
        break
    if halterror(normal, count):
        break
    else:
        machineCode(normal)
        break
